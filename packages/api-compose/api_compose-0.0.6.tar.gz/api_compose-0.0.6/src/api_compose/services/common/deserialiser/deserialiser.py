__all__ = ['deserialise_manifest_to_model']

from pathlib import Path
from typing import Dict, Optional, Union, List

import yaml
from jinja2 import Undefined, StrictUndefined

from api_compose.core.jinja.core.context import BaseJinjaContext
from api_compose.core.jinja.core.engine import JinjaEngine, JinjaTemplateSyntax
from api_compose.core.logging import get_logger
from api_compose.core.settings import GlobalSettingsModelSingleton
from api_compose.core.utils.transformers import overlay_dict
from api_compose.services.common.deserialiser.checks import are_files_unique_in, get_file_paths_relative_to, \
    is_folder_populated
from api_compose.services.common.deserialiser.exceptions import ManifestMissingModelNameException, \
    NonUniqueManifestNameException, ManifestNotFoundException, EmptyManifestFolderException
from api_compose.services.common.deserialiser.parser import parse_sentence
from api_compose.services.common.events.deserialisation import DeserialisationEvent
from api_compose.services.common.models.base import BaseModel
from api_compose.services.common.registry.processor_registry import ProcessorRegistry

logger = get_logger(__name__)


def deserialise_manifest_to_model_with_parser(
        manifest_file_path: str,
        manifests_folder_path: Path,
        sentence: str = '',
        json_dump=False,
        is_rendering_strict: bool = True,
) -> Optional[Union[BaseModel, str]]:
    context = parse_sentence(sentence)
    return deserialise_manifest_to_model(
        manifest_file_path=manifest_file_path,
        manifests_folder_path=manifests_folder_path,
        context=context,
        json_dump=json_dump,
        is_rendering_strict=is_rendering_strict
    )


def deserialise_manifest_to_model(
        manifest_file_path: str,
        manifests_folder_path: Path,
        context: Dict = None,
        is_rendering_strict: bool = True,
        json_dump=False,
) -> Optional[Union[BaseModel, str]]:
    """
    Given relative path to a manifest file, deserialise it to a model based on the field `model_name` in the file.

    Parameters
    ----------
    manifest_file_path: Path to Manifest relative to MANIFESTS_FOLDER_PATH
    context: user-defined additional contexts
    is_rendering_strict: When True, when context does not include the variable required by the manifest, it errors out.
    json_dump: If True, dump model as json string. Else, return Model itself

    Returns
    -------

    """
    dict_ = deserialise_manifest_to_dict(
        manifest_file_path=manifest_file_path,
        manifests_folder_path=manifests_folder_path,
        context=context,
        is_rendering_strict=is_rendering_strict
    )
    model = deserialise_dict_to_model(dict_)

    if model:
        if json_dump:
            return model.model_dump_json()
        else:
            return model
    else:
        raise ManifestMissingModelNameException(
            manifest_file_path=manifest_file_path,
            manifest_content=dict_,
            available_model_names=[
                name for name in
                ProcessorRegistry.get_model_names()]
        )


def deserialise_manifest_to_dict(
        manifest_file_path: str,
        manifests_folder_path: Path,
        context: Dict = None,
        is_rendering_strict=True,
) -> Dict:
    if context is None:
        context = {}

    # Precendence - CLI Env Var >> Manifest-specific Env Var >> .env file env var
    context_merged = overlay_dict(overlayed_dict=GlobalSettingsModelSingleton.get().env_vars, overlaying_dict=context)
    context_merged = overlay_dict(overlayed_dict=context_merged,
                                  overlaying_dict=dict(GlobalSettingsModelSingleton.get().cli_options.cli_context))

    if is_rendering_strict:
        # Letting know what context is passed is important only when rendering is strict
        logger.debug(
            f'Deserialising {manifest_file_path=} relative to {manifests_folder_path=}. \n' f'{context_merged=}',
            DeserialisationEvent())

    # Read + Render
    jinja_engine = build_compile_time_jinja_engine(manifests_folder_path, is_rendering_strict)
    id = Path(manifest_file_path).stem
    relative_manifest_path = get_manifest_relative_path(manifests_folder_path, id)

    str_, is_success, exec = jinja_engine.set_template_by_file_path(template_file_path=str(relative_manifest_path),
                                                                    can_strip=True).render_to_str(
        jinja_context=BaseJinjaContext(**context_merged))

    if not is_success:
        raise exec

    dict_ = yaml.safe_load(str_)
    if dict_.get('id'):
        logger.warning(f'Id field is already set in the file. Will be overridden by the file name {id=}',
                       DeserialisationEvent())

    dict_['id'] = id
    return dict_


def deserialise_dict_to_model(
        dict_: Dict,
) -> Optional[BaseModel]:
    model_name = dict_.get('model_name')
    if model_name:
        return ProcessorRegistry.create_model_by_name(model_name, dict_)
    else:
        return None


def get_manifest_relative_path(
        manifests_folder_path: Path,
        manifest_file_name: str,
) -> Path:
    relative_paths = get_file_paths_relative_to(manifests_folder_path, manifest_file_name)
    if len(relative_paths) == 0:
        raise ManifestNotFoundException(manifests_folder_path, manifest_file_name)
    elif len(relative_paths) > 1:
        raise NonUniqueManifestNameException(manifests_folder_path)
    else:
        return relative_paths[0]


def get_all_template_paths(manifest_folder_path: Path) -> List[str]:
    jinja_engine = build_compile_time_jinja_engine(manifests_folder_path=manifest_folder_path)
    return jinja_engine.get_available_templates()


def build_compile_time_jinja_engine(
        manifests_folder_path: Path,
        is_rendering_strict: bool = True,
) -> JinjaEngine:
    if not is_folder_populated(manifests_folder_path):
        raise EmptyManifestFolderException(manifests_folder_path)

    if not are_files_unique_in(manifests_folder_path):
        raise NonUniqueManifestNameException(manifests_folder_path)

    if is_rendering_strict:
        undefined = StrictUndefined
    else:
        undefined = Undefined

    return JinjaEngine(
        undefined=undefined,
        jinja_template_syntax=JinjaTemplateSyntax.SQUARE_BRACKETS,
        templates_search_paths=[
            manifests_folder_path,
        ],
    )
