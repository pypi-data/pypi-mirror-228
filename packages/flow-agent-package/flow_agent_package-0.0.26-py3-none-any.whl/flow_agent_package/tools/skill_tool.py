from promptflow import tool
# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
from flow_agent_package.tools.contracts import AgentSkillConfiguration

# TODO: Fix input name and tool name
@tool
def skill(name: str, description: str, flow_id: str, return_direct: bool):
  config = AgentSkillConfiguration(name, description, flow_id, return_direct)
  return config
