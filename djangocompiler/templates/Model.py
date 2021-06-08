from .Field import Field
class Model:
    fields = {}
    name = None
    imports = []
    def __init__(self, name, raw_model) -> None:
        self.name = name
        if '__extends' in raw_model:
            self.fields = TEMPLATES[raw_model['__extends']]
        for field in raw_model:
            if not field.startswith("__"):
                self.add_field(field,raw_model[field])
    def add_field(self, name, field) -> None:
        new_field = Field(name, field)
        self.fields[name] = new_field
    def render(self) -> list:
        lines = [
            f"class {self.name.title()}:"
        ]
        imports = self.imports
        for field in self.fields:
            new_field,imps = self.fields[field].render(indentation=1)
            imports.extend(imps)
            lines.extend(new_field)
        #lines.extend([
        #])
        return lines, imports
TEMPLATES = {
    "USER":{
        "name":Field("name", {"type":"str", "min":5, "max":20, "required":True}),
        "password":Field("password", {"type":"psw", "min":8, "max":50, "required":True})
    }
}