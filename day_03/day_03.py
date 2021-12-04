import typing


def load_data(filename: str) -> (int, typing.List[int]):
    with open(filename) as f:
        num_bits = len(f.readline().strip())
        f.seek(0)
        values = [
            int(line, 2)
            for line in f
        ]
        return num_bits, values


def filter_bits_set(data: typing.List[int], mask: int) -> (typing.List[int], typing.List[int]):
    bits_set = []
    bits_unset = []

    for d in data:
        if mask & d:
            bits_set.append(d)
        else:
            bits_unset.append(d)

    return bits_set, bits_unset


def calculate_power_consumption(data: typing.List[int], bits_len: int) -> (int, int):
    gamma_rate = 0
    epsilon_rate = 0

    data_len_half = len(data) / 2

    for i in range(bits_len - 1, -1, -1):
        mask = 1 << i
        bits_set, bits_unset = filter_bits_set(data, mask)

        if len(bits_set) > data_len_half:
            gamma_rate |= mask
        else:
            epsilon_rate |= mask

    return gamma_rate * epsilon_rate


def calculate_generator_rating(data: typing.List[int],
                               bit_idx: int,
                               selector: typing.Callable[
                                   [typing.List[int], typing.List[int]], typing.List[int]]) -> int:
    if len(data) == 1:
        return data[0]

    mask = 1 << bit_idx
    bits_set, bits_unset = filter_bits_set(data, mask)
    return calculate_generator_rating(selector(bits_set, bits_unset), bit_idx - 1, selector)


def main():
    bits_len, data = load_data('data.txt')

    power_consumption = calculate_power_consumption(data, bits_len)
    print(f'power_consumption = {power_consumption}')

    def _o2_selector(bits_set: typing.List[int], bits_unset: typing.List[int]) -> typing.List[int]:
        return bits_set if len(bits_set) >= len(bits_unset) else bits_unset

    o2_rating = calculate_generator_rating(data, bits_len - 1, _o2_selector)

    def _co2_selector(bits_set: typing.List[int], bits_unset: typing.List[int]) -> typing.List[int]:
        return bits_set if len(bits_set) < len(bits_unset) else bits_unset

    co2_rating = calculate_generator_rating(data, bits_len - 1, _co2_selector)

    life_support_rating = o2_rating * co2_rating
    print(f'life_support_rating = {life_support_rating}')


if __name__ == '__main__':
    main()
