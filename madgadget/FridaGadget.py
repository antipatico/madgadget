import secrets
import string
from enum import Enum
from pathlib import Path

import semver


class FridaArch(Enum):
    arm = "armeabi-v7a"
    arm64 = "arm64-v8a"
    x86 = "x86"
    x86_64 = "x86_64"

    @staticmethod
    def from_string(arch_str: str):
        for arch in FridaArch:
            if arch.value == arch_str:
                return arch
        raise ValueError("Unsupported arch")


class FridaOS(Enum):
    android = "android"


class FridaGadget:
    def __init__(
        self,
        arch: FridaArch,
        os: FridaOS,
        version: semver.version.Version,
        base_path: Path,
    ):
        self.arch = arch
        self.os = os
        self.version = version
        self.base_path = base_path
        self.name = "".join(
            secrets.choice(string.ascii_letters + string.digits)
            for i in range(5 + secrets.randbelow(12))
        )

    def path(self):
        return (
            self.base_path
            / str(self.version)
            / f"frida-gadget-{self.version}-{self.os.name}-{self.arch.name}.so"
        )

    def lib_name(self):
        return f"lib{self.name}.so"

    def config_name(self):
        return f"lib{self.name}.config.so"
