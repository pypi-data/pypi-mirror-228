from typing import Dict, Generic, TypeVar, List

T = TypeVar("T")


class AutoDropStack(Generic[T]):
    def __init__(self, max_size: int):
        self.max_size = max_size
        self.__stack: List[T] = []

    @property
    def stack(self) -> List[T]:
        return self.__stack

    def push(self, item: T):
        if len(self.__stack) >= self.max_size:
            self.__stack.pop(0)
        self.__stack.append(item)

    """Return a dictionary of the percentiles of the items in the stack."""

    def percentiles(self) -> Dict[T, float]:
        return {
            item: self.__stack.count(item) / len(self.__stack) for item in self.__stack
        }

    def __str__(self):
        return f"AutoDropStack({self.max_size})"

    def __repr__(self):
        return f"AutoDropStack({self.max_size})"

    def __len__(self):
        return len(self.__stack)

    def __iter__(self):
        return iter(self.__stack)

    def __getitem__(self, index):
        return self.__stack[index]

    def __setitem__(self, index, value):
        self.__stack[index] = value

    def __delitem__(self, index):
        del self.__stack[index]

    def __contains__(self, item):
        return item in self.__stack

    def __reversed__(self):
        return reversed(self.__stack)
