from typing import TypeVar, Callable, List, Dict
from functools import reduce

T = TypeVar('T')
V = TypeVar('V')

def group_by(f: Callable[[T], V], target_list: List[T]) -> Dict[V, List[T]]:
    return reduce(
        lambda acc, x: {**acc, f(x): acc.get(f(x), []) + [x]},
        target_list,
        {}
    )

if __name__ == "__main__":
    test_list = ["hi", "dog", "me", "bad", "good"]
    print(group_by(len, test_list))