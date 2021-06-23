from utils import nested_key
from .templates import Model
def compiler(blueprint):
    commands = []
    name = nested_key(blueprint,["settings","name"],default="app")
    commands.append(f"django-admin startproject {name}")
    # MODELS
    models = []
    for model in nested_key(blueprint,["models"],default={}):
        new_model = Model(model,blueprint["models"][model])
        models.append(new_model)
    models_printer(models)
def models_printer(models):
    rendered_models = []
    imports = []
    for model in models:
        new_model, new_imps = model.render()
        rendered_models.append(new_model)
        for import_line in new_imps:
            if import_line not in imports:
                imports.append(import_line)
    
    print("\n".join(imports))
    for model in rendered_models:
        print("\n".join(model))

