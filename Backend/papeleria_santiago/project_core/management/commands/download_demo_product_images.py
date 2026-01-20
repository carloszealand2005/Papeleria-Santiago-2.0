import os
from pathlib import Path
from urllib.request import Request, urlopen

from django.conf import settings
from django.core.management.base import BaseCommand

from project_core.models import Producto


class Command(BaseCommand):
    help = (
        "Descarga imágenes demo para todos los productos y actualiza Producto.imagen_url "
        "para apuntar a /media/productos/<SKU>.jpg (o URL absoluta si se especifica --base-url)."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--limit",
            type=int,
            default=None,
            help="Límite de productos a procesar (útil para pruebas).",
        )
        parser.add_argument(
            "--base-url",
            type=str,
            default="http://127.0.0.1:8000",
            help="Base URL para construir imagen_url absoluta (default: http://127.0.0.1:8000).",
        )
        parser.add_argument(
            "--overwrite",
            action="store_true",
            help="Si se pasa, re-descarga aunque el archivo ya exista.",
        )
        parser.add_argument(
            "--source",
            type=str,
            default="picsum",
            choices=["picsum", "placehold"],
            help="Fuente de imágenes demo: picsum (foto real) o placehold (texto). Default: picsum.",
        )
        parser.add_argument(
            "--only-missing",
            action="store_true",
            help="Si se pasa, solo procesa productos que no tienen imagen_url.",
        )

    def handle(self, *args, **options):
        limit = options["limit"]
        base_url = str(options["base_url"] or "").rstrip("/")
        overwrite = bool(options["overwrite"])
        only_missing = bool(options["only_missing"])
        source = str(options["source"] or "picsum").strip().lower()

        if not getattr(settings, "MEDIA_ROOT", None) or not getattr(settings, "MEDIA_URL", None):
            raise SystemExit("MEDIA_ROOT/MEDIA_URL no están configurados en settings.py.")

        dest_dir = Path(settings.MEDIA_ROOT) / "productos"
        dest_dir.mkdir(parents=True, exist_ok=True)

        qs = Producto.objects.all().order_by("SKU")
        if only_missing:
            qs = qs.filter(imagen_url__isnull=True) | qs.filter(imagen_url="")
            qs = qs.order_by("SKU")
        if limit:
            qs = qs[: int(limit)]

        total = qs.count() if hasattr(qs, "count") else len(list(qs))
        self.stdout.write(f"Productos a procesar: {total}")

        def image_source_url(producto: Producto) -> str:
            # picsum: fotos reales genéricas pero deterministas por SKU (mejor “se ve como producto” para demo)
            if source == "picsum":
                return f"https://picsum.photos/seed/{producto.SKU}/800/800"
            # placehold: texto (útil si quieres ver SKU/nombre en la imagen)
            text = f"{producto.SKU} - {producto.nombre}"[:80]
            from urllib.parse import quote
            return f"https://placehold.co/800x800/jpg?text={quote(text)}"

        def media_absolute_url(filename: str) -> str:
            # Usar URL absoluta porque Producto.imagen_url es URLField (validador espera esquema).
            return f"{base_url}{settings.MEDIA_URL}productos/{filename}".replace("//media/", "/media/")

        processed = 0
        downloaded = 0

        for producto in qs:
            filename = f"{producto.SKU}.jpg"
            out_path = dest_dir / filename

            if out_path.exists() and not overwrite:
                # Igual actualizamos imagen_url si falta o está vacío
                if not producto.imagen_url:
                    producto.imagen_url = media_absolute_url(filename)
                    producto.save(update_fields=["imagen_url"])
                processed += 1
                continue

            url = image_source_url(producto)
            req = Request(url, headers={"User-Agent": "PapeleriaSantiagoDemo/1.0"})
            with urlopen(req, timeout=30) as resp:
                content = resp.read()

            out_path.write_bytes(content)
            downloaded += 1

            producto.imagen_url = media_absolute_url(filename)
            producto.save(update_fields=["imagen_url"])
            processed += 1

        self.stdout.write(self.style.SUCCESS(f"Listo. Procesados={processed}, descargados={downloaded}, carpeta={dest_dir}"))


