import shutil
import subprocess
from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory

import lief

from ..exceptions import (
    AndroidPatchError,
    AndroidUnpackError,
    ApktoolError,
    ApktoolMissingError,
)
from ..FridaGadget import FridaArch, FridaGadget
from ..FridaScript import FridaScript


class AndroidPatcher:
    def __init__(self, apk_path: Path) -> None:
        self.apk_path = apk_path
        self.tempdir = TemporaryDirectory(suffix=".maxgadget")
        self.libs_path = Path(self.tempdir.name) / "lib"
        self.manifest_path = Path(self.tempdir.name) / "AndroidManifest.xml"

    def unpack(self):
        if not self.apk_path.is_file():
            raise AndroidUnpackError(
                f"Specified apk path is not a file: '{self.apk_path}'"
            )
        try:
            apktool_present = subprocess.run(
                ["apktool", "-version"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                stdin=subprocess.DEVNULL,
            )
            if apktool_present.returncode != 0:
                raise FileNotFoundError()
        except FileNotFoundError:
            raise ApktoolMissingError(
                f"Apktool not found, please install it from https://github.com/iBotPeaches/Apktool/"
            )
        apktool_result = subprocess.run(
            ["apktool", "d", self.apk_path, "-f", "-o", self.tempdir.name]
        )
        if apktool_result.returncode != 0:
            raise ApktoolError("Please refer to the above apktool logs")

    def archs(self) -> list[FridaArch]:
        archs = []
        if not self.libs_path.exists():
            return []
        for dir in filter(lambda d: d.is_dir(), self.libs_path.iterdir()):
            try:
                archs.append(FridaArch.from_string(dir.name))
            except ValueError:
                pass  # Would be nice to throw a warning
        return archs

    def patch_arch(self, arch: FridaArch, gadget: FridaGadget, script: FridaScript):
        if arch != gadget.arch:
            raise AndroidPatchError(
                f"Gadget architecture and target architecture do not match: '{arch.value}' != '{gadget.arch.value}'"
            )

        if not script.path.is_file():
            raise AndroidPatchError(
                f"Frida script file not found: '{script.path.absolute()}'"
            )

        target_path = self.libs_path / arch.value

        if not target_path.is_dir():
            raise AndroidPatchError(f"Cannot patch invalid arch libs: {arch.value}")

        target_libs = filter(
            lambda f: f.is_file() and f.name.endswith(".so"), target_path.iterdir()
        )
        for lib in target_libs:
            elf = lief.parse(f"{lib}")
            if elf is None:
                next
            elf.add_library(gadget.lib_name())
            elf.write(f"{lib}")
            break

        dest_gadget = Path(target_path) / gadget.lib_name()
        shutil.copyfile(gadget.path(), dest_gadget)

        gadget_config = target_path / gadget.config_name()
        with open(gadget_config, "w") as f:
            f.write(script.default_gadget_config())

        dest_script = Path(target_path) / script.name
        shutil.copyfile(script.path, dest_script)

    def build(self, output_path: Path):
        with NamedTemporaryFile() as f:
            apktool_result = subprocess.run(
                ["apktool", "b", self.tempdir.name, "-o", f.name]
            )
            if apktool_result.returncode != 0:
                raise ApktoolError("Please refer to the above apktool logs")
            zipalign_result = subprocess.run(
                ["zipalign", "-p", "4", f.name, output_path.absolute()]
            )
            if zipalign_result.returncode != 0:
                raise ApktoolError("Please refer to the above zipalign logs")
