from uuid import uuid4
import pytest
from app.domain import NodeColor, DuplicateKeyError
from app.domain.models.node import Node
from app.domain.models.rbt_tree import RedBlackTree
from app.domain.services.tree_diff import TreeDiffService
from app.domain.services.tree_merge import TreeMergeService


def test_init_rbtree():
    """Тест: проверка инициализации агрегата RedBlackTree."""
    tree = RedBlackTree(tree_id=uuid4())
    assert tree.size == 0
    assert tree.root is None


def test_search_node_in_rbt():
    """Тест: проверка поиска узлов в RedBlackTree."""
    tree = RedBlackTree(tree_id=uuid4())
    tree.insert(key=1, value='1')
    node_1 = tree.search(key=1)
    node_2 = tree.search(key=2)
    assert isinstance(node_1, Node)
    assert node_1.key == 1
    assert node_1.value == '1'
    assert node_2 is None


def test_delete_node_from_rbt(setup_rbt_a):
    """Тест: проверка удаления узла в RedBlackTree."""
    delete_root = setup_rbt_a.root
    setup_rbt_a.delete(key=delete_root.key)
    assert delete_root.key != setup_rbt_a.root.key
    assert delete_root.key == 4


def test_merge_rbt(setup_rbt_a, setup_rbt_b):
    """Тест: объединения 2-х деревьев RedBlackTree."""
    tree_c = TreeMergeService.merge(setup_rbt_a, setup_rbt_b)
    assert tree_c.root.key == 6


def test_compare_rbt(setup_rbt_a, setup_rbt_b):
    """Тест: получение разницы между 2-я деревьями RedBlackTree."""
    result = TreeDiffService.compare(setup_rbt_a, setup_rbt_b)
    assert result.only_in_a == [3, 4, 5]
    assert result.only_in_b == [22, 54, 90]
    assert result.are_identical == False


def test_tree_dfs_iter(setup_rbt_a):
    """Тест: получение узлов дерева по запросу через генератор."""
    count = 0
    for node in setup_rbt_a.iterative_dfs():
        count += 1
        assert isinstance(node, Node)
    assert count == setup_rbt_a.size


def test_insert_node():
    """Тест: добавление узлов в дерево по возрастанию."""
    tree = RedBlackTree(tree_id=uuid4())
    tree.insert(key=10, value=10)
    tree.insert(key=20, value=20)
    tree.insert(key=30, value=30)
    assert tree.root.color == NodeColor.BLACK
    assert tree.root.key == 20
    assert tree.root.left.color == NodeColor.RED
    assert tree.root.right.color == NodeColor.RED


def test_rotation_node():
    """Тест: левый и правый поворот дерева."""
    tree_a = RedBlackTree(tree_id=uuid4())
    tree_b = RedBlackTree(tree_id=uuid4())

    for key_a, key_b in [(10, 30), (20, 20), (30, 10)]:
        tree_a.insert(key=key_a, value=key_a)
        tree_b.insert(key=key_b, value=key_b)

    # Проверить деревья на идентичность
    diff = TreeDiffService.compare(tree_a, tree_b)
    assert diff.are_identical == True
    assert all([
        tree_a.root.key == 20,
        tree_a.root.color == NodeColor.BLACK
    ])
    assert all([
        tree_b.root.key == 20,
        tree_b.root.color == NodeColor.BLACK
    ])


def test_two_rotation():
    """Тест: двойной поворот дерева."""
    tree = RedBlackTree(tree_id=uuid4())

    for i, key in enumerate(start=1, iterable=[10, 30, 20]):
        tree.insert(key=key, value=key)
        if i == 1:
            assert tree.root.key == 10
        if i == 2:
            assert tree.root.right.key == 30

    assert tree.root.key == 20
    assert tree.root.color == NodeColor.BLACK


def test_insert_duplicate_node():
    """Тест: добавить дубликат узла в дерево."""
    tree = RedBlackTree(tree_id=uuid4())
    with pytest.raises(DuplicateKeyError):
        tree.insert(key=10, value=10)
        tree.insert(key=10, value=10)
