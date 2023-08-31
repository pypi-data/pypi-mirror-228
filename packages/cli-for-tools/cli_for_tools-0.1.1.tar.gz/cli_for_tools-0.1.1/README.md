<a href="https://www.islas.org.mx/"><img src="https://www.islas.org.mx/img/logo.svg" align="right" width="256" /></a>
# Cli Guadalupe Data

## `paco_el_chato`
Paco el chato es el asistente para las tareas de gabinete en el proyecto de erradicación de gato
feral en Isla Guadalupe.

Tiene tres habilidades:
- clasificar fotos con gatos
- generar un esbozo del mapa con trampas activas y desactivas de Isla Guadalupe
- actualizar la paquetería para hacer las tareas anteriores

## Instalación 🏗️
Podemos instalar esta aplicación usando `pip`:
```shell
pip uninstall cli_for_tools
pip install git+https://github.com/IslasGECI/cli_guadalupe_data@latest
```

## Modo de uso
Para utilizar `haz-mapa` o `clasifica-fotos` debemos abrir la terminal desde la carpeta de trabajo:
1. damos doble _click_ a la carpeta de trabajo
1. damos _click_ derecho al ratón y escogemos la opción **Open Terminal**
1. escribimos el comando `paco_el_chato --help` y tendremos la ayuda general
1. escribimos el comando `paco_el_chato haz-mapa --help` y tendremos la ayuda del comando `haz-mapa`
1. escribimos el comando `paco_el_chato clasifica-fotos --help` y tendremos la ayuda del comando `clasifica-fotos`

## `haz-mapa`
Hace un esbozo del mapa de Isla Guadalupe con las trampas activas e inactivas.

**Requerimiento**: En la carpeta de trabajo debe estar:
- IG_POSICION_{fecha}.txt         : Archivo que obtenemos de mapsource
- IG_POSICION_TRAMPAS_{fecha}.xlsx: Archivos con los esfuerzos de la semana

Al final generará el archivo `map_of_traps.jpg`.

## `clasifica-fotos`
Clasifica las fotos que vienen de las trampas cámara.

**Requerimiento**: En la carpeta de trabajo debe estar una carpeta (varias carpetas) con las fotos.
El nombre de la carpeta principal debe ser sin espacios. Por ejemplo:
- `FOTOS GATOS`: es un nombre incorrecto,
- `FOTOS_GATOS`: es un nombre correcto.

Al final generará la carpeta `cat_detected` con las fotos en las que detectó gato.

## `actualiza-comandos`
Actualiza los comandos:
- `haz-mapa`
- `clasifica-fotos`
