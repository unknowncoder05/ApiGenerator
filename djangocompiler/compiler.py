from utils import nested_key
from .templates import Model
def compiler(blueprint):
    commands = []
    name = nested_key(blueprint,["settings","name"],default="app")
    commands.append(f"django-admin startproject {name}")
    print(commands)
    models = []
    for model in nested_key(blueprint,["models"],default={}):
        new_model = Model(model,blueprint["models"][model])
        models.append(new_model)
