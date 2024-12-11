def product_of_digits(x: int) -> int:
    x = abs(x)
    
    if x < 10:
        return x
        
    return (x % 10) * product_of_digits(x // 10)

def array_to_string(a: list, index: int) -> str:
    if index >= len(a):
        return ""
    
    if index == len(a) - 1:
        return str(a[index])
        
    return str(a[index]) + "," + array_to_string(a, index + 1)

def log(base: int, value: int) -> int:
    if base <= 1 or value <= 0:
        raise ValueError("Base must be > 1 and value must be > 0")
        
    if value < base:
        return 0
        
    return 1 + log(base, value // base)

if __name__ == "__main__":

    print("Testing product_of_digits:")
    print("234 ->", product_of_digits(234))
    print("-12 ->", product_of_digits(-12))
    
 
    print("\nTesting array_to_string:")
    test_array = [1, 2, 3, 4, 5]
    print(f"{test_array} ->", array_to_string(test_array, 0))
    

    print("\nTesting log:")
    print("log2(64) ->", log(2, 64))
    print("log10(123456) ->", log(10, 123456))
    

    try:
        print("log(-2, 10) ->", log(-2, 10))
    except ValueError as e:
        print("Caught expected error:", e)