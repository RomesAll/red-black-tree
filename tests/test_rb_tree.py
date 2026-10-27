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
    tree.insert(key=7, value='7')
    tree.insert(key=8, value='8')
    root = tree.root
    assert isinstance(root, Node)
    assert root.key == 4
    assert root.left.key == 3
    assert root.right.key == 6
    assert root.right.left.key == 5
    assert root.right.right.key == 7
    assert root.right.right.right.key == 8


def test_delete_node_from_rbt():
    """Тест: проверка удаления узла в RedBlackTree."""
    tree = RedBlackTree()
    tree.insert(key=5, value='5')
    tree.insert(key=3, value='3')
    tree.insert(key=4, value='4')
    tree.insert(key=6, value='6')
    tree.insert(key=7, value='7')
    tree.insert(key=8, value='8')
    tree.delete(key=6)
    root = tree.root
    assert root.key == 4
    assert root.right.key == 7