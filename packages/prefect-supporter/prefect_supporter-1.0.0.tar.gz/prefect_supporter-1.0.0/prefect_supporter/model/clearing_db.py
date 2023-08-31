from datetime import datetime

import pydantic
from prefect.server.schemas.states import StateType


class FlowRunClearing(pydantic.BaseModel):
    api_url: str = "http://localhost:4200/api"
    state_list: list[StateType] = [StateType.COMPLETED]
    before_dt: datetime
    after_dt: datetime
