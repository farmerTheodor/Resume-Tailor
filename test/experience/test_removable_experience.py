import pytest
from pydantic import BaseModel


from src.experience.removable_experience import (
    get_all_removable_experience,
    remove_experience,
)


class RemovableItem(BaseModel):
    rank: int
    value: str


def test_gets_all_removable_experience_singular():
    removable_item = RemovableItem(rank=1, value="test")

    removable_experience = get_all_removable_experience(removable_item)
    assert len(removable_experience) == 1
    assert removable_experience[0] == removable_item


def test_gets_all_removable_experience_list():
    removable_item1 = RemovableItem(rank=1, value="test1")
    removable_item2 = RemovableItem(rank=2, value="test2")
    all_items = [removable_item1, removable_item2, 1, 2]

    removable_experience = get_all_removable_experience(all_items)

    assert len(removable_experience) == 2
    assert removable_item1 in removable_experience
    assert removable_item2 in removable_experience


def test_gets_all_removable_experience_dict():
    removable_item1 = RemovableItem(rank=1, value="test1")
    removable_item2 = RemovableItem(rank=2, value="test2")
    all_items = {"item1": removable_item1, "item2": removable_item2, "not_removable": 1}

    removable_experience = get_all_removable_experience(all_items)

    assert len(removable_experience) == 2
    assert removable_item1 in removable_experience
    assert removable_item2 in removable_experience


def test_gets_all_removable_experience_nested():
    removable_item1 = RemovableItem(rank=1, value="test1")
    removable_item2 = RemovableItem(rank=2, value="test2")

    class NestedModel(BaseModel):
        name: str
        experience: RemovableItem
        all_items: list

    all_items = NestedModel(
        name="Nested", experience=removable_item1, all_items=[removable_item2, 1, 2]
    )

    removable_experience = get_all_removable_experience(all_items)

    assert len(removable_experience) == 2
    assert removable_item1 in removable_experience
    assert removable_item2 in removable_experience


def test_removal_of_item_from_list():
    removable_item1 = RemovableItem(rank=1, value="test1")
    removable_item2 = RemovableItem(rank=2, value="test2")
    all_items = [removable_item1, removable_item2, 1, 2]

    all_items = remove_experience(all_items, removable_item1)

    assert len(all_items) == 3
    assert all_items == [removable_item2, 1, 2]
