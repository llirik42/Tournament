import random

#жадная
def honest_strategy(neighbors):
    all_chains = []
    
    for start in neighbors:
        used = set([start])
        chain = [start]
        current = start

        while True:
            candidates = []
            for x in neighbors[current]:
                if x not in used:
                    candidates.append(x)
            if not candidates:
                break

            next_node = candidates[0]
            for x in candidates:
                if len(neighbors[x]) < len(neighbors[next_node]):
                    next_node = x
            chain.append(next_node)
            used.add(next_node)
            current = next_node
        all_chains.append(chain)

    return all_chains

#жадная наоборот
def not_honest_strategy(neighbors):
    all_chains = []
    
    for start in neighbors:
        used = set([start])
        chain = [start]
        current = start

        while True:
            candidates = []
            for x in neighbors[current]:
                if x not in used:
                    candidates.append(x)
            if not candidates:
                break

            next_node = candidates[0]
            for x in candidates:
                if len(neighbors[x]) > len(neighbors[next_node]): #тут
                    next_node = x
            chain.append(next_node)
            used.add(next_node)
            current = next_node
        all_chains.append(chain)

    return all_chains

#рандом
def random_strategy(neighbors):
    max_length = 0
    longest_chains = []

    for start in neighbors:
        used = set([start])
        chain = [start]
        current = start

        while True:
            candidates = []
            for x in neighbors[current]:
                if x not in used:
                    candidates.append(x)
            if not candidates:
                break

            next_node = random.choice(candidates)
            chain.append(next_node)
            used.add(next_node)
            current = next_node

        if len(chain) > max_length:
            max_length = len(chain)
            longest_chains.clear()
            longest_chains.append(chain)
        elif len(chain) == max_length:
            longest_chains.append(chain)

    return longest_chains

#дфс
def back_strategy(neighbors):
    
    max_length = 0
    longest_chains = []
    def dfs(chain, used):
        nonlocal max_length, longest_chains
        current = chain[-1]

        for neighbor in neighbors[current]:
            if neighbor not in used:
                chain.append(neighbor)
                used.add(neighbor)
                dfs(chain, used)
                chain.pop()
                used.remove(neighbor)

        if len(chain) > max_length:
            max_length = len(chain)
            longest_chains.clear()
            longest_chains.append(chain.copy())
        elif len(chain) == max_length:
            longest_chains.append(chain.copy())
    for start in neighbors:
        dfs([start], set([start]))

    return longest_chains

#меньший сосед
def smaller_number_strategy(neighbors):

    all_chains = []
    for start in neighbors:
        used = set([start])
        chain = [start]
        current = start

        while True:
            candidates = []
            for x in neighbors[current]:
                if x not in used:
                    candidates.append(x)
            if not candidates:
                break

            next_node = candidates[0]
            for x in candidates:
                if x < next_node: #тут
                    next_node = x
            chain.append(next_node)
            used.add(next_node)
            current = next_node
        all_chains.append(chain)

    return all_chains

#максимальная сумма
def sum_digits(n):
    s = 0
    for ch in str(n):
        s += int(ch)
    return s
def max_sum_digits_strategy(neighbors):

    all_chains = []
    for start in neighbors:
        used = set([start])
        chain = [start]
        current = start

        while True:
            candidates = []
            for x in neighbors[current]:
                if x not in used:
                    candidates.append(x)
            if not candidates:
                break

            next_node = candidates[0]
            for x in candidates:
                if sum_digits(x) > sum_digits(next_node): #тут 
                    next_node = x
            chain.append(next_node)
            used.add(next_node)
            current = next_node
        all_chains.append(chain)

    return all_chains
#мин-макс-мин 
def alternating_strategy(neighbors):

    all_chains = []
    for start in neighbors:
        used = set([start])
        chain = [start]
        current = start
        step = 0

        while True:
            candidates = []
            for x in neighbors[current]:
                if x not in used:
                    candidates.append(x)
            if not candidates:
                break

            next_node = candidates[0]
            if step % 2 == 0:
                for x in candidates: #шаг четный — берём максимум
                    if x > next_node:
                        next_node = x
            else:
                for x in candidates: #шаг нечетный — берём минимум
                    if x < next_node:
                        next_node = x
            chain.append(next_node)
            used.add(next_node)
            current = next_node
            step += 1
        all_chains.append(chain)

    return all_chains
