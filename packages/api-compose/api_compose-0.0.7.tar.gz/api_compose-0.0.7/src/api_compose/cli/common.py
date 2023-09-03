from typing import Set, List

from api_compose.core.settings import GlobalSettingsModelSingleton
from api_compose.cli.session_builder.builder import build_session_from_model, build_session_from_tags
from api_compose.cli.utils.parser import parse_context
from api_compose.core.settings.settings import CliContext, CliOptions
from api_compose.root.models.session import SessionModel
from api_compose.services.common.deserialiser.deserialiser import deserialise_manifest_to_model


def build_session(
        tags: List[str],
        select: str,
        is_interactive: bool,
        ctx: List[str],
) -> SessionModel:

    GlobalSettingsModelSingleton.get().cli_options = CliOptions(
        cli_context=CliContext(**parse_context(ctx)),
        tags=set(tags),
        select=select,
        is_interactive=is_interactive
    )

    manifests_folder_path = GlobalSettingsModelSingleton.get().discovery.manifests_folder_path
    if select:
        model = deserialise_manifest_to_model(
            select,
            manifests_folder_path=manifests_folder_path,
        )
        model = build_session_from_model(model)
    else:
        # Run any specification with matching tags
        model = build_session_from_tags(
            target_tags=GlobalSettingsModelSingleton.get().cli_options.tags,
            manifests_folder_path=manifests_folder_path,
        )

    return model
