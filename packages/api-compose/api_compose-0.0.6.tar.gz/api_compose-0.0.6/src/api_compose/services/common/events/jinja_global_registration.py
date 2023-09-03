from api_compose.core.events.base import BaseData, BaseEvent, EventType


class JinjaGlobalRegistrationEvent(BaseEvent):
    event: EventType = EventType.JinjaGlobalRegistration
    # state:
    data: BaseData() = BaseData()
