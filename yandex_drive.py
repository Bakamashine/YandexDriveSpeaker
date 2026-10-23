import os
from pathlib import Path
import requests

# curl -X GET --header 'Accept: application/json' --header 'Authorization: OAuth <Token>' 'https://cloud-api.yandex.net/v1/disk/resources?path=<dir>'

class YandexDrive:
    def __init__(self, dir_name: str, access_key: str):
        self.dir_name = dir_name
        self.access_key = access_key
        self.headers = {"Authorization": f"OAuth {access_key}"}
        print("Access_key: ",self.access_key)
        self.local_dir = Path("downloads")

    def parse_answer(self, answer: int):
        if answer == 1:
            self.__download_from_dir()
        elif answer == 2:
            self.__upload_to_dir()

    def __download_from_dir(self):
        self.local_dir.mkdir(exist_ok=True)

        # GET /v1/disk/resources?path=truefiles
        r = requests.get(
            "https://cloud-api.yandex.net/v1/disk/resources",
            headers={
                "Accept": "application/json",
                "Authorization": f"OAuth {self.access_key}",
            },
            params={"path": self.dir_name},
        )
        if r.status_code == 404:
            print("Directory is not found")
            return
        r.raise_for_status()

        for item in r.json()["_embedded"]["items"]:
            if item["type"] != "file":
                continue
            if self.__try_download_from_dir(item) == False:
                print(f"{self.dir_name}/{item['name']} - 500 error")

    def __try_download_from_dir(self, item):
        r = requests.get(
            "https://cloud-api.yandex.net/v1/disk/resources/download",
            headers=self.headers,
            params={"path": item["path"]},
        )
        if r.status_code >= 500:
            return False
        r.raise_for_status()
        href = r.json()["href"]

        data = requests.get(href)
        data.raise_for_status()
        (self.local_dir / item["name"]).write_bytes(data.content)
        print(f"Downloaded: {item['name']}")

    def __upload_to_dir(self):
        self.local_dir.mkdir(exist_ok=True)

        r = requests.put(
            "https://cloud-api.yandex.net/v1/disk/resources",
            headers=self.headers,
            params={"path": self.dir_name, "limit": 5000},
        )
        if r.status_code not in (201, 409):
            r.raise_for_status()

        for path in self.local_dir.iterdir():
            if not path.is_file():
                continue

            disk_path = f"{self.dir_name}/{path.name}"
            r = requests.get(
                "https://cloud-api.yandex.net/v1/disk/resources/upload",
                headers=self.headers,
                params={"path": disk_path, "overwrite": "true", "limit": 5000},
            )
            r.raise_for_status()
            href = r.json()["href"]

            requests.put(href, data=path.read_bytes()).raise_for_status()
            print(f"Загружен: {path.name}")