#!/usr/bin/env python
import click
import asyncio

from ecg.cli import database as cli_database


@click.group()
def cli():
    pass

@cli.command()
def setup_server():
    asyncio.run(cli_database.create_user_table())
    asyncio.run(cli_database.populate_user_table())

if __name__ == "__main__":
    cli()
