"""
config subcommand
"""
from pathlib import Path

import typer

from api_compose import GlobalSettingsModelSingleton
from api_compose.cli.utils.yaml_dumper import dump_model_as_yaml

app = typer.Typer(
    help="Configure your programme",
    no_args_is_help=True
)


@app.command(help="Initialise Configuration File")
def init() -> None:
    """
    generate a config file

    :return:
    """
    config_file = Path('config.yaml')
    if config_file.exists():
        typer.echo(f'Config File {config_file.absolute()} already exists! Aborted')
    else:
        # Get config
        dump_model_as_yaml(GlobalSettingsModelSingleton.get(), config_file)
        typer.echo(f'Config File {config_file.absolute()} is created')