"""
Tool Manager
------------
Gerencia ferramentas disponíveis do Draco.
"""


from backend.tools.weather_tool import WeatherTool



class ToolManager:


    def __init__(self):

        self.tools = {

            "weather":
            WeatherTool()

        }



    def execute(
        self,
        tool_name: str
    ):


        tool = self.tools.get(
            tool_name
        )


        if not tool:

            return None


        return tool.execute()