import traceback
from typing import Dict, Optional
from unittest.mock import Mock

import requests
from requests import Response

from api_compose.core.logging import get_logger
from api_compose.services.common.models.text_field.templated_text_field import StringTemplatedTextField, \
    JsonLikeTemplatedTextField
from api_compose.services.common.registry.processor_registry import ProcessorRegistry, ProcessorType, ProcessorCategory
from api_compose.services.composition_service.events.action import ActionEvent, ActionData
from api_compose.services.composition_service.jinja.context import ActionJinjaContext
from api_compose.services.composition_service.models.actions.actions import BaseHttpActionModel
from api_compose.services.composition_service.models.actions.states import ActionStateEnum
from api_compose.services.composition_service.models.protocols.status_enums import HttpResponseStatusEnum, \
    OtherResponseStatusEnum
from api_compose.services.composition_service.processors.adapters.base_adapter import BaseAdapter

logger = get_logger(__name__)


@ProcessorRegistry.set(
    processor_type=ProcessorType.Builtin,
    processor_category=ProcessorCategory.Adapter,
    models=[]
)
class BaseHttpAdapter(BaseAdapter):
    """
    Communication over HTTP
    """

    def __init__(
            self,
            action_model: BaseHttpActionModel,
            *args,
            **kwargs,
    ):
        super().__init__(action_model, *args, **kwargs)
        self.method = action_model.config.method
        self.headers = action_model.config.headers
        self.params = action_model.config.params

        self.response: Optional[Response] = None

    def _on_start(self, jinja_context: ActionJinjaContext):
        """
        Hook to preprocess config passed
        :return:
        """
        super()._on_start(jinja_context)
        self.method_obj = self.method.render_to_text(jinja_engine=self.jinja_engine, jinja_context=self.jinja_context).deserialise_to_obj().obj
        self.headers_obj = self.headers.render_to_text(jinja_engine=self.jinja_engine, jinja_context=self.jinja_context).deserialise_to_obj().obj
        self.params_obj = self.params.render_to_text(jinja_engine=self.jinja_engine, jinja_context=self.jinja_context).deserialise_to_obj().obj

    def _on_exchange(self):
        super()._on_exchange()

        logger.info(f"Action %s is communicating over HTTP" % (self.action_model.fqn), ActionEvent(
            data=ActionData(id=self.action_model.fqn, state=ActionStateEnum.RUNNING,
                            input={'url': self.url_obj,
                                   'method': self.method_obj,
                                   'headers': self.headers_obj,
                                   'params': self.params_obj,
                                   'body': self.body_obj,  # noqa - will be initialised in child class
                                   })))

        self.response = requests.request(
            method=self.method_obj,
            url=self.url_obj,
            headers=self.headers_obj,
            params=self.params_obj,
            json=self.body_obj if self.body_obj else None,  # noqa - will be initialised in child class
            # json cannot take empty dict. Must take None. Else Bad Body

            verify=False,
        )

    def _on_error(self, exception: Exception):
        super()._on_error(exception)

    def _on_end(self):
        super()._on_end()

    def _set_response_status(self):
        status_code = self.response.status_code
        try:
            self.response_status = HttpResponseStatusEnum(status_code)
        except Exception as e:
            logger.error(f"No matching status found for status code {status_code}")
            self.response_status = OtherResponseStatusEnum.NO_MATCHING_STATUS_FOUND

    def start(self, jinja_context: ActionJinjaContext):
        try:
            # Might error on_start when rendering
            self._on_start(jinja_context=jinja_context)
            # Might error on_exchange when doing network call
            self._on_exchange()
        except Exception as e:
            self._on_error(e)
            logger.error(traceback.format_exc(), ActionEvent(data=ActionData(id=self.action_model.fqn, state=ActionStateEnum.ERROR)))
        else:
            self._on_end()
        finally:
            if self.response is not None:
                # there's input, output, response_status only when response object is created
                self._set_input()
                self.action_model.input = self.input
                self._set_output()
                self.action_model.output = self.output
                self._set_response_status()
                self.action_model.response_status = self.response_status

    def stop(self):
        logger.debug("stop() in JsonHttpAdapter not implemented",
                     ActionEvent(data=ActionData(id=self.action_model.fqn)))


