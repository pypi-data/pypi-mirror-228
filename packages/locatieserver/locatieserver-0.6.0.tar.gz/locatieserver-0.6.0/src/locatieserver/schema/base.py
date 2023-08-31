from pydantic import BaseModel
from pydantic import ConfigDict


class LocatieserverBaseModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    """BaseModel replacement for sharing the configuration across the different schemas."""
