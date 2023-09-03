from api_compose.core.logging import get_logger
from api_compose.services.common.registry.jinja_globals_registry import JinjaGlobalsRegistry

logger = get_logger(name=__name__)


@JinjaGlobalsRegistry.set(name='get_one')
def return_value_one() -> int:
    return 1

