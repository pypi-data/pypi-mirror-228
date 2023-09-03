from typing import List

from api_compose.core.utils.transformers import parse_json_with_jsonpath
from api_compose.core.utils.exceptions import NoMatchesFoundWithFilter
from api_compose.services.composition_service.models.actions.actions import BaseActionModel


def _get_action_attr_from_actions(
        execution_id: str,
        action_models: List[BaseActionModel],
        action_attrs: List[str],
        json_path: str = ""
):
    """

    Parameters
    ----------
    execution_id: execution id of the target action
    action_models: a list of BaseActionComponentModels
    action_output_attr: Attribute of the OutputModel
    json_path

    Returns
    -------

    """
    for action in action_models:
        if action.execution_id == execution_id:
            return _get_action_attr_from_action(action, action_attrs, json_path)
    # Nothing found
    raise NoMatchesFoundWithFilter(filter={'execution_id': execution_id}, collection=action_models)


def _get_action_attr_from_action(
        action_model: BaseActionModel,
        action_attrs: List[str],
        json_path: str = ""
):
    """

    Parameters
    ----------
    execution_id: execution id of the target action
    action_models: a list of BaseActionComponentModels
    action_output_attr: Attribute of the OutputModel
    json_path

    Returns
    -------

    """
    _var = action_model
    for action_attr in action_attrs:
        action_attr = action_attr.strip()
        _var = getattr(_var, action_attr)

    if json_path:
        return parse_json_with_jsonpath(_var, json_path)
    else:
        return _var
