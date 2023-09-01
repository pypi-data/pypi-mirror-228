from dataclasses import dataclass
from enum import Enum


@dataclass
class AgentSkillConfiguration:
    name: str
    description: str
    flow_name: str
    return_direct: bool


class ArbitrationMethod(Enum):
  LANGCHAIN = "Langchain Zero Shot Agent"
  OPENAI_FUNCTIONS = "OpenAI Functions"
  SEMANTIC_KERNEL = "Semantic Kernel Custom Orchestrator"
  SEMANTIC_KERNEL_PLANNER = "Semantic Kernel Action Planner"