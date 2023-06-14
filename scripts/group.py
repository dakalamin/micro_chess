import typing


T = typing.TypeVar('T', bound=typing.Hashable)

class Group(typing.Generic[T]):
    def __init__(self, elements: typing.Iterable[T]|None=None) -> None:
        self.distinct: set[T] = set()
        self.repeated: set[T] = set()
        
        if elements is not None:
            self.group(elements)
    
    def group(self, elements: typing.Iterable[T]) -> typing.Self:
        for element in elements:
            if element in self.repeated:
                continue

            updated_set = self.repeated if element in self.distinct else self.distinct
            updated_set.add(element)
                
        return self