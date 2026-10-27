from app.domain.exceptions import DomainError, DuplicateKeyError, TreeNotFoundError


def test_domain_error_def_msg():
    """Тест: проверка сообщения в базовом исключении"""
    error = DomainError()
    assert str(error) == 'Базовая ошибка в домене.'


def test_duplicate_key_error_message():
    """Тест: проверка, что текст ошибки формируется правильно"""
    error = DuplicateKeyError(key="test_key")
    assert error.key == "test_key"
    assert "test_key" in str(error)
    assert "уже существует" in str(error)


def test_tree_not_found_error_message():
    """Тест: проверка, что текст ошибки формируется правильно при неудачном поиске дерева"""
    error = TreeNotFoundError(tree_id=123)
    assert error.tree_id == 123
    assert "123" in str(error)