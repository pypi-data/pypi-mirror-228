from typing import Dict, Generic, TypeVar, List, Iterator

T = TypeVar("T")


class AutoDropStack(Generic[T]):
    """
    A stack-like data structure that automatically drops the oldest item
    when the maximum size is reached.

    Parameters:
        max_size (int): The maximum number of items the stack can hold.
    """

    def __init__(self, max_size: int):
        """
        Initializes a new AutoDropStack instance.

        Args:
            max_size (int): The maximum number of items the stack can hold.
        """
        self.max_size = max_size
        self.__stack: List[T] = []

    @property
    def stack(self) -> List[T]:
        """
        Returns the current items in the stack.

        Returns:
            List[T]: The list of items in the stack.
        """
        return self.__stack

    def push(self, item: T):
        """
        Adds an item to the stack. If the stack's size exceeds the maximum,
        the oldest item is dropped.

        Args:
            item (T): The item to be added to the stack.
        """
        if len(self.__stack) >= self.max_size:
            self.__stack.pop(0)
        self.__stack.append(item)

    def percentiles(self) -> Dict[T, float]:
        """
        Returns a dictionary of the percentiles of the items in the stack.

        Returns:
            Dict[T, float]: A dictionary where keys are items in the stack and
            values are their respective percentiles.
        """
        return {
            item: self.__stack.count(item) / len(self.__stack) for item in self.__stack
        }

    def __str__(self) -> str:
        return f"AutoDropStack({self.max_size})"

    def __repr__(self) -> str:
        return f"AutoDropStack({self.max_size})"

    def __len__(self) -> int:
        return len(self.__stack)

    def __iter__(self) -> Iterator[T]:
        return iter(self.__stack)

    def __getitem__(self, index) -> T:
        return self.__stack[index]

    def __setitem__(self, index, value):
        self.__stack[index] = value

    def __delitem__(self, index):
        del self.__stack[index]

    def __contains__(self, item) -> bool:
        return item in self.__stack

    def __reversed__(self) -> Iterator[T]:
        return reversed(self.__stack)
