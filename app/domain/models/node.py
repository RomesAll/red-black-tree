from enum import Enum
from dataclasses import dataclass
from typing import Any


class NodeColor(Enum):
    RED = 'RED'
    BLACK = 'BLACK'


@dataclass(slots=True)
class Node:
    """Узел красно-черного дерева."""
    key: Any
    value: Any = None
    color: NodeColor = NodeColor.RED
    parent: 'Node | None' = None
    left: 'Node | None' = None
    right: 'Node | None' = None

    def __repr__(self) -> str:
        color_str = self.color.value
        return f"Node(key={self.key}, color={color_str})"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Node):
            return NotImplemented
        return self.key == other.key

    def __hash__(self) -> int:
        return hash(self.key)