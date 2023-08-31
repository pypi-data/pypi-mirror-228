from dataclasses import dataclass
from enum import Enum


@dataclass
class AgentSkillConfiguration:
    name: str
    description: str
    flow_name: str
    return_direct: bool


class ArbitrationMethod(Enum):
  LANGCHAIN = "Langchain"
  OPENAI_FUNCTIONS = "OpenAI Functions"
  SEMANTIC_KERNEL = "Semantic Kernel"