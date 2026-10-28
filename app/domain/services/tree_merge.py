from app.domain.exceptions import DuplicateKeyError
from app.domain.models.node import Node
from app.domain.models.rbt_tree import RedBlackTree


class TreeMergeService:
    """Доменный сервис для объединения 2-х деревьев."""

    @classmethod
    def merge(cls, tree_a: RedBlackTree, tree_b: RedBlackTree) -> RedBlackTree:
        """Объединить два независимых дерева."""
        tree_c = RedBlackTree()
        # Вставить узлы из первого дерева в новое
        cls._merge(tree_a.root, tree_c)
        # Вставить узлы из второго дерева в новое
        cls._merge(tree_b.root, tree_c)
        return tree_c

    @classmethod
    def _merge(cls, node: Node | None, new_tree: RedBlackTree):
        """Рекурсивный алгоритм для обхода дерева и объединения с новым."""
        if node is None:
            return

        cls._merge(node.left, new_tree)
        try:
            new_tree.insert(node.key, node.value)
        except DuplicateKeyError:
            pass
        cls._merge(node.right, new_tree)