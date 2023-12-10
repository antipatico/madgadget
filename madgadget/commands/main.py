import argparse
from pathlib import Path

from ..version import __version__
from .inject import inject_cli, inject_parser
from .pull import pull_cli, pull_parser


def main():
    parser = argparse.ArgumentParser(
        "madgadget",
        description="Embed frida gadgets into android multiarch applications",
        epilog="Author: Jacopo (antipatico) Scannella",
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s v{__version__}"
    )

    sub_parsers = parser.add_subparsers(
        help="Desired action", dest="action", required=True
    )

    # Add subcommands
    parser_pull = sub_parsers.add_parser(
        "pull", help="Pull a (split) package from a connected device"
    )
    parser_inject = sub_parsers.add_parser(
        "inject", help="Inject frida-gadget inside a locally-stored package"
    )

    # Add flags to command parsers
    inject_parser(parser_inject)
    pull_parser(parser_pull)

    args = parser.parse_args()

    if args.action == "inject":
        inject_cli(args)
    elif args.action == "pull":
        pull_cli(args)


if __name__ == "__main__":
    main()
