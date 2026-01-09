from abc import ABC, abstractmethod


class Figure(ABC):
    @abstractmethod
    def draw(self) -> None:
        raise NotImplementedError
        
class Rectangle(Figure):
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        
rec = Rectangle(5, 2)