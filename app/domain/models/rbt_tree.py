from typing import Any
from .node import Node, NodeColor
from app.domain.exceptions import DuplicateKeyError


class RedBlackTree:
    """Агрегат: Красно-черное дерево."""
    def __init__(self):
        self.root: Node | None = None
        self.size: int = 0

    def search(self, key: Any) -> Node | None:
        """Поиск узла по ключу. Возвращает либо None, либо Node"""
        current = self.root
        while current is not None:
            if current.key == key:
                return current
            if current.key > key:
                current = current.left
            elif current.key < key:
                current = current.right
        return None

    def insert(self, key: Any, value: Any):
        """
        Вставка нового узла в дерево.
        :param key: Ключ узла.
        :param value: Значение узла.
        :return: None.
        :raises DuplicateKeyError - узел с ключом уже существует.
        """
        if self.search(key):
            raise DuplicateKeyError(key=key)
        node = Node(key=key, value=value)
        self._insert(node)
        self._fix_insert(node)
        self.size += 1

    def _insert(self, node: Node):
        """Вставка узла как в бинарном дереве поиска."""
        x, y = self.root, None
        while x is not None:
            y = x
            if node.key < x.key:
                x = x.left
            elif node.key > x.key:
                x = x.right
        node.parent = y
        if y is None:
            self.root = node
        elif node.key < y.key:
            y.left = node
        elif node.key > y.key:
            y.right = node

    def _fix_insert(self, node: Node):
        """Алгоритм балансировки дерева после вставки."""
        while node.parent and node.parent.color == NodeColor.RED:
            if node.parent.parent.left == node.parent:
                uncle = node.parent.parent.right
                if uncle and uncle.color == NodeColor.RED:
                    node.parent.color = NodeColor.BLACK
                    uncle.color = NodeColor.BLACK
                    node.parent.parent.color = NodeColor.RED
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        node = node.parent
                        self._left_rotate(node)
                    node.parent.color = NodeColor.BLACK
                    node.parent.parent.color = NodeColor.RED
                    self._right_rotate(node.parent.parent)
            else:
                u = node.parent.parent.left  # uncle
                if u is not None and u.color == NodeColor.RED:
                    u.color = NodeColor.BLACK
                    node.parent.color = NodeColor.BLACK
                    node.parent.parent.color = NodeColor.RED
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self._right_rotate(node)
                    node.parent.color = NodeColor.BLACK
                    node.parent.parent.color = NodeColor.RED
                    self._left_rotate(node.parent.parent)
            if node == self.root:
                break
        self.root.color = NodeColor.BLACK

    def _left_rotate(self, x: Node):
        """Левый поворот дерева."""
        y = x.right
        x.right = y.left
        if y.left is not None:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = x
        elif x.parent.left == x:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def _right_rotate(self, x: Node):
        """Правый поворот дерева."""
        y = x.left
        x.left = y.right
        if y.right is not None:
            y.right.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y