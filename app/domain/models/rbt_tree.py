from typing import Any
from app.domain.models.node import Node, NodeColor
from app.domain.exceptions import DuplicateKeyError


class RedBlackTree:
    """Агрегат: Красно-черное дерево."""

    def __init__(self):
        self.root: Node | None = None
        self.size: int = 0

    def _change_color(self, node: Node, new_color: NodeColor):
        """Метод смены цвета"""
        if node.color != new_color:
            node.color = new_color

    def search(self, key: Any) -> Node | None:
        """Поиск узла по ключу. Возвращает либо None, либо Node"""
        current = self.root
        while current is not None:
            if current.key == key:
                return current
            if current.key > key:
                current = current.left
            else:
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
            else:
                x = x.right
        node.parent = y
        if y is None:
            self.root = node
        elif node.key < y.key:
            y.left = node
        else:
            y.right = node

    def _fix_insert(self, node: Node):
        """Алгоритм балансировки дерева после вставки."""
        while node.parent and node.parent.color == NodeColor.RED:
            if node.parent.parent and node.parent.parent.left == node.parent:
                uncle = node.parent.parent.right
                if uncle and uncle.color == NodeColor.RED:
                    self._change_color(node.parent, NodeColor.BLACK)
                    self._change_color(uncle, NodeColor.BLACK)
                    self._change_color(node.parent.parent, NodeColor.RED)
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        node = node.parent
                        self._left_rotate(node)
                    if node.parent and node.parent.parent:
                        self._change_color(node.parent, NodeColor.BLACK)
                        self._change_color(node.parent.parent, NodeColor.RED)
                        self._right_rotate(node.parent.parent)
            else:
                if node.parent and node.parent.parent:
                    uncle = node.parent.parent.left
                    if uncle and uncle.color == NodeColor.RED:
                        self._change_color(uncle, NodeColor.BLACK)
                        self._change_color(node.parent, NodeColor.BLACK)
                        self._change_color(node.parent.parent, NodeColor.RED)
                        node = node.parent.parent
                    else:
                        if node == node.parent.left:
                            node = node.parent
                            self._right_rotate(node)
                        if node.parent and node.parent.parent:
                            self._change_color(node.parent, NodeColor.BLACK)
                            self._change_color(node.parent.parent, NodeColor.RED)
                            self._left_rotate(node.parent.parent)
            if node == self.root:
                break
        if self.root:
            self._change_color(self.root, NodeColor.BLACK)

    def _left_rotate(self, x: Node):
        """Левый поворот дерева."""
        y = x.right
        if not y: return
        x.right = y.left
        if y.left is not None:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x.parent.left == x:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def _right_rotate(self, x: Node):
        """Правый поворот дерева."""
        y = x.left
        if not y: return
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

    def delete(self, key: Any):
        """Удаление узла по ключу."""
        node_to_delete = self.search(key)
        if node_to_delete is None:
            return
        self._delete_node(node_to_delete)
        self.size -= 1

    def _delete_node(self, z: Node):
        y = z
        y_original_color = y.color
        x = None

        if z.left is None:
            x = z.right
            self._rb_transplant(z, z.right)
        elif z.right is None:
            x = z.left
            self._rb_transplant(z, z.left)
        else:
            y = self._minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                if x: x.parent = y
            else:
                self._rb_transplant(y, y.right)
                y.right = z.right
                if y.right: y.right.parent = y

            self._rb_transplant(z, y)
            y.left = z.left
            if y.left: y.left.parent = y
            self._change_color(y, z.color)

        if y_original_color == NodeColor.BLACK and x is not None:
            self._fix_delete(x)

    def _rb_transplant(self, u: Node, v: Node | None):
        """Заменяет поддерево u на поддерево v."""
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        if v is not None:
            v.parent = u.parent

    def _minimum(self, node: Node) -> Node:
        """Находит узел с минимальным ключом."""
        while node.left is not None:
            node = node.left
        return node

    def _fix_delete(self, x: Node):
        """Полная корректная и безопасная нерекурсивная балансировка удаления"""
        while x != self.root and x.color == NodeColor.BLACK:
            if x.parent and x == x.parent.left:
                w = x.parent.right
                if w and w.color == NodeColor.RED:
                    self._change_color(w, NodeColor.BLACK)
                    self._change_color(x.parent, NodeColor.RED)
                    self._left_rotate(x.parent)
                    w = x.parent.right

                if not w:
                    x = x.parent
                elif (not w.left or w.left.color == NodeColor.BLACK) and \
                        (not w.right or w.right.color == NodeColor.BLACK):
                    self._change_color(w, NodeColor.RED)
                    x = x.parent
                else:
                    if not w.right or w.right.color == NodeColor.BLACK:
                        if w.left:
                            self._change_color(w.left, NodeColor.BLACK)
                        self._change_color(w, NodeColor.RED)
                        self._right_rotate(w)
                        w = x.parent.right

                    if w and x.parent:
                        self._change_color(w, x.parent.color)
                        self._change_color(x.parent, NodeColor.BLACK)
                        if w.right:
                            self._change_color(w.right, NodeColor.BLACK)
                        self._left_rotate(x.parent)
                    x = self.root
            else:
                if x.parent:
                    w = x.parent.left
                    if w and w.color == NodeColor.RED:
                        self._change_color(w, NodeColor.BLACK)
                        self._change_color(x.parent, NodeColor.RED)
                        self._right_rotate(x.parent)
                        w = x.parent.left

                    if not w:
                        x = x.parent
                    elif (not w.left or w.left.color == NodeColor.BLACK) and \
                            (not w.right or w.right.color == NodeColor.BLACK):
                        self._change_color(w, NodeColor.RED)
                        x = x.parent
                    else:
                        if not w.left or w.left.color == NodeColor.BLACK:
                            if w.right:
                                self._change_color(w.right, NodeColor.BLACK)
                            self._change_color(w, NodeColor.RED)
                            self._left_rotate(w)
                            w = x.parent.left

                        if w and x.parent:
                            self._change_color(w, x.parent.color)
                            self._change_color(x.parent, NodeColor.BLACK)
                            if w.left:
                                self._change_color(w.left, NodeColor.BLACK)
                            self._right_rotate(x.parent)
                        x = self.root
        self._change_color(x, NodeColor.BLACK)
