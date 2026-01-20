## Fixtures (datos iniciales)

### Qué hay aquí
- `initial_data.json`: categorías/subcategorías/variantes + un set pequeño de productos de ejemplo.
- `generate_category_fixtures.py` (management command): genera productos inventados (opción A) por categoría.
- `download_demo_product_images.py` (management command): descarga imágenes demo y las asigna a `Producto.imagen_url`.

### Generar 50 productos por categoría (Oficina/Escolar/Tecnología)
Desde la carpeta donde está `manage.py`:

```bash
python manage.py generate_category_fixtures --count 50
```

Esto crea:
- `project_core/fixtures/productos_oficina.json`
- `project_core/fixtures/productos_escolar.json`
- `project_core/fixtures/productos_tecnologia.json`
- `project_core/fixtures/initial_data_full.json` (base + productos)

### Cargar datos en la BD
Opción 1 (recomendada, un solo archivo):

```bash
python manage.py loaddata project_core/fixtures/initial_data_full.json
```

Opción 2 (múltiples archivos):

```bash
python manage.py loaddata project_core/fixtures/initial_data.json project_core/fixtures/productos_oficina.json project_core/fixtures/productos_escolar.json project_core/fixtures/productos_tecnologia.json
```

> Nota: No cargues **ambas** opciones en la misma BD, porque duplicarías registros.

### Descargar imágenes demo para productos (solo para pruebas)
Desde la carpeta donde está `manage.py`:

```bash
python manage.py download_demo_product_images --base-url http://127.0.0.1:8000
```

Notas:
- Guarda archivos en `MEDIA_ROOT/productos/`.
- Actualiza `Producto.imagen_url` con una URL absoluta tipo `http://127.0.0.1:8000/media/productos/<SKU>.jpg`.
- Si quieres probar con pocos registros: `--limit 10`
- Si quieres re-descargar: `--overwrite`


