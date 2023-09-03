from typing import Callable, Dict

from api_compose.core.logging import get_logger
from api_compose.services.common.events.jinja_global_registration import JinjaGlobalRegistrationEvent

logger = get_logger(__name__)


class JinjaGlobalsRegistry:
    """
    - Use Decorator to Register Jinja Globals

    Lazy evaluation of Calculated Field.
    Only evaluate when `render()` is called
    """

    _registry: Dict[str, Callable] = {}

    @classmethod
    def set(cls, name: str):
        # Set Calculate Fields as templates

        logger.info("Registered Jinja Global %s" % (name), JinjaGlobalRegistrationEvent())

        def decorator(func: Callable):
            cls._registry[name] = func
            return func

        return decorator
