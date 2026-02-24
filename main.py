import matplotlib.pyplot as plt

import strategies
from running import run_for_lengths


def main():
    plt.rcParams['font.size'] = 20

    # run_for_time_and_max_length(
    #     m_list=range(1000, 11000, 1000),
    #     point="b",
    #     settings=[
    #         (strategies.min_neighbours_strategy, 5),
    #         (strategies.max_neighbours_strategy, 5),
    #         (strategies.random_strategy, 25),
    #         (strategies.smaller_number_strategy, 5),
    #         (strategies.max_sum_digits_strategy, 5),
    #         (strategies.alternating_strategy, 5)
    #     ]
    # )

    run_for_lengths(
        m=20000,
        point="b",
        settings=[
            (strategies.min_neighbours_strategy, 1),
            (strategies.max_neighbours_strategy, 5),
            (strategies.random_strategy, 25),
            (strategies.smaller_number_strategy, 5),
            (strategies.max_sum_digits_strategy, 5),
            (strategies.alternating_strategy, 5),
            # (strategies.back_tracing_strategy, 5)
        ]
    )


if __name__ == "__main__":
    main()
