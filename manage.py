#!/usr/bin/env python
import asyncio

import click

from ecg.cli import database as cli_database


@click.group()
def cli():
    pass

@cli.command()
def setup_server():
    asyncio.run(cli_database.create_user_table())
    asyncio.run(cli_database.populate_user_table())
    asyncio.run(cli_database.create_ecgs_tables())
    asyncio.run(cli_database.populate_ecgs_tables())

if __name__ == "__main__":
    cli()
