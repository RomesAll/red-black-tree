from app.domain.models.node import NodeColor, Node


def test_node_init():
    """Тест: проверка инициализации узла Node."""
    node = Node(key=1, value='some value')
    assert node.key == 1
    assert node.value == 'some value'
    assert not all([node.left, node.right, node.parent]) == True
    assert node.color == NodeColor.RED


def test_node_eq():
    """Тест: сравнение разных узлов."""
    node_1 = Node(key=1, value='some value')
    node_2 = Node(key=2, value='some value')
    node_3 = Node(key=1)
    assert node_1 != node_2
    assert node_1 == node_3