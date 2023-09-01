# vidlink.py
import re
import sys
import argparse
from time import sleep
from requests import get, head

VERSION, TIMEOUT, RETRY_TIMEOUT, MAX_TRIES, formats = (
    "0.1.1b",
    10,
    5,
    20,
    ["mp4", "avi", "mkv"],
)
CLIENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
read_data, save_data = lambda f: open(f, "r").read().splitlines(), lambda f, d: open(
    f, "w+"
).write("\n".join(d))

def get_video_size_from_url(video_url):
    tries, response, result = 0, None, ""
    while True if MAX_TRIES == 0 else (tries < MAX_TRIES):
        tries += 1
        print(f"Try #{tries} to connect to url: {video_url}")
        try:
            response = head(
                url=video_url, headers={"User-Agent": CLIENT}, timeout=TIMEOUT
            )
            result = (
                f'[{int(response.headers["Content-Length"]) / pow(10, 6)} mb] {video_url}'
                if "Content-Length" in response.headers.keys()
                else video_url
            )
            break
        except Exception:
            print("Failed to connect to the server in that url address...")
            sleep(RETRY_TIMEOUT)
    return result

def get_links_from_url(steps, url):
    global formats
    tries, response = 0, None
    steps[0] += 1
    print(f"[{(steps[0])}/{steps[1]}] Url: {url}")
    while True if MAX_TRIES == 0 else (tries < MAX_TRIES):
        tries += 1
        print(f"Try #{tries} to connect to url: {url}")
        try:
            response = get(url=url, headers={
                           "User-Agent": CLIENT}, timeout=TIMEOUT)
            break
        except:
            print(f"Failed to connect to the server in that url address...")
            sleep(RETRY_TIMEOUT)
    if tries == MAX_TRIES:
        print(
            "The maximum number of attempts has been exceeded, cancelling the connection to the server in that url"
        )
        return []
    print(f"Searching for raw videos in {url}")
    result = set(
        re.compile(
            f'(?!.*(?:https://.*){{2}})https:\/\/.*\.(?:{"|".join(formats)})'
        ).findall(response.text)
        if response.ok
        else []
    )
    print(
        f"{str(len(result)) + ' v' if len(result) > 0 else 'No v'}ideo(s) found in {url}"
    )
    return result


def run(args: list):
    print(args)
    parser = argparse.ArgumentParser(prog="VidLink")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "url", type=str, nargs="*", action="extend", default=argparse.SUPPRESS
    )
    [
        group.add_argument(a, b, type=str, nargs="+", action="extend")
        for a, b in [("-u", "--url"), ("-f", "--file")]
    ]
    parser.add_argument("-s", "--save_file", type=str, nargs="?")
    parser.add_argument(
        "-v", "--version", action="version", version=f"%(prog)s {VERSION}"
    )
    parsed_args = None
    try:
        parsed_args = parser.parse_args(args[1:])
    except:
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
            videos_found.append(get_video_size_from_url(link))
            for link in get_links_from_url(steps, url)
        ]
        for url in parsed_args.url
    ]
    if videos_found:
        save_data(
            parsed_args.save_file, videos_found
        ) if parsed_args.save_file else print("\n".join(videos_found))
    else:
        print("No videos were found or the url(s) is/are not correct.")


if __name__ == "__main__":
    run(sys.argv)
