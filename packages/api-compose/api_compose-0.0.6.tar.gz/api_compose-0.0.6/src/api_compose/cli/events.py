from api_compose.core.events.base import BaseEvent, BaseData, EventType


class CliEvent(BaseEvent):
    event: EventType = EventType.CLI
    data: BaseData = BaseData()


class DiscoveryEvent(BaseEvent):
    event: EventType = EventType.Discovery
    data: BaseData = BaseData()
