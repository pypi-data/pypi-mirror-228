__all__ = ['Action']

from api_compose.core.jinja.core.engine import JinjaEngine
from api_compose.core.logging import (get_logger)
from api_compose.services.common.models.text_field.templated_text_field import StringTemplatedTextField, \
    JsonTemplatedTextField
from api_compose.services.common.processors.base import BaseProcessor
from api_compose.services.common.registry.processor_registry import ProcessorRegistry, ProcessorType, \
    ProcessorCategory
from api_compose.services.composition_service.jinja.context import ActionJinjaContext
from api_compose.services.composition_service.models.actions.actions import BaseActionModel, \
    JsonHttpActionModel, \
    JsonRpcWebSocketActionModel
from api_compose.services.composition_service.models.actions.configs import JsonHttpActionConfigModel, \
    JsonRpcWebSocketActionConfigModel
from api_compose.services.composition_service.processors.adapters.base_adapter import BaseAdapter
from api_compose.services.composition_service.processors.schema_validators.base_schema_validator import \
    BaseSchemaValidator
from api_compose.services.persistence_service.processors.base_backend import BaseBackend

logger = get_logger(__name__)


@ProcessorRegistry.set(
    processor_type=ProcessorType.Builtin,
    processor_category=ProcessorCategory.Action,
    models=[
        JsonHttpActionModel(
            id='example_rest_action',
            description='Get request against http://httpbin.org/get',
            execution_id='example_rest_action',
            config=JsonHttpActionConfigModel(
                url=StringTemplatedTextField(template='http://httpbin.org/get'),
                method=StringTemplatedTextField(template='GET'),
                headers=JsonTemplatedTextField(template='{}'),
                body=JsonTemplatedTextField(template='{}'),
                params=JsonTemplatedTextField(template='{}'),
            ),
        ),
        JsonRpcWebSocketActionModel(
            id='example_websocket_action',
            description='Postman public Websocket',
            execution_id='example_websocket_action',
            config=JsonRpcWebSocketActionConfigModel(
                url=StringTemplatedTextField(template='wss://ws.postman-echo.com/raw/query-params?key=template')
            ),
        ),
    ]
)
class Action(BaseProcessor):
    """
    Action
    """

    def __init__(
            self,
            action_model: BaseActionModel,
            backend: BaseBackend,
            jinja_engine: JinjaEngine,
    ):
        super().__init__()
        self.adapter: BaseAdapter = ProcessorRegistry.create_processor_by_name(
            class_name=action_model.config.adapter_class_name,
            config={
                # **dict(action_model.config),
                **dict(action_model=action_model, jinja_engine=jinja_engine, )
            }
        )
        self.backend = backend
        self.action_model = action_model

    def start(self, jinja_context: ActionJinjaContext):
        self.adapter.start(jinja_context)

    def stop(self):
        self.adapter.stop()
        self.backend.add(self.action_model)

    def validate_schema(self):
        for schema_validator_model in self.action_model.schema_validators:
            self.schema_validator: BaseSchemaValidator = ProcessorRegistry.create_processor_by_name(
                class_name=schema_validator_model.class_name,
                config={'schema_models': self.action_model.schemas,
                        'action_output_model': self.action_model.output,
                        'schema_validator_model': schema_validator_model,
                        }
            )

            self.schema_validator.validate()

    @property
    def state(self):
        return self.action_model.state

    @property
    def execution_id(self):
        return self.action_model.execution_id
