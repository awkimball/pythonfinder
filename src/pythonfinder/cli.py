#!/usr/bin/env python
# -*- coding=utf-8 -*-

import click
import crayons
import sys
from . import __version__
from .pythonfinder import Finder


# @click.group(invoke_without_command=True, context_settings=CONTEXT_SETTINGS)
@click.command()
@click.option('--find', default=False, nargs=1, help="Find a specific python version.")
@click.option('--which', default=False, nargs=1, help="Run the which commend.")
@click.option('--findall', is_flag=True, default=False, help="Find all python versions.")
# @click.version_option(prog_name=crayons.normal('pyfinder', bold=True), version=__version__)
@click.pass_context
def cli(
    ctx, find=False, findall=False
):
    if not find and not findall:
        click.echo('Please provide a command', color='red')
        sys.exit(1)
    finder = Finder()
    if find:
        
        if any([find.startswith('{0}'.format(n)) for n in range(10)]):
            found = finder.find_python_version(find.strip())
        else:
            found = finder.system_path.python_executables
        if found:
            click.echo('Found Python Version: {0}'.format(found), color='white')
            sys.exit(0)
    elif which:
        found = finder.system_path.which(find.strip())
        if found:
            click.echo('Found Executable: {0}'.format(found), color='white')
            sys.exit(0)
    else:
        # TODO: implement this
        click.echo('This is not yet implemented')
        sys.exit(0)
    sys.exit()


if __name__ == '__main__':
    cli()
