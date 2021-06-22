from .Field import Field
class Model:
    fields = None
    name = None
    verbose_name = None
    verbose_name_plural = None

    model_class = "models.Model"
    imports = [
        "from django.db import models"
    ]
    def __init__(self, name, raw_model) -> None:
        self.name = name
        properties = {}
        if '__extends' in raw_model:
            properties = TEMPLATES[raw_model['__extends']].copy()
        properties.update(raw_model)
        self.verbose_name = properties["__verbose_name"] if "__verbose_name" in properties else name
        self.verbose_name_plural = properties["__verbose_name_plural"] if "__verbose_name_plural" in properties else self.verbose_name
        self.fields = {}
        for field in properties:
            if not field.startswith("__"):
                self.add_field(field,properties[field])
    def add_field(self, name, field) -> None:
        new_field = Field(name, field)
        self.fields[name] = new_field
    def render(self) -> list:
        lines = [
            f"class {self.name.title()}({self.model_class}):"
        ]
        imports = self.imports
        for field in self.fields:
            new_field,imps = self.fields[field].render(indentation=1)
            imports.extend(imps)
            lines.extend(new_field)
        lines.extend([
            "\t"*1+"class Meta:",
            #"\t"+"ordering = ['name']",
            "\t"*2+f"verbose_name = ('{self.verbose_name}')",
            "\t"*2+f"verbose_name_plural = ('{self.verbose_name_plural}')",
        ])
        return lines, imports
TEMPLATES = {
    "USER":{
        "name":{"type":"str", "min":5, "max":20, "required":True},
        "password":{"type":"psw", "min":8, "max":50, "required":True},
        "__verbose_name":"user",
        "__verbose_name_plural":"users",
    }
}