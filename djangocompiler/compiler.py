from utils import nested_key
from .templates import Model

DB_SETTINGS_FORMAT="""
DATABASES = {{
    'default': {{
        'ENGINE': {engine},
        'NAME': {name},
        'USER': {user},
        'PASSWORD': {psw},
        'HOST': {host},
        'PORT': {port},
    }}
}}
"""
DB_ENGINES={
    "postgres":'django.db.backends.postgresql_psycopg2'
}
def compiler(blueprint):
    commands = []
    name = nested_key(blueprint,["settings","name"],default="app")
    commands.append(f"django-admin startproject {name}")
    # MODELS
    models = []
    for model in nested_key(blueprint,["models"],default={}):
        new_model = Model(model,blueprint["models"][model])
        models.append(new_model)
    #render_models(models)

    settings_lines = render_settings(blueprint)
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
    
    print("\n".join(imports))
    for model in rendered_models:
        print("\n".join(model))

def render_settings(blueprint):
    db = {}
    if "database" in blueprint: # HaACK: this will only work for one db
        name = blueprint['database'][0].get('__db')
        user = blueprint['database'][0].get('__user', 'postgres')
        psw  = blueprint['database'][0].get('__password')
        host = blueprint['database'][0].get('__host', 'localhost')
        port = blueprint['database'][0].get('__port', '5432')
        db = DB_SETTINGS_FORMAT.format(
            engine=DB_ENGINES.get(blueprint["database"][0]["type"]),
            name=f"os.environ['{name}']",
            user=f"os.environ['{user}']",
            psw=f"os.environ['{psw}']",
            host=f"os.environ['{host}']",
            port=f"os.environ['{port}']",
        )
    return db