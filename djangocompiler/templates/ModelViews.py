from . import Model
PERMISSION_LEVELS = [
    "public",
    "authed",
    "owner",
    "admin"
]
ACTIONS = [
    "list",
    "get",
    "write",
    "update"
    "delete",
    "all"
]
render_template="""
class UserViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)
"""
class ModelViews:
    model = None
    actions = []
    def __init__(self, model:Model) -> None:
        self.model = model
        self.actions = self.model.properties["__actions"] if "__actions" in self.model.properties else []
    def render(self):
        lines = [
            f"class {self.model.name}ViewSet(viewsets.ViewSet):"
            
        ]
        imports = [
            f"from .models import {self.model.name}",
            f"from .serializers import {self.model.serializer}",
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
                if action == "list":
                    lines.extend([
                        "\t"*1+ "def list(self, request):",
                        "\t"*2+ "queryset = self.model_class.objects.all()",
                        "\t"*2+ "serializer = self.serializer_class(queryset, many=True)",
                        "\t"*2+ "return Response(serializer.data)",
                        ""
                    ])
                if action == "get":
                    imports.append("from django.shortcuts import get_object_or_404")
                    lines.extend([
                        "\t"*1+ "def retrieve(self, request):",
                        "\t"*2+ "object = get_object_or_404(queryset, pk=pk)",
                        "\t"*2+ "serializer = self.serializer_class(object)",
                        "\t"*2+ "return Response(serializer.data)",
                    ])
            #if action == "list":
        return lines, imports
