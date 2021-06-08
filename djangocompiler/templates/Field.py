class Field:
    attrs = {}
    name = None
    def __init__(self, name:str, attrs) -> None:
        self.attrs = attrs
        self.name = name
        self.type = get_type(attrs["type"])
    def render(self, indentation) -> list:
        string_attrs = ""
        imports = []
        if "max" in self.attrs:
            field,new_imps = min_max_field(self.attrs)
            imports.extend(new_imps)
            string_attrs += field
        lines = [
            "\t"*indentation+ f"{self.name} = models.{self.type}({string_attrs})"
        ]
        return lines, imports
def get_type(raw_type):
    if raw_type in TYPES:
        return TYPES[raw_type]
    raise NameError(f"Type {raw_type} not registered")
def min_max_field(attrs):
    res = ""
    imps = []
    if attrs["type"] == "string":
        if "max" in attrs:
            res+=f"max_length={attrs['max']}"
        if "min" in attrs:
            res+=f"min_length={attrs['min']}"
    elif attrs["type"] in ["int","float"]:
        imps.append("from django.core.validators import MaxValueValidator, MinValueValidator")
        aux = []
        if "min" in attrs:
            aux.append(f"MinValueValidator({attrs['min']})")
        if "max" in attrs:
            aux.append(f"MaxValueValidator({attrs['max']})")
        res = "validators=["+', '.join(aux)+"]"
    return res, imps
TYPES = {
    "str":"CharField",
    "int":"IntegerField",
    "psw":"CharField",
    "datetime":"DateTimeField",
    "date":"DateField",
}