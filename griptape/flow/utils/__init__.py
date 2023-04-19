import json
from griptape.flow.utils.j2 import J2
from griptape.flow.utils.conversation import Conversation
from griptape.flow.utils.tool_loader import ToolLoader

__all__ = [
    "J2",
    "Conversation",
    "ToolLoader"
]


def minify_json(value: str) -> str:
    return json.dumps(json.loads(value), separators=(',', ':'))
