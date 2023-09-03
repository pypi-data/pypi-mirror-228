import datetime
from pathlib import Path
from typing import Annotated, List, Optional

import click

from api_compose import get_logger
from api_compose.cli.commands import config
from api_compose.cli.common import build_session
from api_compose.cli.utils.yaml_dumper import dump_model_as_yaml
from api_compose.core.settings import GlobalSettingsModelSingleton
from api_compose.root import run_session_model
from api_compose.version import __version__

logger = get_logger(__name__)

import typer
from typer.core import TyperGroup as TyperGroupBase

DOCUMENTATION_URL = ""
EPILOG_TXT = f"Doc: {DOCUMENTATION_URL}"
HELP_TXT = "Declaratively Compose, Test and Report your API Calls"
COMPILED_FOLDER_PATH = GlobalSettingsModelSingleton.get().build_folder.joinpath(
    GlobalSettingsModelSingleton.get().compiled_folder
)
RUN_FOLDER_PATH = GlobalSettingsModelSingleton.get().build_folder.joinpath(
    GlobalSettingsModelSingleton.get().run_folder
)


class TyperGroup(TyperGroupBase):
    """Custom TyperGroup class."""

    def get_usage(self, ctx: click.Context) -> str:
        """Override get_usage."""
        usage = super().get_usage(ctx)
        message = (
                usage
                + f'\nVersion: {__version__}'
        )
        return message


app = typer.Typer(
    help=HELP_TXT,
    short_help=HELP_TXT,
    epilog=EPILOG_TXT,
    no_args_is_help=True,
    cls=TyperGroup
)

app.add_typer(config.app, name='cfg', help="Configuration")


@app.command(help="Print CLI Version")
def version() -> None:
    typer.echo(__version__)


@app.command(help="Scaffold a Sample Project Structure")
def scaffold(project_name: str) -> None:
    root = Path(project_name).absolute()
    if root.exists():
        raise ValueError(f'File/Folder {root} already exists!')

    root.mkdir(parents=True)
    for source in Path(__file__).parent.joinpath('scaffold').glob('**/*'):
        if source.is_file():
            relative_path = Path(*source.relative_to(Path(__file__).parent).parts[1:])
            dest = root.joinpath(relative_path)
            dest.parent.mkdir(exist_ok=True, parents=True)
            dest.write_bytes(source.read_bytes())
    typer.echo(f'Project {project_name} is created!')


@app.command(help=f"Compile and dump manifests as session to Path {COMPILED_FOLDER_PATH}")
def compile(
        select: Annotated[Optional[str], typer.Option("--select", "-s", help='Relative Path to Manifest')] = None,
        is_interactive: Annotated[bool, typer.Option("--interactive/--no-interactive", "-i/-I",
                                                     help='Start interactive shell or not')] = False,
        tags: Annotated[Optional[List[str]], typer.Option()] = None,
        ctx: Annotated[Optional[List[str]], typer.Option()] = None,
) -> None:
    """
    Compile and output model
    Usage:
    acp render --ctx key1=val1 --ctx key2=val2
    """
    session_model = build_session(
        tags=tags,
        select=select,
        is_interactive=is_interactive,
        ctx=ctx
    )

    timestamp = datetime.datetime.utcnow()
    file_path = COMPILED_FOLDER_PATH.joinpath(f'{session_model.model_name}-{timestamp}.yaml')
    dump_model_as_yaml(session_model, file_path)


@app.command(help=f"Compile, run and dump manifests as session to Path {RUN_FOLDER_PATH}")
def run(
        select: Annotated[Optional[str], typer.Option("--select", "-s", help='Relative Path to Manifest')] = None,
        is_interactive: Annotated[bool, typer.Option("--interactive/--no-interactive", "-i/-I",
                                                     help='Start interactive shell or not')] = False,
        tags: Annotated[Optional[List[str]], typer.Option()] = None,
        ctx: Annotated[Optional[List[str]], typer.Option()] = None
):
    """
    Compile, run and output model
    acp run --ctx key1=val1 --ctx key2=val2
    """
    session_model = build_session(
        tags=tags,
        select=select,
        is_interactive=is_interactive,
        ctx=ctx
    )
    timestamp = datetime.datetime.utcnow()
    session_model = run_session_model(session_model, timestamp)
    file_path = RUN_FOLDER_PATH.joinpath(f'{session_model.model_name}-{timestamp}.yaml')
    dump_model_as_yaml(session_model, file_path)
