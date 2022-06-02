from os.path import exists
from sys import argv

from parser import Parser
from solver import *


def solve_file(file_name: str) -> dict:
    if not exists(file_name):
        raise FileNotFoundError()
    with open(file_name) as file:
        text = file.read()
    p = Parser(text)
    commands, variables = p.get_parsed()
    s = create_solver(commands, variables)
    final_values = get_solver_final_values(s, variables)
    return final_values


def main():
    print(solve_file(argv[1]))


if __name__ == '__main__':
    main()
