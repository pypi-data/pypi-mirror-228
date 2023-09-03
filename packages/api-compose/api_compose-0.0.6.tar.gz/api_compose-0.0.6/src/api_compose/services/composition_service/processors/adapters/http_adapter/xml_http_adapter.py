## TODO: Update XML HTTP Adapter


__all__ = ["XmlHttpAdapter"]

from typing import Optional, Dict

from lxml import etree
from lxml.etree import Element

from api_compose.core.logging import get_logger
from api_compose.services.common.models.text_field.templated_text_field import BaseTemplatedTextField
from api_compose.services.common.registry.processor_registry import ProcessorRegistry, ProcessorType, \
    ProcessorCategory
from api_compose.services.composition_service.jinja.context import ActionJinjaContext
from api_compose.services.composition_service.models.actions.actions import XmlHttpActionModel
from api_compose.services.composition_service.models.actions.inputs import XmlHttpActionInputModel
from api_compose.services.composition_service.models.actions.outputs import XmlHttpActionOutputModel
from api_compose.services.composition_service.processors.adapters.http_adapter.base_http_adapter import BaseHttpAdapter

logger = get_logger(name=__name__)


@ProcessorRegistry.set(
    processor_type=ProcessorType.Builtin,
    processor_category=ProcessorCategory.Adapter,
    models=[]
)
class XmlHttpAdapter(BaseHttpAdapter):
    """
    XML Communication over HTTP
    """

    ## FIXME
    DEBUG_OUTPUT_BODY: Element = etree.Element(BaseHttpAdapter.OUTPUT_BODY_KEY)
    ERROR_OUTPUT_BODY: Element = etree.Element(BaseHttpAdapter.OUTPUT_BODY_KEY)

    def __init__(
            self,
            action_model: XmlHttpActionModel,
            *args,
            **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.body = action_model.config.body

        # values to be set
        self.input: XmlHttpActionInputModel = XmlHttpActionInputModel()
        self.output: XmlHttpActionOutputModel = XmlHttpActionOutputModel()

    def _on_start(self, jinja_context: ActionJinjaContext):
        super()._on_start(jinja_context)
        self.body_obj = self.body.render_to_text(jinja_engine=self.jinja_engine, jinja_context=self.jinja_context).deserialise_to_obj().obj

    def _set_input(self):
        self.input = XmlHttpActionInputModel(
            url=self.url_obj,
            method=self.method_obj,
            headers=self.headers_obj,
            params=self.params_obj,
            body=self.body_obj,
        )

    def _set_output(self):
        self.output = XmlHttpActionOutputModel(
            url=self.response.url,
            status_code=self.response.status_code,
            headers=self.response.headers,
            body=self.response.text,
        )
