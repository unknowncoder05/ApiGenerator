from . import Model
PERMISSION_LEVELS = [
    "public",
    "authed",
    "owner",
    "admin"
]
TAB = "\t"
ACTIONS = {
    "list":{
        "imports":[],
        "lines":[
            "def list(self, request):",
            TAB*1+ "queryset = self.model_class.objects.all()",
            TAB*1+ "serializer = self.serializer_class(queryset, many=True)",
            TAB*1+ "return Response(serializer.data)",
        ]
        },
    "get":{
        "imports":["from django.shortcuts import get_object_or_404"],
        "lines":[
            "def retrieve(self, request):",
            TAB*1+ "queryset = self.model_class.objects.all()",
            TAB*1+ "object = get_object_or_404(queryset, pk=pk)",
            TAB*1+ "serializer = self.serializer_class(object)",
            TAB*1+ "return Response(serializer.data)",
        ]
    },
    "write":{
        "imports":[],
        "lines":[
            "def create(self, request):",
            TAB*1+ "serializer = self.serializer_class(data=request.data)",
            TAB*1+ "serializer.is_valid(raise_exception=True)",
            TAB*1+ "serializer.save()",
            TAB*1+ "return Response(serializer.data)",
        ]
    },
    "update":{
        "imports":["from rest_framework import status"],
        "lines":[
            "def update(self, request):",
            TAB*1+ "instance = self.model_class(data=request.data)",
            TAB*1+ "serializer = self.get_serializer(instance, data=request.data, partial=partial)",
            TAB*1+ "serializer.is_valid(raise_exception=True)return Response(status=status.HTTP_204_NO_CONTENT)",
            TAB*1+ "return Response(status=status.HTTP_204_NO_CONTENT)",
        ]
    },
    "delete":{
        "imports":[],
        "lines":[
            "def destroy(self, request):",
            TAB*1+ "instance = self.model_class(data=request.data)",#GET OBJECT
            TAB*1+ "instance.delete()",
            TAB*1+ "return Response(status=status.HTTP_204_NO_CONTENT)",
        ]
    }
}
class ModelViews:
    model = None
    actions = []
    def __init__(self, model:Model) -> None:
        self.model = model
        self.actions = self.model.properties["__actions"] if "__actions" in self.model.properties else []
    def add_action_to_view(self, new_action, lines, imports):
        if new_action == "all":
            for action in ACTIONS:
                imports.extend(ACTIONS[action]["imports"])
                lines.extend([TAB+x for x in ACTIONS[action]["lines"]])
            return lines, imports
        if new_action not in ACTIONS:
            raise NameError(f"\"{new_action}\" is Not a valid Action")
        imports.extend(ACTIONS[new_action]["imports"])
        lines.extend([TAB+x for x in ACTIONS[new_action]["lines"]])
        return lines, imports
    def render(self):
        lines = [
            f"class {self.model.name}ViewSet(viewsets.ViewSet):"
            
        ]
        imports = [
            f"from .models import {self.model.name}",
            f"from .serializers import {self.model.serializer.name}",
            "from rest_framework import viewsets"
        ]
        to_render = {}
        for action in self.actions:
            if self.actions[action] not in to_render:
                to_render[self.actions[action]] = [action]
            else:
                to_render[self.actions[action]].append(action)
        lines.extend([
            "\t"*1+f"serializer_class = {self.model.serializer.name}",
            "\t"*1+f"model_class = {self.model.name}"
        ])
        for view in to_render:
            for action in to_render[view]:
                lines, imports = self.add_action_to_view(action, lines, imports)
            #if action == "list":
        return lines, imports
