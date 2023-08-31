from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import uuid4


class ObjectBaseModel(BaseModel):
    """
    ObjectBaseModel serves as the base class for other models.
    It includes common fields that are generally useful for a variety of data models.
    """

    # The date and time when the object was created.
    # It is Optional and by default, the current datetime will be used.
    date_created: Optional[datetime] = Field(default_factory=datetime.now)

    # The date and time when the object was last edited.
    # It is Optional and by default, the current datetime will be used.
    date_last_edit: Optional[datetime] = Field(default_factory=datetime.now)

    # A unique identifier (UUID) for the object, converted to a hexadecimal string.
    # It is Optional, and by default, a unique hex string will be generated.
    slug: Optional[str] = uuid4().hex

    # An integer ID for the object.
    # It is Optional and defaults to None, which allows the database to auto-generate it.
    id: Optional[int] = None
