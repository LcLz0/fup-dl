#!/usr/bin/env python3

import time

import requests

URL = "https://fup.link/api/tr/"


class File:
    def __init__(self, name, url) -> None:
        self.name = name
        self.url = url


class Case:
    def __init__(self, case) -> None:
        self.title = case["title"]
        self.slug = case["slug"]
        self.court_slug = case["courtSlug"]
        self.file_list = list()

    def populate_files(self):
        r = requests.get(f"{URL}{self.court_slug}/{self.slug}")
        r = r.json()["files"]
        for case_file in r:
            self.file_list.append(File(case_file["name"], case_file["url"]))
            time.sleep(0.2)
