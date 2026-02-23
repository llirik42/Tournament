from typing import Callable

Graph = dict[int, list[int]]


def _get_prime_numbers(m: int) -> list[int]:
    """
    Функция использует решето Эратосфена.
    """

    is_prime = [True] * (m + 1)

    for i in range(2, m + 1):
        if is_prime[i]:
            for j in range(i * i, m + 1, i):
                is_prime[j] = False

    prime_numbers = []
    for i in range(2, m + 1):
        if is_prime[i]:
            prime_numbers.append(i)

    return prime_numbers


def get_prime_numbers_a(m: int) -> list[int]:
    all_prime_numbers = _get_prime_numbers(m)
    lower_limit = 10 ** (len(str(m)) - 1)
    result = []

    for x in all_prime_numbers:
        if x >= lower_limit:
            result.append(x)

    return result


def get_prime_numbers_b(m: int) -> list[int]:
    return _get_prime_numbers(m)


def _are_similar_a(a: int, b: int) -> bool:
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


def _are_similar_b(a: int, b: int) -> bool:
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


def _get_graph(prime_numbers: list[int], are_similar: Callable[[int, int], bool]) -> Graph:
    graph = {}

    for i in range(len(prime_numbers)):
        for j in range(i + 1, len(prime_numbers)):
            n1 = prime_numbers[i]
            n2 = prime_numbers[j]
            if are_similar(n1, n2):
                if n1 not in graph:
                    graph[n1] = []
                if n2 not in graph:
                    graph[n2] = []
                graph[n1].append(n2)
                graph[n2].append(n1)

    return graph


def get_graph_a(prime_numbers: list[int]) -> Graph:
    return _get_graph(prime_numbers, _are_similar_a)


def get_graph_b(prime_numbers: list[int]) -> Graph:
    return _get_graph(prime_numbers, _are_similar_b)
