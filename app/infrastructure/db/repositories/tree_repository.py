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