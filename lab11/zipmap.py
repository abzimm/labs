from typing import List, TypeVar, Dict, Any

T = TypeVar('T')
V = TypeVar('V')

def zipmap(key_list: List[T], value_list: List[V], override: bool = False) -> Dict[T, V]:
    if not override and len(key_list) != len(set(key_list)):
        return {}
        
    pairs = list(map(lambda k, v: (k, v), 
                    key_list, 
                    value_list if len(value_list) >= len(key_list) 
                    else value_list + [None] * (len(key_list) - len(value_list))))
                    
    return dict(pairs if not override else reversed(pairs))

if __name__ == "__main__":
    list_1 = ['a', 'b', 'c', 'd', 'e', 'f']
    list_2 = [1, 2, 3, 4, 5, 6]
    print(zipmap(list_1, list_2))
    
    print(zipmap([1, 2, 3, 2], [4, 5, 6, 7], True))
    print(zipmap([1, 2, 3], [4, 5, 6, 7, 8]))
    print(zipmap([1, 3, 5, 7], [2, 4, 6]))