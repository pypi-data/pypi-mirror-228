#!/usr/bin/env python
# -*- coding: utf-8 -*-

import click
from click.exceptions import ClickException

from arcl import __version__
from arcl.auth import (
    AUTH_ACTIONS,
    AUTH_ACTIONS_GET_TOKEN,
    AUTH_ACTIONS_LOGIN,
    AUTH_ACTIONS_LOGOUT,
    AUTH_ACTIONS_SHOW,
    ArchimedesAuth,
    get_accepted_env,
)

CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}
DEFAULT_AUTHOR_NAME = "Optimeering AS <dev@optimeering.com>"

# source for official regex for semver:
# https://semver.org/#is-there-a-suggested-regular-expression-regex-to-check-a-semver-string
SEMVER_REGEX = (
    r"(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)"
    r"(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)"
    r"(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?"
    r"(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
)


class ConfigNotFoundException(Exception):
    """Exception to raise when config not in config path"""


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    """
    Welcome to The Archimedes CLI.

    \b
    Commands:
        arcl auth        Handle Archimedes authentication
        arcl version     Print the version number
    """


@cli.command(hidden=True)
@click.argument(
    "action", type=click.Choice(AUTH_ACTIONS, case_sensitive=False), required=True
)
@click.argument("organization", required=False)
@click.option(
    "--env",
    type=click.STRING,
    required=False,
    default="prod",
    help="Environment to setup",
)
def auth(action, organization, env):
    """Method for handling auth operations"""
    accepted_env = get_accepted_env()
    if env not in accepted_env:
        raise ClickException(f"env should be one of {accepted_env}")

    archimedes_auth = ArchimedesAuth(env)

    if action.lower() == AUTH_ACTIONS_LOGOUT:
        archimedes_auth.logout()
        return

    if action.lower() == AUTH_ACTIONS_LOGIN:
        archimedes_auth.login(organization)
        return

    if action.lower() == AUTH_ACTIONS_GET_TOKEN:
        click.echo(archimedes_auth.get_access_token())

    if action.lower() == AUTH_ACTIONS_SHOW:
        click.echo(archimedes_auth.show())


@cli.command(hidden=True)
def version():
    """
    Print the current version
    """
    click.echo(__version__)


if __name__ == "__main__":
    cli()
