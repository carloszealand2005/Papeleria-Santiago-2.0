import json
import re
import time
from pathlib import Path
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import models

from project_core.models import Producto


class Command(BaseCommand):
    help = (
        "Busca imágenes relacionadas en Pixabay por nombre/marca/subcategoría y rellena "
        "Producto.imagen_url, imagen_url2, imagen_url3, imagen_url4.\n"
        "\n"
        "Por defecto DESCARGA las imágenes a MEDIA_ROOT/productos_api/ y guarda URLs locales "
        "(http://127.0.0.1:8000/media/productos_api/<SKU>_<n>.jpg).\n"
        "Si quieres guardar URLs externas en vez de descargar, usa --external-only.\n"
        "\n"
        "Requiere API key de Pixabay (PIXABAY_API_KEY en .env/entorno, o pasar --api-key)."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--api-key",
            type=str,
            default=None,
            help="API key de Pixabay. Recomendado: usar variable de entorno PIXABAY_API_KEY.",
        )
        parser.add_argument(
            "--limit",
            type=int,
            default=None,
            help="Límite de productos a procesar (útil para pruebas).",
        )
        parser.add_argument(
            "--sku",
            type=str,
            default=None,
            help="Procesar solo un SKU específico (útil para pruebas).",
        )
        parser.add_argument(
            "--base-url",
            type=str,
            default="http://127.0.0.1:8000",
            help="Base URL para construir URLs locales cuando se descargan (default: http://127.0.0.1:8000).",
        )
        parser.add_argument(
            "--only-missing",
            action="store_true",
            help="Si se pasa, solo procesa productos que tengan ALGUNA imagen_url* vacía.",
        )
        parser.add_argument(
            "--overwrite",
            action="store_true",
            help="Si se pasa, sobre-escribe todas las imagen_url* aunque ya tengan valor.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Si se pasa, no guarda nada en DB ni descarga archivos; solo imprime lo que haría.",
        )
        parser.add_argument(
            "--external-only",
            action="store_true",
            help="Si se pasa, NO descarga a MEDIA_ROOT; guarda URLs externas directas de Pixabay.",
        )
        parser.add_argument(
            "--per-page",
            type=int,
            default=30,
            help="Cantidad de resultados a pedir a la API por búsqueda (default: 30).",
        )
        parser.add_argument(
            "--throttle",
            type=float,
            default=0.20,
            help="Segundos de pausa entre llamadas a la API (default: 0.20).",
        )

    def handle(self, *args, **options):
        # API key: preferir entorno / .env (settings.py ya carga .env) o pasar explícitamente --api-key.
        api_key = (options.get("api_key") or "").strip()
        if not api_key:
            import os
            api_key = (os.environ.get("PIXABAY_API_KEY") or "").strip()

        if not api_key:
            raise SystemExit(
                "Falta PIXABAY_API_KEY. Define PIXABAY_API_KEY en tu .env o variable de entorno, "
                "o pásala con --api-key."
            )

        if not getattr(settings, "MEDIA_ROOT", None) or not getattr(settings, "MEDIA_URL", None):
            raise SystemExit("MEDIA_ROOT/MEDIA_URL no están configurados en settings.py.")

        base_url = str(options.get("base_url") or "").rstrip("/")
        limit = options.get("limit")
        sku = (options.get("sku") or "").strip()
        only_missing = bool(options.get("only_missing"))
        overwrite = bool(options.get("overwrite"))
        dry_run = bool(options.get("dry_run"))
        external_only = bool(options.get("external_only"))
        per_page = int(options.get("per_page") or 30)
        throttle = float(options.get("throttle") or 0.0)

        # Carpeta NUEVA (no toca media/productos/ legacy)
        dest_subdir = "productos_api"
        dest_dir = Path(settings.MEDIA_ROOT) / dest_subdir
        if not external_only and not dry_run:
            dest_dir.mkdir(parents=True, exist_ok=True)

        qs = Producto.objects.all().order_by("SKU")
        if sku:
            qs = qs.filter(SKU=sku)
        if only_missing:
            qs = qs.filter(
                models.Q(imagen_url__isnull=True) | models.Q(imagen_url="") |
                models.Q(imagen_url2__isnull=True) | models.Q(imagen_url2="") |
                models.Q(imagen_url3__isnull=True) | models.Q(imagen_url3="") |
                models.Q(imagen_url4__isnull=True) | models.Q(imagen_url4="")
            ).order_by("SKU")
        if limit:
            qs = qs[: int(limit)]

        total = qs.count() if hasattr(qs, "count") else len(list(qs))
        self.stdout.write(f"Productos a procesar: {total}")

        def media_absolute_url(filename: str) -> str:
            # Usar URL absoluta porque Producto.imagen_url es URLField (validador espera esquema).
            url = f"{base_url}{settings.MEDIA_URL}{dest_subdir}/{filename}"
            return url.replace("//media/", "/media/")

        def clean_text(s: str) -> str:
            return re.sub(r"\s+", " ", (s or "").strip())

        def strip_trailing_counter(name: str) -> str:
            """
            Quita sufijos típicos tipo " 001" al final del nombre.
            Importante: solo quita si son 3+ dígitos al final (para no romper 'A4' o '2B').
            """
            return re.sub(r"\s+\d{3,}$", "", clean_text(name)).strip()

        def build_queries(producto: Producto) -> list[str]:
            nombre = clean_text(getattr(producto, "nombre", "") or "")
            marca = clean_text(getattr(producto, "marca", "") or "")
            subcat = ""
            try:
                if getattr(producto, "subcategoria", None):
                    subcat = clean_text(getattr(producto.subcategoria, "nombre_subcategoria", "") or "")
            except Exception:
                subcat = ""

            nombre_stripped = strip_trailing_counter(nombre)

            # Estrategia:
            # 1) Intentar full (incluye marca/subcat) para acercarse a algo más específico
            # 2) Si no alcanza 4 hits, intentar variantes más generales
            variants = [
                " ".join([nombre, marca, subcat]).strip(),
                " ".join([nombre_stripped, marca, subcat]).strip(),
                " ".join([nombre_stripped, subcat]).strip(),
                nombre_stripped or nombre,
            ]
            seen = set()
            out = []
            for q in variants:
                q = clean_text(q)
                if q and q not in seen:
                    seen.add(q)
                    out.append(q)
            return out

        def pixabay_search(query: str) -> list[str]:
            params = {
                "key": api_key,
                "q": query,
                "image_type": "photo",
                "safesearch": "true",
                "per_page": str(per_page),
                "lang": "es",
            }
            url = f"https://pixabay.com/api/?{urlencode(params)}"
            req = Request(url, headers={"User-Agent": "PapeleriaSantiago/1.0"})
            with urlopen(req, timeout=30) as resp:
                payload = resp.read()
            data = json.loads(payload.decode("utf-8"))
            hits = data.get("hits") or []
            urls = []
            for h in hits:
                u = h.get("largeImageURL") or h.get("webformatURL") or h.get("previewURL")
                if isinstance(u, str) and u.startswith("http"):
                    urls.append(u)
            return urls

        def guess_extension(image_url: str) -> str:
            try:
                path = urlparse(image_url).path or ""
                ext = Path(path).suffix.lower()
                if ext in (".jpg", ".jpeg", ".png", ".webp"):
                    return ext
            except Exception:
                pass
            return ".jpg"

        def download_to_media(image_url: str, filename: str) -> None:
            req = Request(image_url, headers={"User-Agent": "PapeleriaSantiago/1.0"})
            with urlopen(req, timeout=45) as resp:
                content = resp.read()
            (dest_dir / filename).write_bytes(content)

        processed = 0
        updated = 0
        downloaded = 0
        not_found = 0

        for producto in qs:
            processed += 1

            current = [
                getattr(producto, "imagen_url", None),
                getattr(producto, "imagen_url2", None),
                getattr(producto, "imagen_url3", None),
                getattr(producto, "imagen_url4", None),
            ]
            if only_missing and all(bool(x) for x in current):
                continue

            queries = build_queries(producto)
            candidates: list[str] = []
            seen_urls = set()

            for q in queries:
                if throttle:
                    time.sleep(throttle)
                try:
                    urls = pixabay_search(q)
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"[{producto.SKU}] Error buscando '{q}': {e}"))
                    continue
                for u in urls:
                    if u not in seen_urls:
                        seen_urls.add(u)
                        candidates.append(u)
                    if len(candidates) >= 4:
                        break
                if len(candidates) >= 4:
                    break

            if not candidates:
                not_found += 1
                self.stdout.write(self.style.WARNING(f"[{producto.SKU}] Sin resultados (queries: {queries[:2]}...)"))
                continue

            # Preparar 4 valores (puede haber <4)
            chosen = candidates[:4]
            while len(chosen) < 4:
                chosen.append(None)

            new_values: list[str | None] = [None, None, None, None]
            new_sources: list[str | None] = [None, None, None, None]

            for idx, src_url in enumerate(chosen, start=1):
                if not src_url:
                    continue
                new_sources[idx - 1] = src_url
                if external_only:
                    new_values[idx - 1] = src_url
                    continue

                ext = guess_extension(src_url)
                filename = f"{producto.SKU}_{idx}{ext}"
                if dry_run:
                    new_values[idx - 1] = media_absolute_url(filename)
                    continue

                try:
                    download_to_media(src_url, filename)
                    downloaded += 1
                    new_values[idx - 1] = media_absolute_url(filename)
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"[{producto.SKU}] Error descargando {src_url}: {e}"))
                    # Fallback: si falla descarga, al menos dejar URL externa (mejor que nada)
                    new_values[idx - 1] = src_url

            # Aplicar reglas de overwrite vs fill-missing
            fields = ["imagen_url", "imagen_url2", "imagen_url3", "imagen_url4"]
            to_update = {}

            for i, field in enumerate(fields):
                incoming = new_values[i]
                if overwrite:
                    to_update[field] = incoming
                else:
                    # solo llenar si está vacío
                    if not getattr(producto, field):
                        to_update[field] = incoming

            # En dry-run solo reportar
            if dry_run:
                preview = {
                    "SKU": producto.SKU,
                    "nombre": producto.nombre,
                    "queries": queries,
                    "sources": new_sources,
                    "would_set": to_update,
                    "mode": "external-only" if external_only else "download+local-url",
                }
                self.stdout.write(json.dumps(preview, ensure_ascii=False))
                continue

            if to_update:
                for k, v in to_update.items():
                    setattr(producto, k, v)
                producto.save(update_fields=list(to_update.keys()))
                updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Listo. Procesados={processed}, actualizados={updated}, descargados={downloaded}, sin_resultados={not_found}, "
                f"carpeta_local={(str(dest_dir) if not external_only else 'N/A')}."
            )
        )


