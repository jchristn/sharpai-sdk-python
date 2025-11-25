from datetime import datetime, timezone

from pydantic import BaseModel, ConfigDict, Field


class TimestampModel(BaseModel):
    """
    Represents a timestamp.
    """

    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), alias="Timestamp"
    )
    model_config = ConfigDict(populate_by_name=True)
