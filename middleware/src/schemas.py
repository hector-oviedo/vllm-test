from typing import List, Optional, Union, Dict, Any, Literal
from pydantic import BaseModel, Field, validator

# --- Unified Request Object: Anatomy of an Inference Call ---

class FunctionDefinition(BaseModel):
    name: str
    description: Optional[str] = None
    parameters: Dict[str, Any]
    strict: Optional[bool] = False  # Unified Protocol 5.1

class Tool(BaseModel):
    type: Literal["function"]
    function: FunctionDefinition

class ContentPart(BaseModel):
    type: Literal["text", "image_url"]
    text: Optional[str] = None
    image_url: Optional[Dict[str, str]] = None

class Message(BaseModel):
    role: Literal["system", "user", "assistant", "tool"]
    content: Union[str, List[ContentPart]]
    name: Optional[str] = None
    tool_call_id: Optional[str] = None
    tool_calls: Optional[List[Dict[str, Any]]] = None
    # Prefix completion support (DeepSeek feature)
    prefix: Optional[bool] = False 

class ThinkingConfig(BaseModel):
    """Protocol 3.3: The 'Thinking' Protocol"""
    type: Literal["enabled", "disabled"] = "disabled"
    budget_tokens: Optional[int] = Field(None, description="Optional limit on thought length")

class ResponseFormat(BaseModel):
    type: Literal["text", "json_object", "json_schema"]
    json_schema: Optional[Dict[str, Any]] = None

class ChatCompletionRequest(BaseModel):
    # Core (Mandatory)
    model: str
    messages: List[Message]
    stream: Optional[bool] = False

    # Config (Optional)
    temperature: Optional[float] = 1.0
    top_p: Optional[float] = 1.0
    # Protocol 3.2: max_completion_tokens vs max_tokens
    max_completion_tokens: Optional[int] = None
    max_tokens: Optional[int] = Field(None, description="Deprecated alias for max_completion_tokens")
    stop: Optional[Union[str, List[str]]] = None
    seed: Optional[int] = None
    logit_bias: Optional[Dict[str, float]] = None

    # Advanced (Capability)
    tools: Optional[List[Tool]] = None
    tool_choice: Optional[Union[str, Dict[str, Any]]] = None
    # Protocol 3.3: Thinking
    thinking: Optional[ThinkingConfig] = None
    response_format: Optional[ResponseFormat] = None

    # Anthropic Compatibility: Top-level system
    system: Optional[str] = None

    @validator("messages", pre=True)
    def handle_system_message(cls, v, values):
        """
        Protocol 3.1.1: Support top-level system parameter.
        If 'system' is present at top-level, prepend it to messages.
        Note: This validator runs BEFORE field validation, but 'system' field 
        might not be available in 'values' yet if validation order matters.
        Better handled in the API logic or using a root_validator.
        """
        return v

    @validator("max_completion_tokens", pre=True, always=True)
    def alias_max_tokens(cls, v, values):
        """Protocol 3.2: Alias max_tokens to max_completion_tokens"""
        if v is None and values.get("max_tokens") is not None:
            return values.get("max_tokens")
        return v

class ToolExecutionRequest(BaseModel):
    name: str = Field(..., description="Name of the tool to execute")
    arguments: Dict[str, Any] = Field(..., description="Arguments for the tool")