import argparse
import sys
import typing


# Part 1 - Window size 1
# Part 2 - Window size 3

def load_data(filename: str) -> typing.List[int]:
    with open(filename) as f:
        return [
            int(line)
            for line in f
        ]


def sum_ints(int_list: typing.List[int]) -> int:
    total = 0
    for i in int_list:
        total += i
    return total


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--window_size', type=int, default=1, help="sliding window size")
    args = parser.parse_args()

    depths = load_data('data.txt')

    increase_count = 0
    previous_window_depth = sys.maxsize

    for idx, _ in enumerate(depths):
        if idx + args.window_size <= len(depths):
            window = depths[idx:idx + args.window_size]
            window_depth = sum_ints(window)

            if window_depth > previous_window_depth:
                increase_count += 1

            previous_window_depth = window_depth

    print(f'increase_count={increase_count}')


if __name__ == '__main__':
    main()
