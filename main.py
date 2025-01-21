#!/usr/bin/env python3

import argparse
import json
import sys

import requests

URL = "https://fup.link/api/tr/"


def _get_cities() -> list:
    r = requests.get(URL)
    data = json.loads(r.text)
    cities = [(x["name"], x["slug"]) for x in data]
    return cities


    r = requests.get(URL + path)


def main():
    parser = argparse.ArgumentParser(description="Downloader script for fup.link API")
    download_or_list = parser.add_mutually_exclusive_group(required=True)
    download_or_list.add_argument(
        "-l",
        "--list-cities",
        action="store_true",
        help="Print available cities and exit",
    )
    download_or_list.add_argument("-c", "--city", help="Target city to download")
    args = parser.parse_args()

    cities = _get_cities()

    if args.list_cities:
        [print(x[0]) for x in cities]
        sys.exit(0)



if __name__ == "__main__":
    main()
