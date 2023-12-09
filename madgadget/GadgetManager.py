from pathlib import Path
import semver
from .FridaGithub import FridaGithub
from .FridaGadget import FridaArch, FridaGadget, FridaOS

class GadgetManager:
    def __init__(self, data_path : Path =None) -> None:
        if data_path is None:
            data_path = Path.home() / ".local" / "share" / "madgadget"
        data_path.mkdir(parents=True, exist_ok=True)
        self.data_path = data_path
        self.frida_path = self.data_path / "frida"
        self.frida_path.mkdir(parents=True, exist_ok=True)
        self.gh = FridaGithub()

    def downloaded_versions(self) -> list[semver.Version]:
        subdirs = list(filter(lambda e: e.is_dir(), self.frida_path.iterdir()))
        return [ semver.Version.parse(dir.name) for dir in subdirs ]

    def latest_version(self) -> semver.Version:
        downloaded = self.downloaded_versions()
        return max(downloaded) if len(downloaded) > 0 else None
    
    def latest_github_version(self) -> semver.Version:
        return self.gh.latest_version()

    def needs_update(self) -> bool:
        return self.latest_version() is None or self.latest_version() < self.latest_github_version()

    def download_latest(self) -> None:
        dest_dir = self.frida_path / Path(str(self.latest_github_version()))
        dest_dir.mkdir(parents=True, exist_ok=False)
        self.gh.download_latest(dest_dir)
    
    def gadget_for_arch(self, arch: FridaArch):
        return FridaGadget(arch, FridaOS.android, self.latest_version(), self.frida_path)