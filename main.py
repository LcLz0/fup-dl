#!/usr/bin/env python3

import argparse
import json
import sys

import requests

URL = "https://fup.link/api/"


def _get_city_slug(city: str):
    cities = _get_cities()
    target_slug = ""
    for city in cities:



def _get_cities() -> list:
    path = "tr/"
    r = requests.get(URL + path)
    data = json.loads(r.text)
    cities = [(x["name"], x["slug"]) for x in data]
    return cities


def _get_cases(city: str) -> list:
    path = f"tr/{city}/"
    r = requests.get(URL + path)
    print(r)


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

    if args.list_cities:
        cities = _get_cities(URL)
        [print(x[0]) for x in cities]
        sys.exit(0)

    if args.city:
        print(args.city)


if __name__ == "__main__":
    main()
