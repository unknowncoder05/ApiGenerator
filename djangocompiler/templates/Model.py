from .Field import Field
class Model:
    fields = {}
    name = None
    def __init__(self, name, raw_model) -> None:
        self.name = name
        if '__extends' in raw_model:
            self.fields = raw_model['__extends']
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
        for field in self.fields:
            lines.extend(field.render(indentation=1))
        lines.extend([
            ""
        ])
        return lines
TEMPLATES = {
    "USER":{
        "name":Field("name", {"type":"string","min":5,"max":20}),
        "password":Field("name", {"type":"password","min":5,"max":20})
    }
}