from .Field import Field
class Model:
    fields = None
    name = None
    verbose_name = None
    verbose_name_plural = None
    is_user = False

    model_class = "models.Model"
    imports = [
        "from django.db import models"
    ]
    def __init__(self, name, raw_model) -> None:
        self.name = name
        self.properties = {}
        if '__extends' in raw_model:
            self.properties = TEMPLATES[raw_model['__extends']].copy()
            if "USER" == raw_model['__extends']:
                self.is_user = True
                self.imports = ["from django.contrib.auth.models import AbstractUser"]
                self.model_class = "AbstractUser"
        self.properties.update(raw_model)
        self.verbose_name = self.properties["__verbose_name"] if "__verbose_name" in self.properties else name
        self.verbose_name_plural = self.properties["__verbose_name_plural"] if "__verbose_name_plural" in self.properties else self.verbose_name
        self.fields = {}
        for field in self.properties:
            if not field.startswith("__"):
                self.add_field(field,self.properties[field])
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
        if self.is_user:
            lines.extend([
                "\t"*1+ f"USERNAME_FIELD = '{self.properties['__USERNAME_FIELD']}'",
            ])
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
        "__USERNAME_FIELD":"email"
    }
}