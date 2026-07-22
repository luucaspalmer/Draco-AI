from tools.tool_manager import ToolManager



manager = ToolManager()



response = manager.execute(
    "weather"
)



print(response)