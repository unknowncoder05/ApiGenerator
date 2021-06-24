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

def render_settings(blueprint):
    db = {}
    if "database" in blueprint: # HaACK: this will only work for one db
        name = blueprint['database'][0].get('__db')
        user = blueprint['database'][0].get('__user')
        psw  = blueprint['database'][0].get('__password')
        host = blueprint['database'][0].get('__host')
        port = blueprint['database'][0].get('__port')
        db = DB_SETTINGS_FORMAT.format(
            engine=DB_ENGINES.get(blueprint["database"][0]["type"]),
            name=f"os.environ['{name}']",
            user=f"os.environ['{user}']",
            psw=f"os.environ['{psw}']",
            host=f"os.environ['{host}']",
            port=f"os.environ['{port}']",
        )
    main_user = ""
    for model in blueprint["models"]:
        if blueprint["models"][model].get("__extends") == "USER":
            if blueprint["models"][model].get("__main_user"):
                main_user = model
                break
            else:
                if main_user == "":
                    main_user = model

    user_settings = f"AUTH_USER_MODEL = '{'api'}.{main_user}'"#blueprint['settings']['name']
    return user_settings