__all__ = ['build_session_from_model', 'build_session_from_tags']

from pathlib import Path
from typing import List, Set

from api_compose import DiscoveryEvent
from api_compose.core.logging import get_logger
from api_compose.root import SessionModel
from api_compose.root.models.scenario import ScenarioModel
from api_compose.root.models.specification import SpecificationModel
from api_compose.services.common.deserialiser.deserialiser import get_all_template_paths, deserialise_manifest_to_dict, \
    deserialise_manifest_to_model
from api_compose.services.common.models.base import BaseModel
from api_compose.services.composition_service.models.actions.actions import BaseActionModel

logger = get_logger(__name__)


def build_session_from_model(model: BaseModel,
                             ) -> SessionModel:
    """
    Build SessionModel from any given BaseModel
    Parameters
    ----------
    model
    session_ctx: Parameters to SessionModel

    Returns
    -------

    """
    default_id = 'default_id'
    default_description = 'default description'
    if isinstance(model, BaseActionModel):
        scenario_model = ScenarioModel(id=default_id, description=default_description, actions=[model])
        specification_model = SpecificationModel(id=default_id, description=default_description,
                                                 scenarios=[scenario_model])
        session_model = SessionModel(specifications=[specification_model])
    elif isinstance(model, ScenarioModel):
        specification_model = SpecificationModel(id=default_id, description=default_description, scenarios=[model])
        session_model = SessionModel(specifications=[specification_model])
    elif isinstance(model, SpecificationModel):
        session_model = SessionModel(specifications=[model])
    else:
        raise ValueError(f'Unhandled model type {type(model)}')

    return _post_process(session_model)


def build_session_from_tags(target_tags: Set[str],
                            manifests_folder_path: Path,
                            ) -> SessionModel:
    """
    Given all Specifications, filter for those with certain tags and put them in a session model

    Parameters
    ----------
    target_tags
    context

    Returns
    -------

    """
    logger.debug(f'Discovering Specifications with tags {target_tags=}', DiscoveryEvent())
    target_specifications: List[SpecificationModel] = []

    # Discovering for target Specifications
    for template_path in get_all_template_paths(manifests_folder_path):
        dict_ = deserialise_manifest_to_dict(
            template_path,
            manifests_folder_path=manifests_folder_path,
            context=None,
            is_rendering_strict=False,
        )

        model_name = dict_.get('model_name')
        tags: Set = set(dict_.get('tags', []))  # Set set() as default

        if model_name and model_name == 'SpecificationModel' and target_tags <= tags:
            logger.debug(f'added Specification at {template_path=}', DiscoveryEvent())
            specification_model: SpecificationModel = deserialise_manifest_to_model(
                # noqa - must be SpecificationModel
                template_path,
                manifests_folder_path=manifests_folder_path,
                context=None,
                json_dump=False,
                is_rendering_strict=True
            )
            target_specifications.append(specification_model)

    if len(target_specifications) == 0:
        logger.warning(f'No Session Groups Found with {target_tags=}', DiscoveryEvent())

    return _post_process(
        SessionModel(
            specifications=target_specifications
        )
    )


def _post_process(session_model: SessionModel) -> SessionModel:
    return session_model
