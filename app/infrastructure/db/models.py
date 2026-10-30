from uuid import UUID
import sqlalchemy
from sqlalchemy import MetaData, Date, func, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
from datetime import datetime


class BaseOrm(DeclarativeBase):
    """Базовая ORM модель SQLAlchemy"""

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now()
    )


class TreeOrm(BaseOrm):
    """ORM модель для хранения информации о дереве Tree"""

    __tablename__ = 'trees'

    id: Mapped[UUID] = mapped_column(
        sqlalchemy.Uuid,
        primary_key=True,
        index=True
    )

    # Связи relationship
    nodes: Mapped[list["NodeOrm"]] = relationship(
        back_populates="tree",
        cascade="all, delete-orphan"
    )


class NodeOrm(BaseOrm):
    """ORM модель для хранения Node узлов дерева"""

    __tablename__ = 'nodes'

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    # Связь с деревом
    tree_id: Mapped[UUID] = mapped_column(
        sqlalchemy.Uuid,
        ForeignKey('trees.id', ondelete='CASCADE')
    )

    # Данные узла
    key: Mapped[int] = mapped_column(index=True)
    value: Mapped[str | None] = mapped_column(String(255), nullable=True)
    color: Mapped[str] = mapped_column(String(10), default="RED")

    # Связи внутри дерева
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey('nodes.id', ondelete='SET NULL'),
        nullable=True
    )
    left_id: Mapped[int | None] = mapped_column(
        ForeignKey('nodes.id', ondelete='SET NULL'),
        nullable=True
    )
    right_id: Mapped[int | None] = mapped_column(
        ForeignKey('nodes.id', ondelete='SET NULL'),
        nullable=True
    )

    # Связи relationship
    tree: Mapped["TreeOrm"] = relationship(back_populates="nodes")

    parent: Mapped["NodeOrm | None"] = relationship(
        foreign_keys=[parent_id],
        remote_side="NodeOrm.id",
        post_update=True
    )

    left: Mapped["NodeOrm | None"] = relationship(
        foreign_keys=[left_id],
        remote_side="NodeOrm.id",
        post_update=True
    )

    right: Mapped["NodeOrm | None"] = relationship(
        foreign_keys=[right_id],
        remote_side="NodeOrm.id",
        post_update=True
    )