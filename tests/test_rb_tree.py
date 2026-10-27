from app.domain.models.node import Node
from app.domain.models.rbt_tree import RedBlackTree


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


def test_insert_node_in_rbt():
    """Тест: проверка вставки узла в RedBlackTree."""
    tree = RedBlackTree()
    tree.insert(key=5, value='5')
    tree.insert(key=3, value='3')
    tree.insert(key=4, value='4')
    tree.insert(key=6, value='6')
    root = tree.root
    assert isinstance(root, Node)
    assert root.parent is None
    assert root.right is not None
    assert root.left is not None

