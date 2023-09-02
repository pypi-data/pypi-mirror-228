# vidlink.py
import re
import sys
import argparse
from time import sleep
from requests import get, head
import locale

__version__ = "0.1.6"

STRINGS = {
    "en": {
        "TRY_CONNECT": "Try #{tries} to connect to url: {url}",
        "FAILED_CONNECTION": "Failed to connect to the server in that url address...",
        "URL_FETCH": "[{step}/{final}] Url: {url}",
        "URL_EXHAUSTED": "The maximum number of attempts has been exceeded, "
                         "cancelling the connection to the server in that url",
        "RAW_SEARCH": "Searching for raw videos in {url}",
        "VIDEO_NOT_FOUND": "No video(s) found in that url",
        "VIDEO_FOUND": "{0} video(s) found in that url",
        "APP_DESCRIPTION": 'A simple commandline app to extract all '
                           'the raw video links from a set of urls',
        "HELP": 'Displays this help message',
        "URL_HELP": "One or more urls separated by spaces (cannot be "
                    "used at the same time as the argument -f)",
        "FILE_HELP": 'The address of one or more files containing urls'
                     'separated by line jumps (cannot be used at the same '
                     'time as the argument -u)',
        "SAVE_FILE_HELP": 'Define if you want to save the links of the videos' 
                          ' found in a file (a link will be saved by line with the'
                          ' format <file size> <link>) (this is an optional argument,'
                          ' if not defined, the results will be displayed on console)',
        "SILENT_HELP": 'Run app in silent mode (return only the founded links if -d '
                       'is not setted)',
        "VERSION_HELP": 'Displays the current app version',
        "FINISHED": "Fetch finished successfully",
        "FAILED": "No videos were found or the url(s) is/are not correct"
    },
    "es": {
        "TRY_CONNECT": "Intento #{tries} para conectarse a la url: {url}",
        "FAILED_CONNECTION": "Fallo al conectarse al servidor en esa dirección url...",
        "URL_FETCH": "[{step}/{final}] Url: {url}",
        "URL_EXHAUSTED": "El número máximo de intentos ha sido excedido, "
                         "cancelando la conexión con el servidor en esa url",
        "RAW_SEARCH": "Buscando links de videos en {url}",
        "VIDEO_NOT_FOUND": "No se encontraron videos en esa url...",
        "VIDEO_FOUND": "{0} video(s) encontrado(s) en esa url...",
        "APP_DESCRIPTION": "Esta es una simple aplicación para extraer "
                           "todos los links de videos de un conjunto de urls",
        "HELP": 'Muestra este mensaje de ayuda',
        "URL_HELP": 'Una o más urls separadas por espacios (no se puede usar a '
                    'la vez que el argumento -f)',
        "FILE_HELP": 'La dirección de uno o más archivos que contengan urls '
                     'separadas por saltos de líneas  (no se puede usar a la '
                     'vez que el argumento -u)',
        "DEST_FILE_HELP": 'Define si se desea guardar los links de los videos '
                          'encontrados en un archivo (se guardará un link por '
                          'línea con el formato <tamaño del archivo> <link>) '
                          '(este es un argumento opcional, si no se define, '
                          'se mostrarán los resultados en consola)',
        "SILENT_HELP": 'Ejecuta la aplicación en modo silencio (retorna solamente'
                       ' los links encontrados si -d no ha sido asignado)',
        "VERSION_HELP": 'Muestra la versión de esta aplicación',
        "FINISHED": "Extracción terminada satisfactoriamente",
        "FAILED": "No se encontraron videos o la(s) url(s) no es/son correcta(s)"
    }
}

selected_language = STRINGS[locale.getdefaultlocale()[0][:2]]

TIMEOUT, RETRY_TIMEOUT, MAX_TRIES, formats = (
    10, 5, 20, ["mp4", "avi", "mkv"],
)
CLIENT = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
          "AppleWebKit/537.36 (KHTML, like Gecko)"
          "Chrome/114.0.0.0 Safari/537.36")


def read_data(f): open(f, "r").read().splitlines()
def save_data(f, d): open(f, "w+").write("\n".join(d))


