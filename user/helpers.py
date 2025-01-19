import secrets


def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return secrets.SystemRandom().randint(range_start, range_end)
