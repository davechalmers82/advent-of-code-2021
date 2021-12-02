import argparse
import typing
from dataclasses import dataclass


@dataclass
class Command:
    instruction: str
    value: int

    def __init__(self, data: str):
        instruction, value = data.split()
        self.instruction = instruction
        self.value = int(value)


def load_data(filename: str) -> typing.List[Command]:
    with open(filename) as f:
        return [
            Command(line)
            for line in f
        ]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--use-aim', action='store_true', default=False, help="use aim")
    args = parser.parse_args()

    commands = load_data('data.txt')

    position = 0
    depth = 0
    aim = 0

    for c in commands:
        if c.instruction == 'forward':
            position += c.value
            if args.use_aim:
                depth += aim * c.value

        elif c.instruction == 'down':
            aim += c.value
            if not args.use_aim:
                depth += c.value
        elif c.instruction == 'up':
            aim -= c.value
            if not args.use_aim:
                depth -= c.value
        else:
            raise Exception(f'unhandled command instruction: {c.instruction}')

    print(f'result={position * depth}')


if __name__ == '__main__':
    main()
