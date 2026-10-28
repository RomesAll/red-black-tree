import pytest
from app.domain.models.rbt_tree import RedBlackTree


@pytest.fixture(scope='function')
def setup_rbt_a() -> RedBlackTree:
    """Фикстура для получения красно-черного дерева с узлами."""
    tree = RedBlackTree()
    tree.insert(key=5, value='5')
    tree.insert(key=3, value='3')
    tree.insert(key=4, value='4')
    tree.insert(key=6, value='6')
    tree.insert(key=7, value='7')
    tree.insert(key=8, value='8')
    return tree


@pytest.fixture(scope='function')
def setup_rbt_b() -> RedBlackTree:
    """Фикстура для получения красно-черного дерева с узлами."""
    tree = RedBlackTree()
    tree.insert(key=54, value='54')
    tree.insert(key=90, value='90')
    tree.insert(key=22, value='22')
    tree.insert(key=6, value='6')
    tree.insert(key=7, value='7')
    tree.insert(key=8, value='8')
    return tree