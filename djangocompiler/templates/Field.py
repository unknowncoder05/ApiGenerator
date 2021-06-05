class Field:
    attrs = {}
    name = None
    def __init__(self, name:str, attrs) -> None:
        self.attrs = attrs
        self.name = name
        self.type = get_type(attrs["type"])
    def render(self, indentation) -> list:
        string_attrs = ""
        if "max" in self.attrs:
            string_attrs += 
        lines = [
            "\t"*indentation+ f"{self.name} = models.{self.type}({string_attrs})"
        ]
        
        return lines
def get_type(raw_type):
    if raw_type in TYPES:
        return TYPES[raw_type]
    raise NameError("Type not registered")

TYPES = {
    "string":"CharField"
}