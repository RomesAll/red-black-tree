from dataclasses import dataclass


@dataclass(frozen=True)
class TreeDifference:
    """Объект, описывающий разницу между двумя деревьями."""
    only_in_a: list[int]
    only_in_b: list[int]
    are_identical: bool
