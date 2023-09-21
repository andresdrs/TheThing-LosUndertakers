# Como usar los tests de React y FastAPI

En esta branch tienen dos carpetas, una que dice `lacosa_v1` y `lacosa_v2`.

- **lacosa_v1** tiene una aplicación simple de React y FastAPI (que es la que vimos en el meet) que trata de una implementación de una página web permite agregar tareas a un listado.
- **lacosa_v2** tiene una aplicación un toque mas compleja que intenta asimilar "cómo" sería la idea de la parte de elección de nombre de usuario y creación/unión de partidas. La creación de partidas creo que funciona bien, lo que no pude hacer andar es el listado de las partidas existentes.

**Para correr cualquiera de las dos apps necesitan instalar**

1. Uvicorn: servidor que sirve para correr la aplicación.

    Se instala con: `sudo apt install uvicorn`

2. FastAPI: se instala con `pip install fastapi`.

    Si no tienen pip `sudo apt-get install python3-pip`

3. npm: para gestionar paquetes e instalar dependencias que se tengan que usar

    Tienen que ejecutar en secuencia: 

    `npm install`

    `npm install -g react-scripts`

4. nvm: para poder gestionar las versiones de node.js

    Se instala con 

    `curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash`

    luego, ejecutar en secuencia:

    `nvm install 14`

    `export NVM_DIR="$HOME/.nvm”` → esto es para que no tengas que cerrar y abrir vs code para que la instalación finalice

    `[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" # This loads nvm`

    `[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion”`

    `nvm use 14`

    `nvm alias default 14`

5. Axios: para hacer solicitudes HTTP (eso de usar método get, post etc)

    `npm install axios`

**Una vez instalado todo**

Ejemplo, si se quiere testear lacosa_v1, tenes que abrirte una terminal dentro de la carpeta backend y ejecutar `uvicorn main:app --reload`.

Luego, tenes que abrir otra terminal en paralelo en la carpeta frontend y ejecutar `npm start`

Esto debería abrirte una pestaña en google chrome. Cada vez que agreges un item a la lista, vas a ver en la terminal del backend si se proceso bien la solicitud.
