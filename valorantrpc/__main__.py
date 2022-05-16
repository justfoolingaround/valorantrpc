import click

from .cli.commands.run import click_run
from .cli.__core__ import __version__


@click.group(commands={"run": click_run})
@click.version_option(__version__, "-v", "--version")
def valorant_rpc():
    pass


if __name__ == "__main__":
    valorant_rpc()
