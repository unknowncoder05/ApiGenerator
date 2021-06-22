class Field:
    attrs = {}
    name = None
    def __init__(self, name:str, attrs) -> None:
        self.attrs = attrs
        self.name = name
        self.type = get_type(attrs["type"])
    def __str__(self) -> str:
        return f"{self.name} {self.type}"
    def render(self, indentation) -> list:
        string_attrs = []
        imports = []
        if "max" in self.attrs:
            field,new_imps = min_max_field(self.attrs)
            imports.extend(new_imps)
            if field != "":
                string_attrs.append(field)
        if "required" in self.attrs and self.attrs["required"] == True:
            string_attrs.append("blank=False")
        else:
            string_attrs.append("blank=True")
        lines = [
            "\t"*indentation+ f"{self.name} = models.{self.type}({', '.join(string_attrs)})"
        ]
        return lines, imports
def get_type(raw_type):
    if raw_type in TYPES:
        return TYPES[raw_type]
    raise NameError(f"Type {raw_type} not registered")
def min_max_field(attrs):
    res = ""
    imps = []
    if attrs["type"] in ["str", "psw"]:
        aux = []
        if "min" in attrs:
           aux.append(f"min_length={attrs['min']}")
        if "max" in attrs:
            aux.append(f"max_length={attrs['max']}")
        res = ', '.join(aux)
    elif attrs["type"] in ["int","float"]:
        aux = []
        if "min" in attrs:
            imps.extend([
            "from django.core.validators import MinValueValidator"
            ])
            aux.append(f"MinValueValidator({attrs['min']})")
        if "max" in attrs:
            imps.extend([
            "from django.core.validators import MaxValueValidator"
            ])
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