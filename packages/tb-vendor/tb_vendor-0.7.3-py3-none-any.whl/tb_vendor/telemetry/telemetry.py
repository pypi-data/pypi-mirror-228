from abc import ABC, abstractmethod


class VendorPolling(ABC):
    """Use to poll to the vendor.

    Attributes:
        poll: Poll the vendor.
    """
    @abstractmethod
    def poll(self):
        ...


class Pushing(ABC):
    @abstractmethod
    def push(self):
        ...
