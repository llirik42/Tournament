import time

import matplotlib.pyplot as plt
from tqdm import tqdm

import strategies
from custom_types import Chain
from custom_types import Strategy, Graph
from utils import construct_graph_a


# функция для уникальности цепочек
def unique_chains(chains: list[Chain]) -> list[Chain]:
    unique = []
    for chain in chains:
        if chain not in unique and list(reversed(chain)) not in unique:
            unique.append(chain)
    return unique


def run_strategy(strategy: Strategy, graph: Graph, launches: int = 20) -> dict[str, float | int]:
    all_chains = []
    times = []

    for i in range(launches):
        start = time.time()
        chains = strategy(graph)
        end = time.time()
        times.append(end - start)
        all_chains.extend(chains)
    avg_time_ms = 1000 * sum(times) / launches

    # Максимальная длина цепочек
    max_length = 0
    for c in all_chains:
        if len(c) > max_length:
            max_length = len(c)

    # Число цепочек с максимальной длиной
    max_length_chains = []
    for c in all_chains:
        if len(c) == max_length:
            max_length_chains.append(c)
    max_length_chains = unique_chains(max_length_chains)

    result = {
        "avg_time_ms": avg_time_ms,
        "max_length": max_length,
        "max_length_count": len(max_length_chains),
    }

    return result


def main():
    plt.rcParams['font.size'] = 20

    m_list = range(100, 999, 10)

    running_settings = [
        # (strategies.min_neighbours_strategy, 5),
        # (strategies.max_neighbours_strategy, 5),
        # (strategies.random_strategy, 20),
        # (strategies.smaller_number_strategy, 5),
        (strategies.max_sum_digits_strategy, 5),
        # (strategies.alternating_strategy, 5)
    ]

    times = {}
    max_lengths = {}

    for strategy, launches in running_settings:
        times[strategy.__name__] = []
        max_lengths[strategy.__name__] = []

    for m in tqdm(m_list):
        graph = construct_graph_a(m)

        for strategy, launches in running_settings:
            running_result = run_strategy(strategy=strategy, graph=graph, launches=launches)
            avg_time_ms = running_result["avg_time_ms"]
            max_length = running_result["max_length"]
            max_length_count = running_result["max_length_count"]
            times[strategy.__name__].append(avg_time_ms)
            max_lengths[strategy.__name__].append(max_length)

    plt.figure()
    for s, _ in running_settings:
        label = s.__name__
        label = label.replace("_strategy", "")
        plt.plot(m_list, times[s.__name__], label=label, linewidth=3)
        plt.xlabel("m")
        plt.ylabel("time (ms)")
        plt.legend()

    plt.figure()
    for s, _ in running_settings:
        label = s.__name__
        label = label.replace("_strategy", "")
        plt.plot(m_list, max_lengths[s.__name__], label=label, linewidth=3)
        plt.xlabel("m")
        plt.ylabel("max length")
        plt.legend()

    plt.show()


main()
