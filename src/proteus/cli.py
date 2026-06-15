# ruff: noqa: T201
"""
Command Line Interface (CLI) for Proteus.

This module provides the 'proteus' command entry point, allowing users
to interact with configurations directly from the terminal.

Design: Stateless, following the Unix philosophy.
"""

import argparse
import json
import sys
from typing import Any, Callable, List, Optional

from . import __version__
from .core import ConfigurationManager
from .exceptions import ConfigurationError


def main(args: Optional[List[str]] = None) -> None:
    """
    Main entry point for the Proteus CLI.

    Args:
        args: Optional list of command-line arguments. Defaults to sys.argv[1:].
    """
    parser = argparse.ArgumentParser(
        prog="proteus",
        description="Proteus: Unified configuration management and translation.",
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # ------------------------------------------------------------------ #
    # Command: get                                                       #
    # ------------------------------------------------------------------ #
    get_parser = subparsers.add_parser("get", help="Read a value from a config file")
    get_parser.add_argument("file", help="Path to the configuration file")
    get_parser.add_argument("key", help="Dot-notation path to the key")
    get_parser.add_argument(
        "--cast",
        choices=["int", "float", "bool", "str"],
        help="Cast the value to a specific type",
    )

    # ------------------------------------------------------------------ #
    # Command: set                                                       #
    # ------------------------------------------------------------------ #
    set_parser = subparsers.add_parser("set", help="Modify a value and save")
    set_parser.add_argument("file", help="Path to the configuration file")
    set_parser.add_argument("key", help="Dot-notation path to the key")
    set_parser.add_argument("value", help="The value to set")
    set_parser.add_argument(
        "--out",
        help="Optional destination file (defaults to overwriting input file)",
    )

    # ------------------------------------------------------------------ #
    # Command: merge                                                     #
    # ------------------------------------------------------------------ #
    merge_parser = subparsers.add_parser("merge", help="Merge multiple files")
    merge_parser.add_argument("files", nargs="+", help="Files to merge (in order)")
    merge_parser.add_argument(
        "--out", required=True, help="Destination path for the merged file"
    )

    # ------------------------------------------------------------------ #
    # Command: translate                                                 #
    # ------------------------------------------------------------------ #
    trans_parser = subparsers.add_parser("translate", help="Convert between formats")
    trans_parser.add_argument("input", help="Source file path")
    trans_parser.add_argument("output", help="Destination file path")

    # ------------------------------------------------------------------ #
    # Command: view                                                      #
    # ------------------------------------------------------------------ #
    view_parser = subparsers.add_parser(
        "view", help="View the merged configuration as JSON"
    )
    view_parser.add_argument("files", nargs="*", help="Files to load and view")

    # ------------------------------------------------------------------ #
    # Command: list-files                                                #
    # ------------------------------------------------------------------ #
    list_parser = subparsers.add_parser(
        "list-files", help="List absolute paths of loaded files"
    )
    list_parser.add_argument("files", nargs="*", help="Files to load and list")

    # Parse arguments
    parsed_args = parser.parse_args(args)

    if not parsed_args.command:
        parser.print_help()
        sys.exit(0)

    # Execute command
    try:
        config = ConfigurationManager()

        if parsed_args.command == "get":
            config.load(parsed_args.file)
            cast_fn: Optional[Callable[[Any], Any]] = None
            if parsed_args.cast == "int":
                cast_fn = int
            elif parsed_args.cast == "float":
                cast_fn = float
            elif parsed_args.cast == "bool":
                cast_fn = bool

            value = config.get(parsed_args.key, cast=cast_fn)
            print(value)

        elif parsed_args.command == "set":
            config.load(parsed_args.file)
            config.set(parsed_args.key, parsed_args.value)
            out_path = parsed_args.out or parsed_args.file
            config.save(out_path)
            print(
                f"Successfully updated '{parsed_args.key}' and saved to '{out_path}'."
            )

        elif parsed_args.command == "merge":
            for f in parsed_args.files:
                config.load(f)
            config.save(parsed_args.out)
            print(
                f"Successfully merged {len(parsed_args.files)} files "
                f"into '{parsed_args.out}'."
            )

        elif parsed_args.command == "translate":
            config.translate(parsed_args.input, parsed_args.output)
            print(
                f"Successfully translated '{parsed_args.input}' "
                f"to '{parsed_args.output}'."
            )

        elif parsed_args.command == "view":
            for f in parsed_args.files:
                config.load(f)
            print(json.dumps(config.get_all(), indent=2))

        elif parsed_args.command == "list-files":
            for f in parsed_args.files:
                config.load(f)
            for loaded_file in config.loaded_files():
                print(loaded_file)

        sys.exit(0)

    except (ConfigurationError, FileNotFoundError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
    except Exception as exc:
        print(f"Unexpected error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
