#!/usr/bin/env python3

import argparse
import json
import sys
import time

import requests

from Classes import Case

URL = "https://fup.link/api/tr/"


def _get_cities() -> list:
    r = requests.get(URL)
    data = json.loads(r.text)
    cities = [(x["name"], x["slug"]) for x in data]
    return cities


def _get_city_slug(target: str, cities: list) -> str | None:
    for city in cities:
        if target.lower() == city[0].lower():
            return city[1]


def _get_cases(city_slug: str):
    path = f"{city_slug}"
    r = requests.get(URL + path)
    return json.loads(r.text)["cases"]


def _read_cache(dir, city):
    cache = set()
    try:
        with open(f"{dir}/{city.title()}/fupdl.cache", "r") as fh:
            cache = fh.readlines()
            cache = [x.strip() for x in cache]
    except FileNotFoundError:
        print("Cache not found.")
    return set(cache)


def _write_cache(cache, dir, city):
    with open(f"{dir}/{city.title()}/fupdl.cache", "w") as fh:
        for item in cache:
            if item:
                fh.write(f"{item}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Downloader script for fup.link API. Cache file will be placed in target download directory, one cache per city"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-l",
        "--list-cities",
        action="store_true",
        help="Print available cities and exit",
    )
    group.add_argument("-c", "--city", help="Target city to download")
    parser.add_argument(
        "-d", "--dir", default="./", help="Directory for download. Default is PWD"
    )
    parser.add_argument(
        "--show-files", action="store_true", help="Will print out every file download"
    )

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

    cases = [Case(x) for x in cases]
    cache = _read_cache(args.dir, args.city)
    for case in cases:
        if case.slug in cache:
            print(f"Case {case.slug} found in cache. Ignoring")
            continue
        if args.show_files:
            print("")
        print(f"Downloading case: {case.title}")
        case.populate_files()
        case.download_case(args.dir, args.show_files)
        cache.add(case.slug)

    print("All done. Writing cache")
    _write_cache(cache, args.dir, args.city)
    print("Cache written. Exiting")


if __name__ == "__main__":
    main()
