import datetime

from api_compose.core.jinja.core.engine import JinjaEngine, JinjaTemplateSyntax
from api_compose.core.logging import get_logger
from api_compose.root.events import SessionEvent
from api_compose.root.globals import get_action_input_body, \
    get_action_output_body, get_action_output_headers, get_action_output_status_code, get_action_config_params, \
    get_action_config_body, get_action_config_method, get_action_input_url, get_action_config_headers
from api_compose.root.models.session import SessionModel
from api_compose.root.models.session import SessionModel
from api_compose.root.runner import Runner
from api_compose.services.common.registry.jinja_globals_registry import JinjaGlobalsRegistry

logger = get_logger(__name__)


def run_session_model(
        session_model: SessionModel,
        timestamp: datetime.datetime,
) -> SessionModel:
    logger.info(f'Running Session {session_model.id=}', SessionEvent())
    jinja_engine: JinjaEngine = build_runtime_jinja_engine()
    runner = Runner(session_model, jinja_engine, timestamp=timestamp)
    runner.run()
    return runner.session_model


def build_runtime_jinja_engine(
) -> JinjaEngine:
    builtin_globals = {
        # 'templated_text_field': render_templated_text_field,

        'config_headers': get_action_config_headers,
        'config_params': get_action_config_params,
        'config_body': get_action_config_body,
        'config_method': get_action_config_method,

        'input_url': get_action_input_url,
        'input_body': get_action_input_body,

        'output_body': get_action_output_body,
        'output_headers': get_action_output_headers,
        'output_status_code': get_action_output_status_code,
    }

    custom_globals = JinjaGlobalsRegistry._registry
    for name in custom_globals.keys():
        if name in builtin_globals.keys():
            raise ValueError(f'Jinja Global Name {name} is already taken! Please try another name!')

    import os
    all_globals = {**builtin_globals, **custom_globals}

    return JinjaEngine(
        globals=all_globals,
        jinja_template_syntax=JinjaTemplateSyntax.CURLY_BRACES,
    )
