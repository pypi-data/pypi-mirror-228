# VidLink

Last updated 1st September 2023

A simple commandline app to extract all the raw video links from a set of urls

Commands [Click Here](#use)
Examples [Click Here](#ejemplos)
Changelog [Click Here](#changelog)

# TODO

---

- [X] Agregar dinámica de reintentos si falla la petición de una url.
- [X] Agregar característica para obtener el tamaño de los videos
- [X] Agregar característica para silenciar el procedimiento y que solo muestre el resultado en consola con un nuevo argumento
- [ ] Agregar más formatos de video
- [ ] Añadir más argumentos (como definir el tiempo de espera, cantidad máxima de reintentos, cargar un lenguaje específico)
- [ ] Añadir detección de otros tipos de flujos de datos de video
- [ ] Añadir compatibilidad con Youtube, Instagram, Facebook, Reddit, Twitch, Facebook

# Use

---

### English

```bash
usage: VidLink [-h] [-u URL [URL ...]] [-f FILE [FILE ...]] [-s [SAVE_FILE]] [-v] [url ...]

positional arguments:
  url

options:
  -h, --help show this help message and exit

  -u URL [URL ...], --url URL [URL ...] One or more urls separated by spaces (cannot be used at the same time as the argument -f)

  -f FILE [FILE ...], --file FILE [FILE ...] The address of one or more files containing urls separated by line jumps (cannot be used at the same time as the argument -u)

  -d [SAVE_FILE], --save_file [SAVE_FILE] Define if you want to save the links of the videos found in a file (a link will be saved by line with the format <file size> <link>) (this is an optional argument, if not defined, the results will be displayed on console)

  -s, --silent Run app in silent mode (return only the founded links if -d is not setted)

  -v, --version show program's version number and exit
```

### Spanish

```bash
uso: VidLink [-h] [-u URL [URL ...]] [-f FILE [FILE ...]] [-s [SAVE_FILE]] [-v] [url ...]

argumentos posicionales:
  url
  
opciones:
  -h, --help Muestra la ayuda

  -u URL [URL ...], --url URL [URL ...] Una o más urls separadas por espacios (no se puede usar a la vez que el argumento -f)

  -f FILE [FILE ...], --file FILE [FILE ...] La dirección de uno o más archivos que contengan urls separadas por saltos de líneas  (no se puede usar a la vez que el argumento -u)

  -d [SAVE_FILE], --save_file [SAVE_FILE] Define si se desea guardar los links de los videos encontrados en un archivo (se guardará un link por línea con el formato <tamaño del archivo> <link>) (este es un argumento opcional, si no se define, se mostrarán los resultados en consola)

  -s, --silent Ejecuta la aplicación en modo silencio (retorna solamente los links encontrados si -d no ha sido asignado)

  -v, --version Muestra la versión del programa
```

# Ejemplos

---

Puedes usar la app llamándola desde el cmd como cualquier otra app de consola, tiene actualmente 3 formas de uso:

1. Le pasas como argumento una o varias urls (separadas por espacios):

```bash
vidlink "https://webvideo.com"
```

o

```bash
vidlink "https://webvideo.com" "https://webvideo2.com"
```

2. Le pasas como argumento una o varias direcciones de archivos de texto (separadas por espacios) que contengan al menos una url por línea:

Tenemos un archivo "a.txt" que contiene:

```
https://webvideo.com
https://webvideo2.com
```

El comando para cargarlo sería:

```bash
vidlink -f "a.txt"
```

o

```bash
vidlink "a.txt" "b.txt"
```

3. Tanto las urls como las direcciones a archivos de texto se pueden combinar con el argumento -s para definir que guarde por defecto todas las url encontradas en un archivo de texto creado en la ruta que se defina:

```bash
vidlink "https://webvideo.com" "https://webvideo2.com" -s "saved_video_links.txt"
```

o

```bash
vidlink "a.txt" "b.txt" -s "saved_video_links.txt"
```

Importante: El programa no permite usar a la vez los comandos de urls y de archivos (-u --url con -f --file).

Nota: El programa intentará leer el tamaño del archivo de video y lo mostrará en consola o lo almacenará en un archivo siguiendo este formato:

```
[tamaño del archivo en megabytes] link del video
```

Nota 2: Hasta ahora los formatos de video soportados son:

- mp4,
- avi,
- mkv

# Changelog

---

v0.1.0 Initial Package State

v0.1.1 Updates to the template

v0.1.2 Cleaning code and fixing bugs

v0.1.3 Fixed bugs and new messages added

v0.1.4 Documentation, dinamic language and more bugfixes

v0.1.5 Add language support to Spanish and English, bugfixes

v0.1.6 Add new mode in the arguments to run app in silent mode (return only the founded links if -d is not setted)
