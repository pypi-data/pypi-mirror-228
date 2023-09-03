from enum import Enum


class ScalingType(str, Enum):
    LINEAR_COMBINATION = "linear_combination"
    DIRECT = "direct"


class MethodType(str, Enum):
    WEIGHTED = "weighted"
    SPACING = "spacing"
    BOTH = "both"


class ContentType(str, Enum):
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    FILE = "file"
    LOCATION = "location"
    CONTACT = "contact"
    MESSAGE = "message"
    LINK = "link"
    EVENT = "event"
    DIRECTORY = "directory"
    OTHER = "other"


class ConnectionType(str, Enum):
    REPLY_TO = "REPLY_TO"
    MENTION = "MENTION"
    QUOTE = "QUOTE"
    FORWARD = "FORWARD"
    BACKWARD = "BACKWARD"
    SIMILAR_TO = "SIMILAR_TO"
    RESPONSE_TO = "RESPONSE_TO"
    QUESTION_TO = "QUESTION_TO"
    COUNTER = "COUNTER"


class ConnectionStrength(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class RoleType(str, Enum):
    USER = "user"
    CHAT = "chat"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    ADMIN = "admin"
    GUEST = "guest"
    ANONYMOUS = "anonymous"
    MODERATOR = "moderator"
    OWNER = "owner"
    DEVELOPER = "developer"
    CREATOR = "creator"


class NodeRelationship(str, Enum):
    SOURCE = "source"
    PREVIOUS = "previous"
    NEXT = "next"
    PARENT = "parent"
    CHILD = "child"


class ElementType(Enum):
    STEP = "Step"
    CHAPTER = "Chapter"
    PAGE = "Page"
    SECTION = "Section"
