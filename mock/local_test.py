import math


def estimate_nth_prime_upper_bound(n: int):
    if n < 6:
        return 15
    
    log_n = math.log(n)
    log_log_n = math.log(log_n)
    
    if n < 100:
        return int(n * (log_n + log_log_n) * 1.5)
    elif n < 1000:
        return int(n * (log_n + log_log_n) * 1.3)
    elif n >= 8009824:
        return int(n * (log_n + log_log_n - 1 + 1.8 * log_log_n / log_n))
    else:
        return int(n * (log_n + log_log_n - 1 + 2.0 * log_log_n / log_n))


def odd_dig_primes(n: int) -> list[int]: 
    nums = {k: True for k in range(2, n+1)}
    
    for num, is_checkable in nums.items():
        if not is_checkable:
            continue
            
        if nums[2]: 
            nums[2] = False
        
        for x in range(num * num, n, num):
            nums[x] = False
    
    primes = len([x for x in nums.items() if x[1]])
    max_prime = max([x[0] for x in nums.items() if x[1]])
    
    upper_bound = estimate_nth_prime_upper_bound(primes+1)
    print(upper_bound)
    nums2 = {k: True for k in range(2, upper_bound)}

    for num, is_checkable in nums2.items():
        if not is_checkable:
            continue
            
        if nums2[2]: 
            nums2[2] = False
        
        for x in range(num * num, upper_bound, num):
            nums2[x] = False
            
    print([x for x in nums2.items() if x[1]])

    next_prime_after_max = [x[0] for x in nums2.items() if x[1]][-1]

    return [
        primes, 
        max_prime, 
        next_prime_after_max
    ]
            
print(odd_dig_primes(13))