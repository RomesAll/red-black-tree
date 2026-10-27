from typing import Any
from .node import Node
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
        pass

    def _left_rotate(self, x: Node):
        """Левый поворот дерева."""
        pass

    def _right_rotate(self, x: Node):
        """Правый поворот дерева."""
        pass