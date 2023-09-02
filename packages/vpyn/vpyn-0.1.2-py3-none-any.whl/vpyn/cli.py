from argparse import ArgumentParser, _SubParsersAction, Namespace
from dataclasses import dataclass, field
from types import ModuleType, FunctionType
from typing import Optional
from functools import singledispatchmethod, singledispatch
from pathlib import PurePath
from importlib.metadata import entry_points, EntryPoint
from abc import ABC
import vpyn as cli_root


__all__ = ["build", "cli", "no_cli"]


has_cli_attr_name = "__vpyn_has_cli"

cli_entrypoints: dict[PurePath, FunctionType] = {}


@singledispatch
def get_abs_path(object_: object) -> PurePath:
    assert False


@get_abs_path.register
def get_abs_path_of_module(module: ModuleType) -> PurePath:
    return PurePath(f".{module.__name__}".replace(".", "/"))


@get_abs_path.register
def get_abs_path_of_class_or_function(
        cls_or_function: type | FunctionType) -> PurePath:
    return PurePath(
        f".{cls_or_function.__module__}.{cls_or_function.__qualname__}"
        .replace(".", "/"))


def has_cli(function: FunctionType) -> FunctionType:
    setattr(function, has_cli_attr_name, True)
    return function


@dataclass
class ArgumentParserBuilder:

    @singledispatchmethod
    def add_subparsers(self, object_: object, subparser: _SubParsersAction):
        pass

    @add_subparsers.register
    def add_module_subparsers(self, module: ModuleType,
                              subparser: _SubParsersAction):
        for name in module.__all__:
            value = getattr(module, name)
            if not getattr(value, has_cli_attr_name, False):
                continue
            parser = subparser.add_parser(name, description=value.__doc__)


class App:
    name: str

    def __init__(self, name: str):
        self.name = name

    @has_cli
    def build(self):
        """Write objects to disk in a variety of file formats.

        Files consist of C++ source code, header files, .o object files
        (generally cross-compiled for different platforms), and interface files
        for other languages and APIs.

        Files are written into the code's __pycache__ folders. It is expected
        that if this package is packaged as a binary distribution, then the
        necessary generated files are included with the Python bytecode.

        Toolchains may need to be installed to generate certain files (when
        cross-compiling in particular). If your local machine does not have the
        necessary toolchains installed, you can use the 'shell' command to log
        into a dev machine with a number of pre-installed toolchains for
        multiple platforms.

        """
        print("BUILD")

    @has_cli
    def up(self):
        """Deploy resources to a staging deployment."""

    @has_cli
    def down(self):
        """Tear down the staging deployment."""

    @has_cli
    def release(self):
        """Deploy resources to production."""

    @has_cli
    def shell(self):
        """Open a shell on another machine."""

    @has_cli
    def logs(self):
        """Deploy resources through a permanant deployment."""

    @has_cli
    def login(self):
        """Login to the webservice through a browser link.

        Temporary authentication tokens are stored in the user's home
        directory.

        Access keys which don't expire can also be generated. These are a
        better choice for providing access to servers, CI/CD pipelines etc.
        where the access key can be stored more securely.

        """

    @has_cli
    def logout(self):
        """Log out of the webservice.

        Locally stored authentication tokens are invalidated and deleted to prevent
        further use.

        """

    @has_cli
    def info(self):
        """Display information about the project."""

    @has_cli
    def admin(self):
        """Run an administration task."""

    def get_cli_argument_parser(self) -> ArgumentParser:
        argument_parser = ArgumentParser(description="""

vpyn operates on packages at the highest level. Every module of the package
is imported to collect its vpyn components. The package can be specified with
the -m option on the CLI. If it is not specified, it is automatically inferred
from the pyproject.toml found from the current working directory or its parent
directories.

""")

        cls = type(self)
        cli_subparsers = argument_parser.add_subparsers(dest="/", required=True)
        for name, value in cls.__dict__.items():
            if not getattr(value, has_cli_attr_name, False):
                assert name != "run"
                continue
            cli_subparsers.add_parser(
                name=name,
                description=value.__doc__)

        return argument_parser

    def cli(self, *, parsed_args: Optional[Namespace] = None):
        if parsed_args is None:
            argument_parser = self.get_cli_argument_parser()
            parsed_args = argument_parser.parse_args()

        arg = getattr(parsed_args, "/")
        entrypoint = getattr(self, arg)
        entrypoint()


def cli():
    App("vpyn").cli()


def run_app():
    """Run the flask app on localhost."""
    ...
