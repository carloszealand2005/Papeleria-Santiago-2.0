import json
import random
from decimal import Decimal
from pathlib import Path

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Genera fixtures de productos (opción A) por categoría y un initial_data_full.json (base + productos)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            type=int,
            default=50,
            help="Cantidad de productos por categoría (default: 50).",
        )
        parser.add_argument(
            "--seed",
            type=int,
            default=20260120,
            help="Seed para generación determinista (default: 20260120).",
        )
        parser.add_argument(
            "--outdir",
            type=str,
            default=None,
            help="Directorio de salida (default: project_core/fixtures).",
        )
        parser.add_argument(
            "--base-fixture",
            type=str,
            default=None,
            help="Ruta del fixture base (default: project_core/fixtures/initial_data.json).",
        )

    def handle(self, *args, **options):
        count = int(options["count"])
        seed = int(options["seed"])
        rnd = random.Random(seed)

        fixtures_dir = Path(options["outdir"] or Path(__file__).resolve().parents[2] / "fixtures")
        fixtures_dir.mkdir(parents=True, exist_ok=True)

        base_fixture_path = Path(options["base_fixture"] or (fixtures_dir / "initial_data.json"))
        if not base_fixture_path.exists():
            raise SystemExit(f"No existe el fixture base: {base_fixture_path}")

        base_data = json.loads(base_fixture_path.read_text(encoding="utf-8"))

        max_precio_pk = max((int(obj["pk"]) for obj in base_data if obj.get("model") == "project_core.precio"), default=0)
        max_inv_pk = max((int(obj["pk"]) for obj in base_data if obj.get("model") == "project_core.inventario"), default=0)
        next_precio_pk = max_precio_pk + 1
        next_inv_pk = max_inv_pk + 1

        # IDs fijos según tu fixture actual:
        CATEGORIAS = {
            "Oficina": 1,
            "Escolar": 2,
            "Tecnología": 3,
        }
        SUBCATS = {
            # Oficina
            "Papelería": 1,
            "Escritura": 2,
            "Organización": 3,
            # Escolar
            "Regreso a Clases": 4,
            "Manualidades": 5,
            # Tecnología
            "Accesorios Tech": 6,
        }
        # Variantes existentes en initial_data.json
        VARIANTES = {
            # subcat 1
            "Tamaño Carta": 1,
            "Tamaño Oficio": 2,
            # subcat 2
            "Color Azul": 3,
            "Color Negro": 4,
            # subcat 4
            "Básico": 5,
            "Premium": 6,
            # subcat 6
            "USB 3.0": 7,
            "Bluetooth": 8,
        }

        marcas_oficina = ["OfficePro", "FilePro", "PaperMax", "MarkPro", "StickNote"]
        marcas_escolar = ["SchoolLine", "GraphiPlus", "SafeCut", "Adherix", "ColorArt"]
        marcas_tech = ["DataFlash", "SoundGo", "TechNova", "WireLink", "PowerPlus"]

        nombres_oficina = [
            "Carpeta Plástica A4",
            "Archivador Palanca A4",
            "Resma Papel Bond A4 75g",
            "Notas Adhesivas 76x76mm",
            "Grapadora Metálica",
            "Clips Metálicos (Caja)",
            "Cinta Adhesiva Transparente 48mm",
            "Marcador Permanente",
            "Corrector Líquido 20ml",
            "Bandeja Organizadora A4",
        ]
        nombres_escolar = [
            "Cuaderno Espiral 100 Hojas",
            "Lápiz HB #2",
            "Borrador Blanco",
            "Sacapuntas Doble",
            "Regla 30cm",
            "Tijeras Escolares Punta Roma",
            "Pegamento Líquido 200ml",
            "Cartulina A4 (Pack)",
            "Colores 12 unidades",
            "Marcadores Lavables (Pack)",
        ]
        nombres_tech = [
            "Memoria USB 32GB",
            "Memoria USB 64GB",
            "Audífonos Bluetooth",
            "Cable USB-C 1m",
            "Cargador 20W USB-C",
            "Mouse Inalámbrico",
            "Teclado Bluetooth",
            "Adaptador HDMI",
            "Power Bank 10,000mAh",
            "Tarjeta MicroSD 64GB",
        ]

        def _dec(val: Decimal) -> str:
            return str(val.quantize(Decimal("0.01")))

        def make_producto(sku: str, categoria_id: int, subcat_id: int, variante_id: int | None, nombre: str, marca: str, iva: Decimal):
            nonlocal next_precio_pk, next_inv_pk

            codigo_barras = f"789{seed % 1000000:06d}{int(sku[-3:]):03d}"
            total_vendidos = rnd.randint(0, 600)

            # precios: rango por categoría (coherente con tu excel: muchos precios pequeños y algunos altos)
            if categoria_id == CATEGORIAS["Tecnología"]:
                pvp = Decimal(rnd.choice([8, 10, 12, 15, 18, 25, 35, 50, 75, 120, 150])) + Decimal(rnd.randint(0, 99)) / Decimal(100)
            else:
                pvp = Decimal(rnd.choice([0.35, 0.48, 0.87, 1.00, 1.20, 1.74, 2.10, 2.50, 3.30, 4.65, 6.10, 8.90, 11.73, 14.26, 17.70, 25.30]))  # estilo excel

            # pvm ligeramente menor
            pvm = (pvp * Decimal("0.93")).quantize(Decimal("0.0001"))
            desc_pub = Decimal(rnd.choice([0, 5, 10, 15, 20]))
            desc_may = Decimal(rnd.choice([0, 5, 10, 15]))

            stock = rnd.choice([0, 0, 0, 1, 2, 4, 6, 11, 22, 49, 72, 112, 180, 574, 896, 987, 998, 1200, 4590, 6367])

            producto = {
                "model": "project_core.producto",
                "pk": sku,
                "fields": {
                    "codigo_barras": codigo_barras,
                    "nombre": nombre,
                    "descripcion": f"{nombre} - producto generado (MVP).",
                    "marca": marca,
                    "categoria": categoria_id,
                    "subcategoria": subcat_id,
                    "variante": variante_id,
                    "caracteristica1": None,
                    "caracteristica2": None,
                    "caracteristica3": None,
                    "caracteristica4": None,
                    "caracteristica5": None,
                    # Imagen demo (remota) determinista por SKU para que SIEMPRE se vea algo aunque no descargues a local.
                    # Luego puedes bajar las imágenes con `download_demo_product_images` para servir desde /media/.
                    "imagen_url": f"https://picsum.photos/seed/{sku}/800/800",
                    "imagen_url2": None,
                    "imagen_url3": None,
                    "imagen_url4": None,
                    "total_vendidos": total_vendidos,
                    "disponible_mayorista": True,
                    "bulto_minimo_mayorista": 1,
                },
            }

            precio = {
                "model": "project_core.precio",
                "pk": next_precio_pk,
                "fields": {
                    "producto": sku,
                    "pvp": _dec(pvp),
                    "pvm": str(pvm),
                    "iva": _dec(iva),
                    "descuento_publico": _dec(desc_pub),
                    "descuento_mayorista": _dec(desc_may),
                },
            }
            next_precio_pk += 1

            inventario = {
                "model": "project_core.inventario",
                "pk": next_inv_pk,
                "fields": {
                    "producto": sku,
                    "stock": stock,
                    "ubicacion_bodega": f"Bodega {categoria_id}, Estante {rnd.randint(1, 9)}",
                },
            }
            next_inv_pk += 1

            return [producto, precio, inventario]

        def build_categoria(nombre_categoria: str, prefix: str, nombres: list[str], marcas: list[str], subcats: list[int], iva: Decimal, variantes_pool: list[int | None]):
            items: list[dict] = []
            for i in range(1, count + 1):
                sku = f"{prefix}{i:03d}"
                nombre = f"{nombres[(i - 1) % len(nombres)]} {i:03d}"
                marca = marcas[(i - 1) % len(marcas)]
                subcat_id = subcats[(i - 1) % len(subcats)]
                variante_id = variantes_pool[(i - 1) % len(variantes_pool)]
                # Si la variante no pertenece a esa subcategoría, permitir None (simple MVP)
                if variante_id not in (None, 1, 2, 3, 4, 5, 6, 7, 8):
                    variante_id = None
                items.extend(make_producto(sku, CATEGORIAS[nombre_categoria], subcat_id, variante_id, nombre, marca, iva))
            return items

        oficina = build_categoria(
            "Oficina",
            "OFI",
            nombres_oficina,
            marcas_oficina,
            [SUBCATS["Papelería"], SUBCATS["Escritura"], SUBCATS["Organización"]],
            Decimal("15.00"),
            [VARIANTES["Tamaño Carta"], VARIANTES["Tamaño Oficio"], VARIANTES["Color Azul"], VARIANTES["Color Negro"], None],
        )

        escolar = build_categoria(
            "Escolar",
            "ESC",
            nombres_escolar,
            marcas_escolar,
            [SUBCATS["Regreso a Clases"], SUBCATS["Manualidades"]],
            Decimal("15.00"),
            [VARIANTES["Básico"], VARIANTES["Premium"], None],
        )

        tecnologia = build_categoria(
            "Tecnología",
            "TEC",
            nombres_tech,
            marcas_tech,
            [SUBCATS["Accesorios Tech"]],
            Decimal("15.00"),
            [VARIANTES["USB 3.0"], VARIANTES["Bluetooth"], None],
        )

        (fixtures_dir / "productos_oficina.json").write_text(json.dumps(oficina, ensure_ascii=False, indent=2), encoding="utf-8")
        (fixtures_dir / "productos_escolar.json").write_text(json.dumps(escolar, ensure_ascii=False, indent=2), encoding="utf-8")
        (fixtures_dir / "productos_tecnologia.json").write_text(json.dumps(tecnologia, ensure_ascii=False, indent=2), encoding="utf-8")

        # Fixture full (base + productos). OJO: si luego haces loaddata de initial_data.json y también de initial_data_full.json,
        # tendrás duplicados. Usa uno u otro.
        full = list(base_data) + list(oficina) + list(escolar) + list(tecnologia)
        (fixtures_dir / "initial_data_full.json").write_text(json.dumps(full, ensure_ascii=False, indent=2), encoding="utf-8")

        self.stdout.write(self.style.SUCCESS("Fixtures generados: productos_oficina.json, productos_escolar.json, productos_tecnologia.json, initial_data_full.json"))


