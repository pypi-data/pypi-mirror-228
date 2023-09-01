# VidLink

Last updated 31th August 2023

This is a simple commandline app to extract all the raw video links from a set of urls

More information [Click Here](##Introduction)

# Use

## In english

```bash
usage: VidLink [-h] [-u URL [URL ...]] [-f FILE [FILE ...]] [-s [SAVE_FILE]] [-v] [url ...]

positional arguments:
  url

options:
  -h, --help show this help message and exit
  -u URL [URL ...], --url URL [URL ...] One or more urls separated by spaces (cannot be used at the same time as the argument -f)
  -f FILE [FILE ...], --file FILE [FILE ...] The address of one or more files containing urls separated by line jumps (cannot be used at the same time as the argument -u)
  -s [SAVE_FILE], --save_file [SAVE_FILE] Define if you want to save the links of the videos found in a file (a link will be saved by line with the format <file size> <link>) (this is an optional argument, if not defined, the results will be displayed on console)
  -v, --version show program's version number and exit
```

## In spanish

```bash
uso: VidLink [-h] [-u URL [URL ...]] [-f FILE [FILE ...]] [-s [SAVE_FILE]] [-v] [url ...]

argumentos posicionales:
  url

opciones:
  -h, --help Muestra la ayuda
  -u URL [URL ...], --url URL [URL ...] Una o más urls separadas por espacios (no se puede usar a la vez que el argumento -f)
  -f FILE [FILE ...], --file FILE [FILE ...] La dirección de uno o más archivos que contengan urls separadas por saltos de líneas  (no se puede usar a la vez que el argumento -u)
  -s [SAVE_FILE], --save_file [SAVE_FILE] Define si se desea guardar los links de los videos encontrados en un archivo (se guardará un link por línea con el formato <tamaño del archivo> <link>) (este es un argumento opcional, si no se define, se mostrarán los resultados en consola)
  -v, --version Muestra la versión del programa
```

# Changelog

v0.1.0 Initial Package State

v0.1.1 Updates to the template

v0.1.2 Cleaning code and fixing bugs

v0.1.3 Fixed bugs and new messages added

v0.1.4 Documentation, dinamic language and more bug fixes
