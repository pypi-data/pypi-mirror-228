from promptflow.azure import PFClient
import json
from semantic_kernel.skill_definition import sk_function

from flow_agent_package.tools.contracts import AgentSkillConfiguration
from flow_agent_package.tools.flow_manager import FlowManager


class AgentSkill():

    def __init__(self, config: AgentSkillConfiguration, pf: PFClient, subscription_id, resource_group, workspace_name):
        self.name = config.name
        self.tool_description = config.description
        self.return_direct = config.return_direct
        self.flow_manager = FlowManager(pf, config.flow_name, subscription_id, resource_group, workspace_name)
        
        self.function_description = self.init_description(self.flow_manager.flow_json, config)
  
    def init_description(self, flow_json, config):
        config_desc = config.description
        # In case of default desc, use tool description
        # TODO: default to config description first?
        if flow_json.get("description") == "Template Standard Flow" or flow_json.get("description") == "Template Chat Flow":
            return config_desc
        return flow_json.get("description", config_desc)

    def get_langchain_tool_description(self):
        
        return self.function_description + self.flow_manager.get_input_descriptions()

    
    def to_function_definition(self):
        return {
            "name": self.flow_manager.flow_json["flowName"].replace(" ", "_"),
            "description": self.function_description,
            "parameters":{
                "type": "object",
                "properties": self.flow_manager.input_config
            }
        }

    def to_langchain_function(self):

        def run_str(query):
            result = self.execute(json.loads(query))
            return result
        
        return run_str

    def to_sk_function(self):
        # TODO: See if there is a way to have dynamic decorators based on flows inputs (can you add decorators after the fact?)
        @sk_function(
            description=self.function_description,
            name=self.name
        )
        def sk_execute_func(query: str) -> str:
            result = self.execute(json.loads(query))
            return result
        return sk_execute_func

    def execute(self, inputs) -> dict:
        try:
            return self.flow_manager.execute_flow(inputs)
        except Exception as e:
            print(f"Exception encountered: {str(e)}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            return f"Unable to execute skill {self.name} due to exception: {str(e)}"

