
'''
snippet_list = SnippetViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
'''
from . import ModelViews

class ModelViews:
    model_view = None
    actions = []
    def __init__(self, model_view:ModelViews) -> None:
        self.model_view = model_view
    def render():
        pass