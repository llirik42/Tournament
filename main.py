import strategies
from graph_utils import sieve, n, graph_a, graph_b
import time
import matplotlib.pyplot as plt

#функция для уникальности цепочек
def unique_chains(chains):
    unique = []
    for chain in chains:
        if chain not in unique and list(reversed(chain)) not in unique:
            unique.append(chain)
    return unique


def run_strategy(strategy, graph, launches=20):
    all_chains = []
    times = []

    if strategy.__name__ == "random_strategya":
        for i in range(launches):
            start = time.time()
            chains = strategy(graph)
            end = time.time()
            times.append(end - start)
            all_chains.extend(chains)
        avg_time = sum(times) / launches
    else:
        start = time.time()
        chains = strategy(graph)
        end = time.time()
        all_chains.extend(chains)
        avg_time = end - start

    #макс длина цепочек
    max_length = 0
    for c in all_chains:
        if len(c) > max_length:
            max_length = len(c)

    #число цепочек с макс длиной
    max_chains = []
    for c in all_chains:
        if len(c) == max_length:
            max_chains.append(c)
    max_chains = unique_chains(max_chains)

    print(f"Выбранная стратегия: {strategy.__name__}")
    if strategy.__name__ == "random_strategya":
        print(f"Среднее время выполнения: {avg_time:.5f} сек")
    else:
        print(f"Время выполнения: {avg_time:.5f} сек")
    print(f"Максимальная длина цепочек: {max_length}")
    if strategy.__name__ == "random_strategya" and all_chains:
        avg_length = sum(len(c) for c in all_chains) / len(all_chains)
        print(f"Средняя длина: {avg_length:.3f}")
    print(f"Количество найденных цепочек с этой длиной: {len(max_chains)}")
    print("☆" * 30)

    return avg_time  #для графика среднее время

def main():
    m_list = [20,50,70,80,200,877,1000,2300]
    points = [1, 2]
    strategies_list = [
        strategies.honest_strategy,
        strategies.not_honest_strategy,
        strategies.random_strategy,
        strategies.back_strategy,
        strategies.smaller_number_strategy,
        strategies.max_sum_digits_strategy,
        strategies.alternating_strategy
    ]

    #словарь для хранения времени каждой стратегии
    times_dict = dict()
    for strat in strategies_list:
        times_dict[strat.__name__] = []

    for m in m_list:
        for p in points:
            print("\n" + "☆" * 40)
            print(f"m = {m}, пункт = {p}")
            print("☆" * 40)
            if p == 1:
                all_primes = sieve(m)
                prime_numbers = n(all_primes, m)
                neighbors = graph_a(prime_numbers)
            else:
                prime_numbers = sieve(m)
                neighbors = graph_b(prime_numbers)
            if not neighbors:
                print("Граф пустой")
                for strat in strategies_list:
                    times_dict[strat.__name__].append(None)
                continue

            #запуск стратегий
            for strat in strategies_list:
                if strat.__name__ == "back_strategya" and m > 40:
                    print("дфс стратегия пропущена (слишком долго)")
                    times_dict[strat.__name__].append(None)
                    continue
                avg_time = run_strategy(strat, neighbors, launches=10 if strat.__name__=="random_strategya" else 1)
                times_dict[strat.__name__].append(avg_time)

    #графики
    for strat_name in times_dict:
        t_plot = []
        m_plot = []
        t_list = times_dict[strat_name] #время для стратегии
        i = 0
        while i < len(m_list):
            if t_list[i] is not None:
                m_plot.append(m_list[i])
                t_plot.append(t_list[i])
            i += 1
            
        plt.figure() 
        plt.plot(m_plot, t_plot, marker='*') #х м, у время, звезда
        plt.xlabel("m")
        plt.ylabel("Время выполнения (сек)")
        plt.title(f"Стратегия: {strat_name}")
        plt.grid(True) #сетка
        plt.show()

main()
