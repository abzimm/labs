import time
from functools import wraps

def memoize(func):
    cache = {}
    @wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper

def recur_fibo(n: int) -> int:
    if n <= 1:
        return n
    else:
        return recur_fibo(n-1) + recur_fibo(n-2)

@memoize
def memoized_fibo(n: int) -> int:
    if n <= 1:
        return n
    else:
        return memoized_fibo(n-1) + memoized_fibo(n-2)

if __name__ == '__main__':
    n = 35
    start_time = time.time()
    result1 = recur_fibo(n)
    original_time = time.time() - start_time
    
    start_time = time.time()
    result2 = memoized_fibo(n)
    memoized_time = time.time() - start_time
    
    print(f"\nPerformance comparison for n = {n}:")
    print(f"Original recursive time: {original_time:.4f} seconds")
    print(f"Memoized recursive time: {memoized_time:.4f} seconds")
    
    if memoized_time > 0:
        print(f"Speed improvement: {original_time/memoized_time:.1f}x faster")
    else:
        print(f"Speed improvement: >100000x faster (memoized time too small to measure)")
    
    print(f"Both implementations returned: {result1} (verified: {result1 == result2})")