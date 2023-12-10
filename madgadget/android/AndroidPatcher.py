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
    def __init__(self, apk_path: Path, tool) -> None:
        self.apk_path = apk_path
        self.tool = tool
        self.tempdir = TemporaryDirectory(suffix=".madgadget")
        self.libs_path = Path(self.tempdir.name) / tool.libs_path()
        self.manifest_path = Path(self.tempdir.name) / "AndroidManifest.xml"

    def unpack(self):
        self.tool.unpack(self.apk_path, Path(self.tempdir.name))

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
        # TODO: graph of dependencies, select the most top level one
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
        self.tool.build(Path(self.tempdir.name), output_path)
