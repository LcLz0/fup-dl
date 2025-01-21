#!/usr/bin/env python3

import argparse
import json
import sys
import time

import requests

URL = "https://fup.link/api/tr/"


def _get_cities() -> list:
    r = requests.get(URL)
    data = json.loads(r.text)
    cities = [(x["name"], x["slug"]) for x in data]
    return cities


def _get_city_slug(target: str, cities: list) -> str:
    for city in cities:
        if target.lower() == city[0].lower():
            return city[1]


def _get_cases(city_slug: str):
    path = f"{city_slug}"
    r = requests.get(URL + path)
    return json.loads(r.text)["cases"]


def main():
    parser = argparse.ArgumentParser(
        description="Downloader script for fup.link API. Cache file will be placed in target download directory"
    )
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
    time.sleep(0.3)

    if args.list_cities:
        [print(x[0]) for x in cities]
        sys.exit(0)

    target_city = _get_city_slug(args.city, cities)
    if target_city is None:
        print(f"City {args.city} not found. Exiting")
        sys.exit(1)

    cases = _get_cases(target_city)
    time.sleep(0.3)


if __name__ == "__main__":
    main()
