# BioControl + BioControl IA

Esta versión conserva las funciones de la plataforma original e incorpora un chat técnico de IA que puede consultar el contexto local de equipos, mantenimientos y ciclos registrados en el navegador.

## Requisitos

- Node.js 20 o superior.
- Una clave de API de OpenAI con facturación/uso habilitado. La suscripción de ChatGPT no incluye automáticamente saldo de API.
- Conexión a internet para que el servidor consulte el modelo.

## Publicación: GitHub Pages + Render

Tu repositorio es `https://github.com/jimmyalmaciasmo-oss/BioControl1`. GitHub Pages aloja el frontend estático; el servidor `server.js` debe ejecutarse en un servicio Node como Render.

1. Sube al directorio raíz de tu repositorio los archivos `index.html`, `config.js`, `server.js`, `package.json`, `package-lock.json` (si existe), `render.yaml`, `README.md`, `LEEME.txt`, `manifest.json`, `sw.js`, `.nojekyll` y el manual PDF. Conserva el archivo `config.js`.
2. En Render crea un servicio **Web Service** conectado al repositorio `jimmyalmaciasmo-oss/BioControl1`.
3. Configura **Build Command**: `npm install` y **Start Command**: `npm start`.
4. En variables de entorno de Render agrega `OPENAI_API_KEY` (tu clave privada), `OPENAI_MODEL` (`gpt-5-mini`) y `CORS_ORIGIN` (`https://jimmyalmaciasmo-oss.github.io`). Si GitHub Pages muestra otra URL, usa exactamente ese origen, sin la ruta final `/BioControl1/`.
5. Cuando Render entregue una URL como `https://biocontrol-ia.onrender.com`, edita `config.js` en GitHub y reemplaza `https://TU-SERVICIO.onrender.com` por esa URL real.
6. Guarda los cambios y espera a que GitHub Pages publique. Abre `https://jimmyalmaciasmo-oss.github.io/BioControl1/` y prueba el chat.
7. Comprueba el backend abriendo `https://TU-SERVICIO.onrender.com/api/health`. Debe responder `ok: true` y `aiConfigured: true`.

**Importante:** no subas `.env`, claves API ni credenciales al repositorio. Usa únicamente las variables secretas de Render.

## Instalación local en Windows

1. Descarga y descomprime `BioControl_IA_Completo.zip`.
2. Instala Node.js 20 o superior desde https://nodejs.org/.
3. Abre la carpeta descomprimida.
4. En la barra de direcciones del Explorador escribe `cmd` y pulsa Enter.
5. Ejecuta:

   ```bash
   npm install
   ```

6. Copia `.env.example`, pega la copia en la misma carpeta y nómbrala `.env`.
7. Abre `.env` con el Bloc de notas y reemplaza `pega_aqui_tu_clave_api` por tu clave real:

   ```env
   OPENAI_API_KEY=tu_clave_real
   OPENAI_MODEL=gpt-5-mini
   PORT=3000
   ```

   No compartas este archivo, no lo subas a GitHub y no pegues la clave en `index.html`.

8. En la consola ejecuta:

   ```bash
   npm start
   ```

9. Abre en el navegador: http://localhost:3000
10. Pulsa el botón **BioControl IA** de la esquina inferior derecha y realiza una consulta.

## Verificación

Abre http://localhost:3000/api/health. Debe mostrar `ok: true` y `aiConfigured: true`. Si `aiConfigured` es `false`, revisa que el archivo se llame exactamente `.env`, que esté junto a `server.js` y que el servidor se haya reiniciado.

## Cómo usa los equipos registrados

El navegador envía al servidor únicamente datos técnicos seleccionados de los registros locales: código, nombre, marca, modelo, serie, estado, ubicación, fechas, observaciones, mantenimientos y ciclos. No envía fotografías ni documentos adjuntos. El servidor vuelve a filtrar los campos y limita el tamaño de la solicitud.

La conversación se conserva temporalmente en la memoria de la página mientras está abierta. No se guarda el chat en una base de datos. La solicitud a OpenAI usa `store: false`, pero el tratamiento de datos también depende de las políticas y condiciones vigentes del proveedor.

## Importante sobre publicación

- No abras `index.html` directamente con doble clic: la IA necesita el servidor Node.
- GitHub Pages por sí solo no ejecuta `server.js`. Para publicar la IA en internet debes desplegar el servidor Node en un hosting compatible (por ejemplo, Render, Railway o un VPS), configurar allí `OPENAI_API_KEY` como variable secreta y servir el frontend desde el mismo dominio/origen o configurar un proxy seguro.
- No uses una clave API en el navegador ni en un repositorio público.
- Esta versión conserva el almacenamiento local del proyecto original. Los registros de un navegador no se sincronizan automáticamente con otros dispositivos. Para trabajo multiusuario real se debe incorporar autenticación de servidor y base de datos centralizada.
- La asistente brinda orientación técnica y no reemplaza el manual del fabricante, los protocolos institucionales ni al personal biomédico autorizado. Ante fallas que comprometan esterilización, seguridad eléctrica, presión o seguridad del paciente, suspende el uso y escala la revisión.

## Archivos

- `index.html`: plataforma BioControl y ventana de chat.
- `config.js`: URL pública del backend; se puede editar desde GitHub.
- `render.yaml`: plantilla de despliegue para Render.
- `server.js`: servidor y conexión segura con OpenAI.
- `package.json`: dependencias y comandos.
- `.env.example`: plantilla de configuración.
- `.gitignore`: evita subir claves y dependencias.

En Windows también puedes ejecutar `INICIAR_BIOCONTROL.bat`; el archivo comprueba Node.js, instala dependencias y crea la plantilla `.env` si hace falta.
