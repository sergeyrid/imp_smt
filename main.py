from os.path import exists
from sys import argv

from parser import Parser
from solver import *


def add_constraints(file_name: str, s: Solver, info: str) -> Solver:
    if not exists(file_name):
        raise FileNotFoundError()
    with open(file_name) as file:
        text = file.readlines()
    for line in text:
        (var, op, const) = line.split()
        if op == '==':
            s.add(Int(var + info) == int(const))
        elif op == '>':
            s.add(Int(var + info) > int(const))
        elif op == '<':
            s.add(Int(var + info) < int(const))
    return s


def solve_file(mode: str, prog_file_name: str, input_file_name: str, output_file_name: str):
    if not exists(prog_file_name):
        raise FileNotFoundError()
    with open(prog_file_name) as file:
        text = file.read()
    p = Parser(text)
    commands, variables = p.get_parsed()
    s = create_solver(commands, variables)
    if mode == 'get_final_values':
        s = add_constraints(input_file_name, s, '_start')
        get_final_values(s, variables)
    elif mode == 'check_sat':
        s = add_constraints(input_file_name, s, '_start')
        s = add_constraints(output_file_name, s, '_final')
        check_sat(s)


def main():
    if argv[1] == 'get_final_values':
        solve_file(argv[1], argv[2], argv[3], '')
    elif argv[1] == 'check_sat':
        solve_file(argv[1], argv[2], argv[3], argv[4])


if __name__ == '__main__':
    main()
