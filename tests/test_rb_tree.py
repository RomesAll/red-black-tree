from app.domain.models.node import Node
from app.domain.models.rbt_tree import RedBlackTree
from app.domain.services.tree_diff import TreeDiffService
from app.domain.services.tree_merge import TreeMergeService


def test_init_rbtree():
    """Тест: проверка инициализации агрегата RedBlackTree."""
    tree = RedBlackTree()
    assert tree.size == 0
    assert tree.root is None


def test_search_node_in_rbt():
    """Тест: проверка поиска узлов в RedBlackTree."""
    tree = RedBlackTree()
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