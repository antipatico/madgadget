import argparse
from pathlib import Path

from .inject import inject
from .pull import pull


def main():
    parser = argparse.ArgumentParser(
        "madgadget",
        description="Embed frida gadgets into android multiarch applications",
        epilog="Author: Jacopo (antipatico) Scannella",
    )

    sub_parsers = parser.add_subparsers(
        help="Desired action", dest="action", required=True
    )

    # create the parser for the "pull" command
    parser_pull = sub_parsers.add_parser(
        "pull", help="Pull a (split) package from a connected device"
    )
    parser_pull.add_argument(
        "package_name",
        help="The name of the package you want to pull (E.G. com.android.settings)",
    )
    parser_pull.add_argument("-o", "--output", help="Output directory path")

    # create the parser for the "inject" command
    parser_inject = sub_parsers.add_parser(
        "inject", help="Inject frida-gadget inside a locally-stored package"
    )
    parser_inject.add_argument(
        "apk", help="Android apk you want to inject frida gadget to"
    )
    parser_inject.add_argument(
        "script", help="Frida script you want to inject, javascript only"
    )
    parser_inject.add_argument("-o", "--output", help="Output file")

    args = parser.parse_args()

    if args.action == "inject":
        apk = Path(args.apk)
        script_path = Path(args.script)
        if args.output is None:
            candidate = f"{apk}".replace(".apk", ".madgadget.apk")
            args.output = candidate if candidate != f"{apk}" else f"{apk}.madgadget"
        output = Path(args.output)
        inject(apk, script_path, output)
    elif args.action == "pull":
        pull(args.package_name, args.output)


if __name__ == "__main__":
    main()
