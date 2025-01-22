#!/usr/bin/env python3

import os
import time

import requests

URL = "https://fup.link/api/tr/"


class File:
    def __init__(self, name, url) -> None:
        self.name = name
        self.url = url

    def download_file(self, target_dir, show_files):
        download_target = f"{target_dir}/{self.name}"
        if show_files:
            print(f"Downloading file: {self.name}")
        try:
            r = requests.get(self.url)
            r.raise_for_status()
        except requests.HTTPError as e:
            print(f"Failed to download {self.name}.")
            print(e)
            return
        with open(download_target, "wb") as fh:
            fh.write(r.content)


class Case:
    def __init__(self, case) -> None:
        self.title = case["title"]
        self.slug = case["slug"]
        self.court_slug = case["courtSlug"]
        self.court = self.title.split()[0]
        self.file_list = list()

    def populate_files(self):
        r = requests.get(f"{URL}{self.court_slug}/{self.slug}")
        time.sleep(0.2)
        r = r.json()["files"]
        for case_file in r:
            self.file_list.append(File(case_file["name"], case_file["url"]))

    def download_case(self, target_dir, show_files):
        dir_name = f"{target_dir}{self.court}/{self.slug}/"
        os.makedirs(dir_name, exist_ok=True)
        for entry in self.file_list:
            entry.download_file(dir_name, show_files)
            time.sleep(0.5)
