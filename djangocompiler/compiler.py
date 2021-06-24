from utils import nested_key
from .templates import Model
from .templates import render_settings

def compiler(blueprint):
    commands = []
    name = nested_key(blueprint,["settings","name"],default="app")
    commands.append(f"django-admin startproject {name}")
    # MODELS
    models = []
    for model in nested_key(blueprint,["models"],default={}):
        new_model = Model(model,blueprint["models"][model])
        models.append(new_model)
    model_lines = render_models(models)

    settings_lines = render_settings(blueprint)
    print("\n".join(model_lines))
    print(settings_lines)
def render_models(models):
    rendered_models = []
    imports = []
    for model in models:
        new_model, new_imps = model.render()
        rendered_models.append(new_model)
        for import_line in new_imps:
            if import_line not in imports:
                imports.append(import_line)
    lines = []
    lines.extend(imports)
    for model in rendered_models:
        lines.append("")
        lines.extend(model)
    return lines
