# Pasos de instalación

Para instalar nuestros paquetes comunitarios, instalaremos el contenido de la carpeta `ppdc_event_manager` utilizando `pip`.

## 1. Posiciónate en la carpeta.
`cd my-simulation-project/`

## 2. Creando un entorno

En Python, es posible que muchos proyectos utilicen paquetes en versiones específicas.
Además, el sistema operativo tendrá su propia versión de Python, preparada para su uso general.
Para separar la versión de nuestro SO a la de los proyectos, desde Python 3.11+, el sistema operativo protege instalaciones de paquetes globales para evitar inconsistencias.

Entonces, es posible que si intentas utilizar `pip install` aparezca un error indicando que la instalación rompería los paquetes globales.

Para eso primero debes verificar que tienes un ambiente Python para el proyecto, el cual además es _ignorado_ por git.
Los comandos son:

- `python -m venv venv` , que crea una carpeta `./venv/` con nuestro entorno Python. Esta misma carpeta debe ser ignorada por git.
- Para activar el entorno, debemos ejecutar el script que corresponda con nuestra terminal:
    - **Bash**: `source venv/bin/activate`
    - **Fish**: `source venv/bin/activate.fish`
    - **Windows Powershell**: `venv\Scripts\Activate.ps1`
    - **Windows CMD**: `venv\Scripts\activate.bat`
- Para verificar la activación, tu terminal debería mostrar (venv) al inicio de la línea.


## 3. Añade el repositorio como un submódulo.
`git submodule add https://github.com/Santasy/INFO81-S2-DesCom02.git ppdc-event-manager`

## 4. Inicia y hace update
`git submodule init`

`git submodule update`

## 5. Instala la parqueta como un paquete
`pip install -e ppdc-event-manager/`

El instalar con `-e` crea un link en los site-packages que apunta a la carpeta local del módulo.
Esto permite que los cambios estén disponibles inmediatamente.

## 6. Hace commit de la referencia a este nuevo sub-módulo
Hacemos seguimiento de los nuevos archivos, para que estén disponibles para el commit:
`git add .gitmodules ppdc-event-manager/`

Creamos finalmente el commit con todos los cambios:
`git commit -m "Se añadio ppdc-event-manager como submodulo."`