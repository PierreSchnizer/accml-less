"""Probe backend: similar to view, but addressing can change

It needs rather to address the whole accelerator
Why: there is not always a direct mapping from one
     entity in the "design" view to the "device" view
"""
from abc import ABCMeta, abstractmethod
from typing import Sequence


class BackendR(metaclass=ABCMeta):
    """
    Todo:
        should it contain a trigger method?
    """

    @abstractmethod
    async def trigger(self, dev_id: str, prop_id: str):
        raise NotImplementedError("use base class instead")

    @abstractmethod
    async def read(self, dev_id: str, prop_id: str) -> object:
        raise NotImplementedError("use base class instead")


class BackendRW(BackendR, metaclass=ABCMeta):
    @abstractmethod
    async def set(self, dev_id: str, prop_id: str, value: object):
        raise NotImplementedError("use base class instead")
