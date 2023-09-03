import uuid
from typing import List

from api_compose.root.models.specification import SpecificationModel
from api_compose.services.common.models.base import BaseModel


class SessionModel(BaseModel):
    id: str = str(uuid.uuid4()) # ensures uniquenes of session when action is saved to database
    description: str = ''
    specifications: List[SpecificationModel]