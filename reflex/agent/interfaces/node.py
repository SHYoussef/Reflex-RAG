from typing import Annotated

from typing_extensions import TypedDict

from langgraph.graph.message import add_messages

import inspect


class INodes:
    
    def __init__(self):
        self.all_methods = self._get_all_methods_names()

    @classmethod
    def _get_all_methods_names(cls):
        return [name for name, func in inspect.getmembers(cls, inspect.isfunction) if name != "__init__"]     

