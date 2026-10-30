class DomainError(Exception):
    """
    Базовая ошибка домена. Все пользовательские ошибки домена наследуются от нее.
    """
    def __init__(self, msg: str = 'Базовая ошибка в домене.'):
        self.msg = msg
        super().__init__(msg)


class DuplicateKeyError(DomainError):
    """
    Ошибка: попытка добавить узел с существующим ключом.
    """
    def __init__(self, key):
        self.key = key
        msg = f'Ключ {key} уже существует в дереве. Вставка отменена.'
        super().__init__(msg)


class TreeNotFoundError(DomainError):
    """
    Ошибка: запрошенное дерево не найдено в репозитории.
    """
    def __init__(self, tree_id):
        self.tree_id = tree_id
        message = f"Дерево с идентификатором '{tree_id}' не найдено."
        super().__init__(message)