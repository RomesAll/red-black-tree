from app.domain.models.node import Node
from app.domain.models.rbt_tree import RedBlackTree
from app.domain.models.value_objects import TreeDifference


class TreeDiffService:
    """Доменный сервис для вычисления разницы между двумя деревьями."""

    @classmethod
    def compare(cls, tree_a: RedBlackTree, tree_b: RedBlackTree) -> TreeDifference:
        """Получить разницу между 2-я деревьями."""
        keys_a, keys_b = set(), set()
        cls._extract_tree_keys(tree_a.root, keys_a)
        cls._extract_tree_keys(tree_b.root, keys_b)

        only_in_a = sorted(list(keys_a - keys_b))
        only_in_b = sorted(list(keys_b - keys_a))

        return TreeDifference(
            only_in_a=only_in_a,
            only_in_b=only_in_b,
            are_identical=keys_a == keys_b
        )

    @classmethod
    def _extract_tree_keys(cls, node: Node | None, keys: set):
        """
        Рекурсивный метод для обхода дерева в глубину
        и сохранения ключей в коллекцию set.
        """
        if node is None:
            return

        cls._extract_tree_keys(node.left, keys)
        keys.add(node.key)
        cls._extract_tree_keys(node.right, keys)