# Inspired by Objection
import lzma
import requests
from functools import lru_cache
import semver
from .exceptions import GithubNotReachableError
from pathlib import Path


class FridaGithub:
    _instance = None
    GITHUB_LATEST_RELEASE = "https://api.github.com/repos/frida/frida/releases/latest"

    @staticmethod
    @lru_cache(maxsize=100)
    def latest_release() -> dict:
        res = requests.get(FridaGithub.GITHUB_LATEST_RELEASE)
        if res.status_code != 200:
            raise GithubNotReachableError(
                f"Github not reachable, returned 'HTTP {res.status_code}"
            )
        return res.json()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def latest_version(self) -> semver.Version:
        return semver.Version.parse(self.latest_release()["tag_name"])

    def download_latest(self, output_path: Path) -> None:
        if not output_path.is_dir():
            raise ValueError("output_dir must be a directory")

        assets = self.latest_release().get("assets", [])
        assets = list(filter(lambda a: "gadget" in a.get("name", ""), assets))
        # this is in place as long as we support only android
        assets = list(filter(lambda a: "android" in a.get("name", ""), assets))
        for gadget_asset in assets:
            download_url = gadget_asset["browser_download_url"]
            file_name = gadget_asset["name"][:-3]
            res = requests.get(download_url, stream=True)
            if res.status_code != 200:
                raise GithubNotReachableError(
                    f"Cannot download asset, Github returned 'HTTP {res.status_code}"
                )
            with open(output_path / file_name, "wb") as f:
                f.write(lzma.decompress(res.content))
