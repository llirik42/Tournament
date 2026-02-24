import random

from custom_types import Graph, Chain


def min_neighbours_strategy(graph: Graph) -> list[Chain]:
    all_chains = []

    for start in graph:
        used = {start}
        chain = [start]
        current = start

        while True:
            candidates = []
            for x in graph[current]:
                if x not in used:
                    candidates.append(x)
            if not candidates:
                break

            next_node = candidates[0]
            for x in candidates:
                if len(graph[x]) < len(graph[next_node]):
                    next_node = x
            chain.append(next_node)
            used.add(next_node)
            current = next_node

        all_chains.append(chain)

    return all_chains


def max_neighbours_strategy(graph: Graph) -> list[Chain]:
    all_chains = []

    for start in graph:
        used = {start}
        chain = [start]
        current = start

        while True:
            candidates = []
            for x in graph[current]:
                if x not in used:
                    candidates.append(x)
            if not candidates:
                break

            next_node = candidates[0]
            for x in candidates:
                if len(graph[x]) > len(graph[next_node]):
                    next_node = x
            chain.append(next_node)
            used.add(next_node)
            current = next_node

        all_chains.append(chain)

    return all_chains


def random_strategy(graph: Graph) -> list[Chain]:
    all_chains = []

    for start in graph:
        used = {start}
        chain = [start]
        current = start

        while True:
            candidates = []
            for x in graph[current]:
                if x not in used:
                    candidates.append(x)
            if not candidates:
                break

            next_node = random.choice(candidates)
            chain.append(next_node)
            used.add(next_node)
            current = next_node

        all_chains.append(chain)

    return all_chains


def smaller_number_strategy(graph: Graph) -> list[Chain]:
    all_chains = []
    for start in graph:
        used = {start}
        chain = [start]
        current = start

        while True:
            candidates = []
            for x in graph[current]:
                if x not in used:
                    candidates.append(x)
            if not candidates:
                break

            next_node = candidates[0]
            for x in candidates:
                if x < next_node:
                    next_node = x
            chain.append(next_node)
            used.add(next_node)
            current = next_node

        all_chains.append(chain)

    return all_chains


digits_sums = {}


# TODO: действительно ли мемоизация даёт прирост по времени при запуске на одном m
def _sum_digits(n):
    # Мемоизация

    global digits_sums

    if n in digits_sums:
        return digits_sums[n]

    n_copy = n
    s = 0

    while n_copy > 0:
        s += n_copy % 10
        n_copy //= 10

    digits_sums[n] = s

    return s


def max_sum_digits_strategy(graph: Graph) -> list[Chain]:
    all_chains = []
    for start in graph:
        used = {start}
        chain = [start]
        current = start

        while True:
            candidates = []
            for x in graph[current]:
                if x not in used:
                    candidates.append(x)
            if not candidates:
                break

            next_node = candidates[0]
            for x in candidates:
                if _sum_digits(x) > _sum_digits(next_node):
                    next_node = x
            chain.append(next_node)
            used.add(next_node)
            current = next_node

        all_chains.append(chain)

    return all_chains


def alternating_strategy(graph: Graph) -> list[Chain]:
    all_chains = []
    for start in graph:
        used = {start}
        chain = [start]
        current = start
        step = 0

        while True:
            candidates = []
            for x in graph[current]:
                if x not in used:
                    candidates.append(x)
            if not candidates:
                break

            next_node = candidates[0]
            if step % 2 == 0:
                for x in candidates:  # шаг четный — берём максимум
                    if x > next_node:
                        next_node = x
            else:
                for x in candidates:  # шаг нечетный — берём минимум
                    if x < next_node:
                        next_node = x
            chain.append(next_node)
            used.add(next_node)
            current = next_node
            step += 1

        all_chains.append(chain)

    return all_chains


def back_tracing_strategy(graph: Graph) -> list[Chain]:
    max_length = 0
    longest_chains = []

    def dfs(chain, used):
        nonlocal max_length, longest_chains
        current = chain[-1]

        for neighbor in graph[current]:
            if neighbor not in used:
                chain.append(neighbor)
                used.add(neighbor)
                dfs(chain, used)
                chain.pop()
                used.remove(neighbor)

        # Здесь фильтрация нужна, так как эта стратегия вернёт вообще все пути в графе (слишком много!)
        if len(chain) > max_length:
            max_length = len(chain)
            longest_chains.clear()
            longest_chains.append(chain.copy())
        elif len(chain) == max_length:
            longest_chains.append(chain.copy())

    for start in graph:
        dfs([start], {start})

    return longest_chains
