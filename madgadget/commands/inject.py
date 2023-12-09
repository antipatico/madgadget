import sys
from pathlib import Path

from ..android.AndroidPatcher import AndroidPatcher
from ..FridaGithub import GithubNotReachableError
from ..FridaScript import FridaScript
from ..GadgetManager import GadgetManager


def inject(apk: Path, script_path: Path, output: Path):
    script = FridaScript(script_path)
    gm = GadgetManager()
    try:
        if gm.needs_update():
            print(
                f"Downloading latest version of Frida Gadgets (v{gm.latest_github_version()})"
            )
            gm.download_latest()
    except GithubNotReachableError:
        if gm.latest_version() is None:
            print(f"ERROR: cannot reach Github to download frida gadgets.")
            sys.exit(1)
        else:
            print(f"WARNING: cannot reach Github to check for frida upgrades.")

    patcher = AndroidPatcher(apk)
    patcher.unpack()

    arch_patched = 0
    for arch in patcher.archs():
        patcher.patch_arch(arch, gm.gadget_for_arch(arch), script)
        script.new_name()
        arch_patched += 1

    if arch_patched == 0:
        print(f"ERROR: cannot find any native library in the given APK, aborting.")
        sys.exit(1)

    patcher.build(output)
