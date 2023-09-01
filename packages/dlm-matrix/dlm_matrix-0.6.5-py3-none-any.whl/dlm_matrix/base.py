from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Type, Union, Set
from dlm_matrix.models import (
    Content,
    Chain,
    Metadata,
    Message,
    User,
    Assistant,
    System,
    UserChain,
    AssistantChain,
    SystemChain,
)
from dlm_matrix.transformation.coordinate import Coordinate
from pydantic import BaseModel, root_validator, Field
import uuid
import time

Data = Union[Dict[str, Any], List[Dict[str, Any]]]


class BaseMessage(BaseModel):
    """Message object."""

    content: str
    additional_kwargs: dict = Field(default_factory=dict)

    @property
    @abstractmethod
    def type(self) -> str:
        """Type of the message, used for serialization."""


class Generation(BaseModel):
    """Output of a single generation."""

    text: str
    """Generated text output."""

    generation_info: Optional[Dict[str, Any]] = None
    """Raw generation info response from the provider"""
    """May include things like reason for finishing (e.g. in OpenAI)"""
    # TODO: add log probs


class ChatGeneration(Generation):
    """Output of a single generation."""

    text = ""
    message: Chain

    @root_validator
    def set_text(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        values["text"] = values["message"].content
        return values


class ChatResult(BaseModel):
    """Class that contains all relevant information for a Chat Result."""

    generations: List[ChatGeneration]
    """List of the things generated."""
    llm_output: Optional[dict] = None
    """For arbitrary LLM provider specific output."""


class LLMResult(BaseModel):
    """Class that contains all relevant information for an LLM Result."""

    generations: List[List[Generation]]
    """List of the things generated. This is List[List[]] because
    each input could have multiple generations."""
    llm_output: Optional[dict] = None
    """For arbitrary LLM provider specific output."""


class PromptValue(BaseModel, ABC):
    @abstractmethod
    def to_string(self) -> str:
        """Return prompt as string."""

    @abstractmethod
    def to_chain(self) -> List[Chain]:
        """Return prompt as messages."""


def get_buffer_string(
    messages: List[Dict[str, Any]], human_prefix: str = "Human", ai_prefix: str = "AI"
) -> str:
    """Get buffer string of messages."""
    string_messages = []
    for m in messages:
        if "role" in m and "content" in m:
            if m["role"] == "user":
                role = human_prefix
            elif m["role"] == "assistant":
                role = ai_prefix
            elif m["role"] == "system":
                role = "System"
            else:
                raise ValueError(f"Got unsupported message type: {m}")

            string_messages.append(f"{role}: {m['content']}")
        else:
            raise ValueError(f"Invalid message format: {m}")

    return "\n".join(string_messages)


class ChainBuilder(ABC):
    @abstractmethod
    def build_system_chain(self, content: Content, coordinate: Coordinate):
        pass

    @abstractmethod
    def build_assistant_chain(self, content: Content, coordinate: Coordinate):
        pass

    @abstractmethod
    def build_user_chain(self, content: Content, coordinate: Coordinate):
        pass

    def get_result(self):
        return self.chain_tree


class IChainTree(ABC):
    @abstractmethod
    def add_chain(
        self,
        chain_type: Type[Chain],
        id: str,
        content: Content,
        coordinate: Coordinate,
        metadata: Optional[Dict[str, Any]],
    ):
        pass

    @abstractmethod
    def get_chains(self):
        pass

    @abstractmethod
    def get_chain(self, id: str):
        pass

    @abstractmethod
    def get_last_chain(self):
        pass

    @abstractmethod
    def get_chains_by_type(self, chain_type: str):
        pass

    @abstractmethod
    def get_chains_by_coordinate(self, coordinate: Coordinate):
        pass

    @abstractmethod
    def remove_chain(self, id: str):
        pass

    @abstractmethod
    def update_chain(
        self,
        id: str,
        new_content: Optional[Content] = None,
        new_coordinate: Optional[Coordinate] = None,
        new_metadata: Optional[Dict[str, Any]] = None,
    ):
        pass

    def add_link(self, link: dict):
        pass


class IChainFactory(ABC):
    @abstractmethod
    def create_chain(
        self,
        chain_type: str,
        id: str,
        content: Content,
        coordinate: Coordinate,
        metadata: Optional[Dict[str, Any]],
    ) -> Chain:
        pass


def _convert_dict_to_message(message_dict: dict) -> Chain:
    role = message_dict["role"]
    content = Content(raw=message_dict["content"])
    coordinate = Coordinate(x=0, y=0, z=0, t=0)  # Use default coordinates for now

    if role == "user":
        return UserChain(id=str(uuid.uuid4()), content=content, coordinate=coordinate)
    elif role == "assistant":
        return AssistantChain(
            id=str(uuid.uuid4()), content=content, coordinate=coordinate
        )
    elif role == "system":
        return SystemChain(id=str(uuid.uuid4()), content=content, coordinate=coordinate)
    else:
        raise ValueError(f"Got unknown role {role}")


class BaseConversation(ABC):
    @abstractmethod
    def get_history(self) -> List[Chain]:
        pass


def create_system_message() -> Message:
    """
    Create a System message.

    Returns:
        Message: The System message object.
    """
    content_data = {
        "content_type": "text",
        "parts": [],
    }
    system = System()
    return Message(
        id=str(uuid.uuid4()),
        create_time=time.time(),
        content=Content(**content_data),
        author=system,
    )


def create_user_message(
    message_id: str,
    text: str,
    metadata: Optional[Metadata] = None,
    user_embeddings: List[float] = None,
) -> Message:
    """
    Create a User message.

    Args:
        message_id (str): The unique identifier for the User message.
        text (str): The content of the User message.
        metadata (Optional[Metadata]): The metadata associated with the User message. Defaults to None.

    Returns:
        Message: The User message object.
    """
    content_data = {
        "content_type": "text",
        "parts": [text],
        "embedding": user_embeddings,
    }

    user = User()
    return Message(
        id=message_id,
        create_time=time.time(),
        content=Content(**content_data),
        author=user,
        metadata=metadata,
    )


def create_assistant_message(
    text: str, assistant_embeddings: List[float] = None
) -> Message:
    """
    Create an Assistant message.

    Args:
        text (str): The generated content for the Assistant message.

    Returns:
        Message: The Assistant message object.
    """
    assistant = Assistant()
    return Message(
        id=str(uuid.uuid4()),
        create_time=time.time(),
        content=Content(
            content_type="text",
            parts=[text],
            embedding=assistant_embeddings,
        ),
        author=assistant,
        end_turn=True,
    )


class ChatMessage(Chain):
    """Type of message with arbitrary speaker."""

    role: str

    @property
    def type(self) -> str:
        """Type of the message, used for serialization."""
        return "chat"


def _get_token_ids_default_method(text: str) -> List[int]:
    try:
        from transformers import GPT2TokenizerFast
    except ImportError:
        raise ValueError(
            "Could not import transformers python package. "
            "This is needed in order to calculate get_token_ids. "
            "Please install it with `pip install transformers`."
        )
    # create a GPT-2 tokenizer instance
    tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")

    # tokenize the text using the GPT-2 tokenizer
    return tokenizer.encode(text)
