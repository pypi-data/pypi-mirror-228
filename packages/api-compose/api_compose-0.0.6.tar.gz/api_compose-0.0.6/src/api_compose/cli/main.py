import datetime
from typing import Annotated, List, Optional

import typer

from api_compose import get_logger
from api_compose.cli.commands import config
from api_compose.cli.common import build_session
from api_compose.cli.utils.yaml_dumper import dump_model_as_yaml
from api_compose.core.settings import GlobalSettingsModelSingleton
from api_compose.root import run_session_model
from api_compose.version import __version__

logger = get_logger(__name__)

DOCUMENTATION_URL = ""
EPILOG_TXT = f"Doc: {DOCUMENTATION_URL}"
HELP_TXT = "Declaratively Compose and Test and Report your API Calls"

app = typer.Typer(
    help=HELP_TXT,
    short_help=HELP_TXT,
    epilog=EPILOG_TXT,
    no_args_is_help=True
)

app.add_typer(config.app, name='cfg', help="Configuration")


@app.command(help="Scaffold Project Structure")
def version() -> None:
    typer.echo(__version__)


@app.command(help="Scaffold Project Structure")
def scaffold(project_name: str) -> None:
    pass


@app.command(help="Compile a template to a model")
def compile(
        select: Annotated[Optional[str], typer.Option("--select", "-s", help='Relative Path to Manifest')] = None,
        is_interactive: Annotated[bool, typer.Option("--interactive/--no-interactive", "-i/-I", help='Start interactive shell or not')] = False,
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

    compiled_folder_path = GlobalSettingsModelSingleton.get().build_folder.joinpath(
        GlobalSettingsModelSingleton.get().compiled_folder
    )
    timestamp = datetime.datetime.utcnow()
    file_path = compiled_folder_path.joinpath(f'{session_model.model_name}-{timestamp}.yaml')
    dump_model_as_yaml(session_model, file_path)


@app.command(help="Run manifests")
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
    run_folder_path = GlobalSettingsModelSingleton.get().build_folder.joinpath(
        GlobalSettingsModelSingleton.get().run_folder
    )
    timestamp = datetime.datetime.utcnow()
    session_model = run_session_model(session_model, timestamp)
    file_path = run_folder_path.joinpath(f'{session_model.model_name}-{timestamp}.yaml')
    dump_model_as_yaml(session_model, file_path)
