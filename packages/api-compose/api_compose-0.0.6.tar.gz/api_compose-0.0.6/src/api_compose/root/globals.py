""" Jinja Globals """
__all__ = [
    # Config
    'get_action_config_params',
    'get_action_config_body',
    'get_action_config_method',

    # Input
    'get_action_input_body',

    # Output
    'get_action_output_body',
    'get_action_output_headers',
    'get_action_output_status_code',

]

from typing import List

import jinja2
from jinja2 import Environment

from api_compose.services.common.models.text_field.templated_text_field import BaseTemplatedTextField
from api_compose.services.composition_service.models.actions.actions import ReservedExecutionId
from api_compose.services.composition_service.models.actions.filters import _get_action_attr_from_action, \
    _get_action_attr_from_actions


@jinja2.pass_context
def get_action_config_headers(context: jinja2.runtime.Context, execution_id: str):
    """
    Example Usage in Jinja: {{ config_method('execution_id') }}
    """
    templated_text_field: BaseTemplatedTextField = _get_action_attr(execution_id, context, ['config', 'headers'], '$')
    return _render_templated_text_field(context, templated_text_field=templated_text_field)

@jinja2.pass_context
def get_action_config_method(context: jinja2.runtime.Context, execution_id: str):
    """
    Example Usage in Jinja: {{ config_method('execution_id') }}
    """
    templated_text_field: BaseTemplatedTextField = _get_action_attr(execution_id, context, ['config', 'method'], '$')
    return _render_templated_text_field(context, templated_text_field=templated_text_field)


@jinja2.pass_context
def get_action_config_params(context: jinja2.runtime.Context, execution_id: str):
    """
    Example Usage in Jinja: {{ config_params('execution_id') }}
    """
    templated_text_field: BaseTemplatedTextField = _get_action_attr(execution_id, context, ['config', 'params'], '$')
    return _render_templated_text_field(context, templated_text_field=templated_text_field)


@jinja2.pass_context
def get_action_config_body(context: jinja2.runtime.Context, execution_id: str):
    """
    Example Usage in Jinja: {{ config('execution_id') }}
    """
    templated_text_field: BaseTemplatedTextField = _get_action_attr(execution_id, context, ['config', 'body'], '$')
    return _render_templated_text_field(context, templated_text_field=templated_text_field)


@jinja2.pass_context
def get_action_input_url(context: jinja2.runtime.Context, execution_id: str):
    """
    Example Usage in Jinja: {{ input_body('execution_id', '$.some_field') }}
    """
    return _get_action_attr(execution_id, context, ['input', 'url'], '$')


@jinja2.pass_context
def get_action_input_body(context: jinja2.runtime.Context, execution_id: str, json_path: str):
    """
    Example Usage in Jinja: {{ input_body('execution_id', '$.some_field') }}
    """
    return _get_action_attr(execution_id, context, ['input', 'body'], json_path)


@jinja2.pass_context
def get_action_output_body(context: jinja2.runtime.Context, execution_id: str, json_path: str):
    """
    Example Usage in Jinja: {{ output_body('execution_id', '$.some_field') }}
    """
    return _get_action_attr(execution_id, context, ['output', 'body'], json_path)


@jinja2.pass_context
def get_action_output_headers(context: jinja2.runtime.Context, execution_id: str, json_path: str):
    """
    Example Usage in Jinja: {{ output_headers('execution_id', '$.some_field') }}
    """
    return _get_action_attr(execution_id, context, ['output', 'headers'], json_path)


@jinja2.pass_context
def get_action_output_status_code(context: jinja2.runtime.Context, execution_id: str):
    """
    Example Usage in Jinja: {{ output_status_code('execution_id', '$.some_field') }}
    """
    return _get_action_attr(execution_id, context, ['output', 'status_code'])


def _get_action_attr(
        execution_id: str,
        context: jinja2.runtime.Context,
        action_attrs: List[str],
        json_path: str = ""
):
    if execution_id == ReservedExecutionId.Self.value:
        return _get_action_attr_from_action(
            dict(context).get('current_action_model'),
            action_attrs,
            json_path
        )
    else:
        return _get_action_attr_from_actions(
            execution_id,
            dict(context).get('action_models'),
            action_attrs,
            json_path
        )


def _render_templated_text_field(
        context: jinja2.runtime.Context,
        templated_text_field: BaseTemplatedTextField,
):
    """
    Example Usage in Jinja: {{ templated_text_field(config_xxxxxx('exeuction_id')) }}
    """
    # Context has all the global functions already
    str_ = Environment().from_string(templated_text_field.template).render(context)
    return templated_text_field.serde.deserialise(str_)
