# Papelería Santiago 2.0 - Frontend

Proyecto Frontend desarrollado con Vue.js 2 para la aplicación de Papelería Santiago.

## 📋 Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:
- [Node.js](https://nodejs.org/) (versión 14.x o superior)
- [npm](https://www.npmjs.com/) (viene incluido con Node.js) o [yarn](https://yarnpkg.com/)

## 🚀 Pasos para Clonar y Configurar el Proyecto

### 1. Clonar el repositorio
```bash
git clone <URL_DEL_REPOSITORIO>
cd proyectooo
```

### 2. Instalar las dependencias
```bash
npm install
npm install axios
```

### 3. Ejecutar el servidor de desarrollo
```bash
```

El proyecto estará disponible en `http://localhost:8080` (o el puerto que indique la consola)

## 📝 Comandos Disponibles

### Desarrollo
```bash
npm run serve
```
Compila y ejecuta el proyecto en modo desarrollo con recarga automática.

### Producción
```bash
npm run build
```
Compila y minifica el proyecto para producción. Los archivos generados estarán en la carpeta `/dist`.

### Linter
```bash
npm run lint
```
Ejecuta el linter para detectar y corregir errores de código.

## 🛠️ Tecnologías Utilizadas

- Vue.js 2.6.14
- Vue CLI 5.0
- Tailwind CSS 4.1.17
- ESLint
- Babel

## 📦 Estructura del Proyecto

```
proyectooo/
├── public/          # Archivos públicos estáticos
├── src/
│   ├── assets/     # Recursos estáticos (imágenes, CSS)
│   ├── components/ # Componentes Vue
│   └── App.vue     # Componente principal
├── babel.config.js # Configuración de Babel
├── vue.config.js   # Configuración de Vue CLI
└── package.json    # Dependencias del proyecto
```

## 📤 Subir el Proyecto a GitHub

Si necesitas subir este proyecto a GitHub por primera vez:

### 1. Inicializar Git (si no está inicializado)
```bash
git init
```

### 2. Agregar el repositorio remoto
```bash
git remote add origin <URL_DEL_REPOSITORIO_GITHUB>
```

### 3. Agregar todos los archivos
```bash
git add .
```

### 4. Hacer commit
```bash
git commit -m "Initial commit: Frontend Vue.js project"
```

### 5. Subir a GitHub
```bash
git push -u origin Front-End
```

## ⚠️ Notas Importantes

- Asegúrate de que el archivo `.gitignore` esté correctamente configurado antes de hacer commit
- Nunca subas archivos sensibles como contraseñas o API keys
- El directorio `node_modules` no debe subirse al repositorio (ya está en `.gitignore`)

## 📚 Referencias

- [Vue.js Documentation](https://vuejs.org/)
- [Vue CLI Documentation](https://cli.vuejs.org/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