def get_video_size_from_url(video_url, silent = False):
    tries, response, result = 0, None, ""
    while True if MAX_TRIES == 0 else (tries < MAX_TRIES):
        tries += 1
        if not silent: print(selected_language["TRY_CONNECT"].format(tries=tries, url=video_url))
        try:
            response = head(
                url=video_url, headers={"User-Agent": CLIENT}, timeout=TIMEOUT
            )
            result = (
                (f'[{int(response.headers["Content-Length"]) / pow(10, 6)}'
                    f' mb] {video_url}')
                if "Content-Length" in response.headers.keys()
                else video_url
            )
            break
        except Exception:
            if not silent: print(selected_language['FAILED_CONNECTION'])
            sleep(RETRY_TIMEOUT)
    return result


def get_links_from_url(steps, url, silent = False):
    global formats
    tries, response = 0, None
    steps[0] += 1
    if not silent: print(selected_language['URL_FETCH'].format(step=steps[0], final=steps[1], url=url))
    while True if MAX_TRIES == 0 else (tries < MAX_TRIES):
        tries += 1
        if not silent: print(selected_language["TRY_CONNECT"].format(tries=tries, url=url))
        try:
            response = get(url=url, headers={
                "User-Agent": CLIENT}, timeout=TIMEOUT)
            break
        except Exception:
            if not silent: print(selected_language['FAILED_CONNECTION'])
            sleep(RETRY_TIMEOUT)
    if tries == MAX_TRIES:
        if not silent: print(selected_language['URL_EXHAUSTED'])
        return []
    if not silent: print(selected_language['RAW_SEARCH'].format(url=url))
    result = set(
        re.compile(
            f'(?!.*(?:https://.*){{2}})https://.*\.(?:{"|".join(formats)})'
        ).findall(response.text)
        if response.ok
        else []
    )
    if not silent: print(selected_language["VIDEO_FOUND"].format(len(result)) 
          if len(result) > 0 else selected_language["VIDEO_NOT_FOUND"])
    return result


def run(args: list):
    parser = argparse.ArgumentParser(prog="VidLink", 
                                     description=selected_language["APP_DESCRIPTION"], 
                                     add_help=False)
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('-h', '--help', action='store_true', 
                       help=selected_language["HELP"])
    group.add_argument("url", type=str, nargs="*", 
                       action="extend", default=argparse.SUPPRESS)
    group.add_argument("-u", "--url", type=str, nargs="+", action="extend",
                        help=selected_language["URL_HELP"])
    group.add_argument("-f", "--file", type=str, nargs="+", action="extend",
                        help=selected_language["FILE_HELP"])
    parser.add_argument("-d", "--destination_file", type=str, nargs="?",
                        help=selected_language["DEST_FILE_HELP"])
    parser.add_argument('-s', '--silent', action="store_true", default=False,
                       help=selected_language["SILENT_HELP"])
    parser.add_argument("-v", "--version", action="version", 
                        version=f"%(prog)s {__version__}", 
                        help=selected_language["VERSION_HELP"])
    parsed_args = None
    
    try:
        parsed_args = parser.parse_args(args[1:])
    except Exception:
        sys.exit(2)
    
    if (parsed_args.file or parsed_args.url) == None:
        parser.print_help()
        sys.exit(2)
    
    if parsed_args.file:
        parsed_args.url = []
        [
            [parsed_args.url.append(url) for url in set(read_data(file))]
            for file in set(parsed_args.file)
        ]
    
    videos_found, parsed_args.url, steps = (
        [],
        set(parsed_args.url),
        [0, len(parsed_args.url)],
    )
    
    [
        [
            videos_found.append(get_video_size_from_url(link, parsed_args.silent))
            for link in get_links_from_url(steps, url, parsed_args.silent)
        ]
        for url in parsed_args.url
    ]
    
    if videos_found:
        save_data(
            parsed_args.destination_file, videos_found
        ) if parsed_args.destination_file else print("\n".join(videos_found))
        if not parsed_args.silent: print(selected_language["FINISHED"])
    else:
        if not parsed_args.silent:  print(selected_language["FAILED"])


if __name__ == "__main__":
    run(sys.argv)
