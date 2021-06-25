class ModelSerializer:
    name = None
    def __init__(self, model) -> None:
        self.name=f"{model.name}Serializer"