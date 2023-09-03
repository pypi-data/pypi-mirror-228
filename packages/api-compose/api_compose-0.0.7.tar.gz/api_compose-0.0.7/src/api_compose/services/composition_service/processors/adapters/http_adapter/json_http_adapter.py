__all__ = ["JsonHttpAdapter"]

import json
from typing import Optional, Dict

from api_compose.core.logging import get_logger
from api_compose.services.common.models.text_field.templated_text_field import JsonLikeTemplatedTextField
from api_compose.services.common.registry.processor_registry import ProcessorRegistry, ProcessorType, \
    ProcessorCategory
from api_compose.services.composition_service.jinja.context import ActionJinjaContext
from api_compose.services.composition_service.models.actions.actions import JsonHttpActionInputModel, \
    JsonHttpActionOutputModel, JsonHttpActionModel
from api_compose.services.composition_service.processors.adapters.http_adapter.base_http_adapter import BaseHttpAdapter

logger = get_logger(name=__name__)


@ProcessorRegistry.set(
    processor_type=ProcessorType.Builtin,
    processor_category=ProcessorCategory.Adapter,
    models=[]
)
class JsonHttpAdapter(BaseHttpAdapter):
    """
    JSON Communication over HTTP
    """

    DEBUG_OUTPUT_BODY: str = json.dumps({BaseHttpAdapter.OUTPUT_BODY_KEY: 'This is a debug response'})
    ERROR_OUTPUT_BODY: str = json.dumps({BaseHttpAdapter.OUTPUT_BODY_KEY: "failed to parse output"})

    def __init__(
            self,
            action_model: JsonHttpActionModel,
            *args,
            **kwargs,
    ):
        super().__init__(action_model, *args, **kwargs)
        self.body = action_model.config.body

        # values to be set
        self.input: JsonHttpActionInputModel = JsonHttpActionInputModel()
        self.output: JsonHttpActionOutputModel = JsonHttpActionOutputModel()

    def _on_start(self, jinja_context: ActionJinjaContext):
        super()._on_start(jinja_context)
        self.body_obj = self.body.render_to_text(jinja_engine=self.jinja_engine, jinja_context=self.jinja_context).deserialise_to_obj().obj

    def _set_input(self):
        self.input = JsonHttpActionInputModel(
            url=self.url_obj,
            method=self.method_obj,
            headers=self.headers_obj,
            params=self.params_obj,
            body=self.body_obj,
        )

    def _set_output(self):
        try:
            body = json.loads(self.response.text)
        except Exception as e:
            logger.error("Cannot deserialise output body to Dict \n"
                         f"{self.response.text}")
            body = {'message': self.response.text}

        self.output = JsonHttpActionOutputModel(
            url=self.response.url,
            status_code=self.response.status_code,
            headers=dict(self.response.headers),
            body=body,
        )
