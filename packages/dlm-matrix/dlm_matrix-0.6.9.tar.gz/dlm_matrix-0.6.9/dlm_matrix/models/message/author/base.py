from pydantic import BaseModel
from typing import Dict, Any, Optional
from pydantic.fields import Field
from dlm_matrix.type import RoleType


class Author(BaseModel):
    """
    Represents an author in the conversation.
    """

    role: RoleType = Field(..., description="The role of the author.")
    id: Optional[str] = Field(None, description="The ID of the author.")

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "role": "user",
                "id": "123456789",
            }
        }


class User(Author):
    """Represents a user."""

    role = RoleType.USER


class Chat(Author):
    """Represents a chat."""

    role = RoleType.CHAT


class Assistant(Author):
    """Represents an assistant."""

    role = RoleType.ASSISTANT


class System(Author):
    """Represents a system."""

    role = RoleType.SYSTEM
