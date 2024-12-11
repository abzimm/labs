from functools import reduce
from typing import TypeVar, Callable, List

T = TypeVar('T')

def filter_with_reduce(f: Callable[[T], bool], lst: List[T]) -> List[T]:
    return reduce(lambda acc, x: acc + [x] if f(x) else acc, lst, [])

if __name__ == "__main__":
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    print(filter_with_reduce(lambda x: x % 2 == 0, numbers))
    
    words = ["hi", "hello", "hey", "howdy", "greetings"]
    print(filter_with_reduce(lambda x: len(x) > 3, words))