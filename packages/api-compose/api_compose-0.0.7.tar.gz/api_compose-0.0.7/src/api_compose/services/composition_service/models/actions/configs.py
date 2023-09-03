from __future__ import annotations

from lxml import etree
from lxml.builder import E
from pydantic import BaseModel as _BaseModel, Field

from api_compose.services.common.models.text_field.templated_text_field import StringTemplatedTextField, \
    JsonLikeTemplatedTextField, \
    JsonTemplatedTextField, XmlTemplatedTextField


class BaseActionConfigModel(_BaseModel, extra='allow'):
    adapter_class_name: str = Field(
        'BaseAdapter',
        description='Adapter Controller Name',
    )

    url: StringTemplatedTextField = Field(
        StringTemplatedTextField(template=''),
        description='Templateable URL',
    )


class BaseHttpActionConfigModel(BaseActionConfigModel):
    adapter_class_name: str = Field(
        'BaseHttpAdapter',
        description=BaseActionConfigModel.model_fields['adapter_class_name'].description,
    )
    method: StringTemplatedTextField = Field(
        StringTemplatedTextField(template='GET'),
        description='Templateable HTTP Method',
    )
    headers: JsonLikeTemplatedTextField = Field(
        JsonTemplatedTextField(template="{}"),
        description='Templateable HTTP Headers',
    )
    params: JsonLikeTemplatedTextField = Field(
        JsonTemplatedTextField(template="{}"),
        description='Templateable HTTP Params',
    )


class JsonHttpActionConfigModel(BaseHttpActionConfigModel):
    adapter_class_name: str = Field(
        'JsonHttpAdapter',
        description=BaseActionConfigModel.model_fields['adapter_class_name'].description,
    )
    body: JsonLikeTemplatedTextField = Field(
        JsonTemplatedTextField(template="{}"),
        description='Templateable HTTP body',
    )


class XmlHttpActionConfigModel(BaseHttpActionConfigModel):
    adapter_class_name: str = Field(
        'XmlHttpAdapter',
        description=BaseActionConfigModel.model_fields['adapter_class_name'].description,
    )
    body: XmlTemplatedTextField = Field(
        XmlTemplatedTextField(template=etree.tostring(E.default())),
        description='Templateable HTTP body',
    )


class JsonRpcWebSocketActionConfigModel(BaseHttpActionConfigModel):
    pass
