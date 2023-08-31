# -*- coding: utf-8 -*-

import importlib.metadata
import click
from .converter import convert


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return

    app_version = importlib.metadata.version("oaspy")
    click.echo(f"oaspy {app_version}")

    ctx.exit()


@click.command(
    context_settings={
        "ignore_unknown_options": False,
    }
)
@click.option(
    "-f",
    "--file",
    default=None,
    required=True,
    type=click.Path(exists=True, readable=True),
    help="file to import.",
)
@click.option("-s", "--schema", default="v30", required=False, help="OpenApi definition to be generated")
@click.option("-o", "--output", default=None, required=False, help="file name to save.")
@click.option(
    "-v",
    "--version",
    is_flag=True,
    expose_value=False,
    is_eager=True,
    callback=print_version,
    help="show current version and exit.",
)
def command_line(file, schema, output):
    click.clear()
    convert(file, schema, output)


if __name__ == "__main__":
    command_line()
