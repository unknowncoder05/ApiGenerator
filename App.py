import json
from utils import nested_key
from djangocompiler import compiler
class App:
    def __init__(self,json_app_file) -> None:
        with open(json_app_file,"r") as f:
            raw_app=json.load(f)
        if nested_key(raw_app,["settings","framework"],required=True) == "python/django":
            compiler(raw_app)
if __name__ == "__main__":
    app = App("app.json")
