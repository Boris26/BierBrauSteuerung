from abc import ABC, abstractmethod

class IMenuController(ABC):
    @abstractmethod
    def update(self):
        pass
    @abstractmethod
    def clickUpdate(self):
        pass

