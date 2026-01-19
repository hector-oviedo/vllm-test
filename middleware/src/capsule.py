from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Literal

class AdapterConfig(BaseModel):
    """Configuration for a LoRA Adapter."""
    name: str = Field(..., description="Unique identifier for the adapter")
    path: str = Field(..., description="Path to adapter weights relative to /capsules")
    alpha: int = Field(16, description="LoRA alpha parameter")
    rank: int = Field(64, description="LoRA rank")

class CapsuleSpec(BaseModel):
    base_model: str = Field(..., description="HuggingFace ID or local path")
    context_window: int = Field(32768, description="Maximum context length")
    chat_template: Optional[str] = Field(None, description="Custom Jinja2 template")
    adapters: List[AdapterConfig] = Field(default_factory=list)

class ModelCapsule(BaseModel):
    """
    MIAA Capsule Definition.
    Wraps the weights, configuration, and adapters into a single unit.
    """
    api_version: str = "v1"
    kind: Literal["Capsule"] = "Capsule"
    metadata: Dict[str, str] = Field(default_factory=dict)
    
    spec: CapsuleSpec = Field(..., description="Technical specification of the model")