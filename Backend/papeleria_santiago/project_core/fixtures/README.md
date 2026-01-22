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

---

### Rellenar imágenes REALES (relacionadas) vía Pixabay (recomendado para MVP)
Este comando busca imágenes relacionadas por **nombre + marca + subcategoría** y llena:
`imagen_url`, `imagen_url2`, `imagen_url3`, `imagen_url4`.

Por defecto:
- Descarga archivos a `MEDIA_ROOT/productos_api/`
- Guarda URLs locales tipo `http://127.0.0.1:8000/media/productos_api/<SKU>_<n>.jpg`

#### 1) Crear API key de Pixabay
- Crea una cuenta y genera un API key en Pixabay.
- Guarda el key como `PIXABAY_API_KEY`.

#### 2) Guardar el API key (recomendado: .env)
En la carpeta donde está `manage.py` (BASE_DIR), crea un archivo `.env` con:

```bash
PIXABAY_API_KEY=TU_KEY_AQUI
```

> Nota: `.env` NO debe subirse a Git.

#### 3) Ejecutar el comando
Ejemplos:

```bash
# Solo ver qué haría (no descarga ni guarda):
python manage.py fill_product_images_pixabay --dry-run --limit 5

# Procesar TODO (descarga a MEDIA_ROOT/productos_api/ y guarda URLs locales):
python manage.py fill_product_images_pixabay --base-url http://127.0.0.1:8000

# Solo completar campos faltantes (no pisa los que ya existan):
python manage.py fill_product_images_pixabay --only-missing

# Reemplazar SIEMPRE las 4 URLs aunque ya tengan valor:
python manage.py fill_product_images_pixabay --overwrite

# Guardar URLs externas (no descarga a tu media):
python manage.py fill_product_images_pixabay --external-only
```


