from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from app.domain import RedBlackTree, Node, NodeColor
from app.domain.models import node
from app.infrastructure.db.models import TreeOrm, NodeOrm


class SQLAlchemyTreeRepo:
    """Адаптер репозитория для работы с данными БД через SQLAlchemy"""

    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_id(self, tree_id: UUID) -> RedBlackTree | None:
        """Получить дерево и узлы из бд и сформировать агрегат RedBlackTree"""
        stmt = (
            select(TreeOrm)
            .where(TreeOrm.id == tree_id)
            .options(selectinload(TreeOrm.nodes))
        )
        db_tree = (await self._session.execute(stmt)).scalar_one_or_none()

        if db_tree is None:
            return None

        root_node: Node | None = None

        # Словарь с entity Node узлами без связей
        tree_nodes: dict[int, Node] = {
            node.id: Node(key=node.key, value=node.value, color=NodeColor(node.color))
            for node in db_tree.nodes
        }

        # Восстановление связей parent, left, right
        for node_orm in db_tree.nodes:
            entity_node = tree_nodes.get(node_orm.id)
            entity_node.parent = tree_nodes.get(node_orm.parent_id)
            entity_node.left = tree_nodes.get(node_orm.left_id)
            entity_node.right = tree_nodes.get(node_orm.right_id)

            if entity_node.parent is None:
                root_node = entity_node

        # Создание агрегата RedBlackTree
        tree = RedBlackTree(tree_id=tree_id)
        tree.root = root_node

        return tree

    async def delete(self, tree_id: UUID) -> None:
        """Удалить дерево по id"""
        stmt = (
            delete(TreeOrm)
            .where(TreeOrm.id == tree_id)
        )
        await self._session.execute(stmt)

    @staticmethod
    def _is_structure_changed(domain_node: Node, orm_node: NodeOrm) -> bool:
        """
        Проверяет, изменилась ли структура связей у узла.
        Возвращает True, если нужно делать обновления связей
        """
        # Проверить левого потомка
        domain_left_key = domain_node.left.key if domain_node.left else None
        orm_left_key = orm_node.left.key if orm_node.left else None
        if domain_left_key != orm_left_key:
            return True

        # Проверить правого потомка
        domain_right_key = domain_node.right.key if domain_node.right else None
        orm_right_key = orm_node.right.key if orm_node.right else None
        if domain_right_key != orm_right_key:
            return True

        # Проверить родителя
        domain_parent_key = domain_node.parent.key if domain_node.parent else None
        orm_parent_key = orm_node.parent.key if orm_node.parent else None
        if domain_parent_key != orm_parent_key:
            return True

        return False

    async def _update_tree(self, tree: RedBlackTree, db_tree: TreeOrm) -> None:
        """Обновить существующее дерево"""
        # Словарь с orm моделями
        tree_nodes_orm: dict[int, NodeOrm] = {
            node_orm.key: node_orm
            for node_orm in db_tree.nodes
        }

        # Ключи, которые есть в домене (нужно для удаленных связей)
        domain_keys = set()

        # Обновить данные и создать узлы
        for domain_node in tree.iterative_dfs():
            domain_keys.add(domain_node.key)
            orm_node = tree_nodes_orm.get(domain_node.key)

            # Создание нового узла
            if orm_node is None:
                new_node = NodeOrm(
                    tree_id=tree.tree_id,
                    key=domain_node.key,
                    value=domain_node.value,
                    color=domain_node.color.value,
                )
                self._session.add(new_node)
                tree_nodes_orm.update({new_node.key: new_node})
            else:
                # Если изменений нет, то SQLAlchemy не будет делать update
                orm_node.value = domain_node.value
                orm_node.color = domain_node.color.value

        await self._session.flush()

        for domain_node in tree.iterative_dfs():
            orm_node = tree_nodes_orm[domain_node.key]
            parent_orm = tree_nodes_orm.get(domain_node.parent.key) if domain_node.parent else None
            left_orm = tree_nodes_orm.get(domain_node.left.key) if domain_node.left else None
            right_orm = tree_nodes_orm.get(domain_node.right.key) if domain_node.right else None

            # Если структура изменилась, то обновить связи
            if self._is_structure_changed(domain_node, orm_node):
                orm_node.parent = parent_orm
                orm_node.left = left_orm
                orm_node.right = right_orm

        # Ключи узлов, которые были удалены
        keys_to_delete = set(tree_nodes_orm.keys()) - domain_keys

        if keys_to_delete:
            # Удалить узлы
            await self._session.execute(
                delete(NodeOrm).where(
                    NodeOrm.tree_id == tree.tree_id,
                    NodeOrm.key.in_(keys_to_delete)
                )
            )

        await self._session.flush()

    async def _save_new_tree(self, tree: RedBlackTree) -> None:
        """Сохранить новое дерево"""
        tree_orm = TreeOrm(id=tree.tree_id)
        self._session.add(tree_orm)

        if tree.root is None:
            return

        mapping: dict[Node, NodeOrm] = {}

        # Добавить узлы без связей
        for domain_node in tree.iterative_dfs():
            orm_node = NodeOrm(
                tree_id=tree.tree_id,
                key=domain_node.key,
                value=domain_node.value,
                color=domain_node.color.value
            )
            self._session.add(orm_node)
            mapping[domain_node] = orm_node

        await self._session.flush()

        # Восстановить связи узлов
        for domain_node, orm_node in mapping.items():
            if domain_node.parent:
                orm_node.parent_id = mapping[domain_node.parent].id
                orm_node.parent = mapping[domain_node.parent]
            if domain_node.left:
                orm_node.left_id = mapping[domain_node.left].id
                orm_node.left = mapping[domain_node.left]
            if domain_node.right:
                orm_node.right_id = mapping[domain_node.right].id
                orm_node.right = mapping[domain_node.right]

        await self._session.flush()