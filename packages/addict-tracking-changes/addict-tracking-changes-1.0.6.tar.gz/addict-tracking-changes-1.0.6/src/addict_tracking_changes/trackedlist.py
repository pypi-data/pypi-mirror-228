"""
A list-like class to track that tracks access
"""
import json
from collections import UserList

import json_fix


class TrackedList(UserList):
    """A subclass of list that allows you to add custom methods and attributes."""

    def __init__(self, *args, **kwargs):
        object.__setattr__(self, "__track_changes", kwargs.pop("track_changes", False))
        super().__init__(*args, **kwargs)

        if object.__getattribute__(self, "__track_changes"):
            object.__setattr__(self, "__tracker", set())

    def __getitem__(self, index):
        """Overwrites the __getitem__ method to do something custom."""
        child_item = super().__getitem__(index)
        if hasattr(self, "__breadcrumb_parent_dict"):
            if object.__getattribute__(self, "__breadcrumb_parent_dict") is not None:
                parent_dict = object.__getattribute__(self, "__breadcrumb_parent_dict")
                parent_key = object.__getattribute__(
                    self, "__breadcrumb_parent_dict_key"
                )

                if isinstance(child_item, dict):
                    object.__setattr__(child_item, "__breadcrumb_parent_dict", self)
                    object.__setattr__(
                        child_item, "__breadcrumb_parent_dict_key", str(index)
                    )
                    # print("dict-within-list: adding parent-breadcrumb-to-dict")

                if isinstance(child_item, TrackedList):
                    # print("assign breadcrumb to UserList object")
                    object.__setattr__(child_item, "__breadcrumb_parent_dict", self)
                    object.__setattr__(
                        child_item, "__breadcrumb_parent_dict_key", str(index)
                    )
                    # print("reconfirm setting breadcrumb: child_item= ", id(child_item))
                    # print("breadcrumb_parent_dict = ",
                    #       object.__getattribute__(child_item, "__breadcrumb_parent_dict")
                    #       )

        return child_item

    def __setitem__(self, index, value):
        """Overwrites the __setitem__ method to do something custom."""
        assert not isinstance(value, list)

        if isinstance(value, dict):
            child_item = value
            object.__setattr__(child_item, "__breadcrumb_parent_dict", self)
            object.__setattr__(child_item, "__breadcrumb_parent_dict_key", str(index))
            return super().__setitem__(index, value)

        # value is scalar -- do the unfolding via breadcrubs
        assert False

    def __json__(self):
        return self.data
