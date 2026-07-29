from backend.system.action_executor import execute
from backend.system.models import Action

action = Action(
    intent="open_application",
    target="cmd",
    parameters={}
)

resultado = execute(action)

print(resultado)