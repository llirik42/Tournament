def sieve(m):  # то же самое решето
    all_prime_numbers = []
    for i in range(m + 1):
        all_prime_numbers.append(True)
    for i in range(2, m + 1):
        if all_prime_numbers[i]:
            for j in range(i * i, m + 1, i):
                all_prime_numbers[j] = False
    prime_numbers = []
    for i in range(2, m + 1):
        if all_prime_numbers[i]:
            prime_numbers.append(i)

    return prime_numbers


def n(prime_numbers, m):  # оставляем только нужной длины
    min_value = 10 ** (len(str(m)) - 1)
    result = []
    for x in prime_numbers:
        if x >= min_value:
            result.append(x)

    return result


def proverka(a, b):  # пункт а
    a = str(a)
    b = str(b)
    if len(a) != len(b):
        return False
    a_digits = [ch for ch in a]
    b_digits = [ch for ch in b]
    diff_count = 0
    b_new = b_digits.copy()
    for digit in a_digits:
        if digit in b_new:
            b_new.remove(digit)
        else:
            diff_count += 1
    diff_count += len(b_new)

    return diff_count == 2


def proverka_b(a, b):  # пункт б
    a = str(a)
    b = str(b)
    if len(a) < len(b):
        a, b = b, a
    if (len(a) - len(b)) != 1:
        return False
    for i in range(len(a)):
        candidate = ""
        for j in range(len(a)):
            if j != i:
                candidate += a[j]
        if candidate == b:
            return True
    return False


def graph_a(prime_numbers):
    neighbors = {}
    for i in range(len(prime_numbers)):
        for j in range(i + 1, len(prime_numbers)):
            n1 = prime_numbers[i]
            n2 = prime_numbers[j]
            if proverka(n1, n2):
                if n1 not in neighbors:
                    neighbors[n1] = []
                if n2 not in neighbors:
                    neighbors[n2] = []
                neighbors[n1].append(n2)
                neighbors[n2].append(n1)

    return neighbors


def graph_b(prime_numbers):
    neighbors = {}
    for i in range(len(prime_numbers)):
        for j in range(i + 1, len(prime_numbers)):
            n1 = prime_numbers[i]
            n2 = prime_numbers[j]
            if proverka_b(n1, n2):
                if n1 not in neighbors:
                    neighbors[n1] = []
                if n2 not in neighbors:
                    neighbors[n2] = []
                neighbors[n1].append(n2)
                neighbors[n2].append(n1)

    return neighbors

