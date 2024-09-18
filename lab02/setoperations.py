def main():
    
    def make_set(data):
        make_list = []
        for item in data:
            if item not in make_list:
                make_list.append(item)
        return make_list

    test_data = [1, 2, 3, 4, 4, 5]
    result = make_set(test_data)
    print(f"Input: {test_data}")
    print(f"Output: {result}")


    def is_set(data):
        if data is None:
            return False
        is_set_list = []
        for item in data:
            if item in is_set_list:
                return False
            is_set_list.append(item)
        return True

    print(is_set([1, 2, 3, 4, 5]))  
    print(is_set([5, 5]))           
    print(is_set([]))               
    print(is_set(None))  


    def union(setA, setB):
        if not is_set(setA) or not is_set(setB):
            return []
        
        result = setA.copy()
        for item in setB:
            if item not in result:
                result.append(item)
        
        return result
    
    print(union([1, 2], [2, 3]))   
    print(union([], [2, 3]))       
    print(union([1, 1, 1], [2, 3])) 


    def intersection(setA, setB):
        if not is_set(setA) or not is_set(setB):
            return []
        
        result = []
        for item in setA:
            if item in setB:
                result.append(item)
        
        return result
    
    print(intersection([1, 2], [2, 3]))   
    print(intersection([], [2, 3]))        
    print(intersection([1, 1, 1], [2, 3])) 

if __name__ == "__main__":
    main()