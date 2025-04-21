def sum_primes_below_n():
    n = 2000000
    is_prime = [1] * n
    is_prime[0] = 0
    is_prime[1] = 0
    
    i = 2
    while i * i < n:
        if is_prime[i]:
            j = i * i
            while j < n:
                is_prime[j] = 0
                j += i
        i += 1
    
    total = 0
    num = 2
    while num < n:
        if is_prime[num]:
            total += num
        num += 1
    
    return total

result = sum_primes_below_n()
print(result)