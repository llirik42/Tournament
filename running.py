import time
from typing import Any, Iterable, Callable

from matplotlib import pyplot as plt
from tqdm import tqdm

from custom_types import Chain, Strategy, Graph, RunningSettings
from utils import construct_graph_a, construct_graph_b


def _unique_chains(chains: list[Chain]) -> list[Chain]:
    unique = []
    for chain in chains:
        if chain not in unique and list(reversed(chain)) not in unique:
            unique.append(chain)
    return unique


def _run_strategy(strategy: Strategy, graph: Graph, launches: int = 20) -> dict[str, Any]:
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
    lengths = []  # TODO: возвращать не длины цепочек, а сами цепочки (функция run_for_lengths должна всё так же выводить длины, нужно добавить функцию run_for_chains, которая будет принимать m, стратегию, число запусков, пункт a/b и печатать список найденных длинных цепочек (цепочек с максимальной длиной)

    unique_chains = _unique_chains(all_chains)

    for c in unique_chains:
        current_length = len(c)
        lengths.append(current_length)

        if current_length > max_length:
            max_length = current_length

    result = {
        "avg_time_ms": avg_time_ms,
        "max_length": max_length,
        "lengths": lengths,
    }

    return result


def _get_construction_function(point: str) -> Callable[[int], Graph]:
    if point == "a":
        return construct_graph_a
    elif point == "b":
        return construct_graph_b
    else:
        raise ValueError(f"Unknown point: {point}")


def run_for_time_and_max_length(m_list: Iterable[int], point: str, settings: RunningSettings) -> None:
    times = {}
    max_lengths = {}

    for strategy, launches in settings:
        key = strategy.__name__
        times[key] = []
        max_lengths[key] = []

    construction_function = _get_construction_function(point)

    for m in tqdm(m_list):
        graph = construction_function(m)

        for strategy, launches in settings:
            key = strategy.__name__
            running_result = _run_strategy(strategy=strategy, graph=graph, launches=launches)

            avg_time_ms = running_result["avg_time_ms"]
            max_length = running_result["max_length"]

            times[key].append(avg_time_ms)
            max_lengths[key].append(max_length)

    plt.figure()
    for strategy, _ in settings:
        name = strategy.__name__
        label = name.replace("_strategy", "")
        plt.plot(m_list, times[name], label=label, linewidth=3)
        plt.xlabel("m")
        plt.ylabel("time (ms)")
        plt.legend()

    plt.figure()
    for strategy, _ in settings:
        name = strategy.__name__
        label = name.replace("_strategy", "")
        plt.plot(m_list, max_lengths[name], label=label, linewidth=3)
        plt.xlabel("m")
        plt.ylabel("max length")
        plt.legend()

    plt.show()


def run_for_lengths(m: int, point: str, settings: RunningSettings, lengths_to_print: int = 5) -> None:
    construction_function = _get_construction_function(point)
    graph = construction_function(m)

    lengths = {}

    for strategy, launches in tqdm(settings):
        key = strategy.__name__
        running_result = _run_strategy(strategy=strategy, graph=graph, launches=launches)
        lengths[key] = running_result["lengths"]

    indent = " " * 30
    print(f"{indent}{'Length':<15}{'Count':<15}")
    for strategy, _ in settings:
        key = strategy.__name__

        current_strategy_statistics = {}
        for l in lengths[key]:
            if l in current_strategy_statistics:
                current_strategy_statistics[l] += 1
            else:
                current_strategy_statistics[l] = 1

        print(f"{key.capitalize()}")
        for l, n in sorted(current_strategy_statistics.items(), reverse=True, key=lambda x: x[0])[:lengths_to_print]:
            print(f"{indent}{l:<15}{n:<15}")
        print("\n")
