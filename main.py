from os.path import exists
from sys import argv
from z3 import Int

from parser import Parser
from solver import check_sat, create_solver, get_final_values, Solver


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


def solve_file(mode: str, prog_file_name: str, input_file_name: str,
               output_file_name: str) -> None:
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
    elif mode == 'get_formula':
        print(s)


def main() -> None:
    if len(argv) <= 2:
        print('Not enough input arguments, expected at least 1')
        return
    mode = argv[1]
    prog_file_name = argv[2]
    input_file_name = ''
    if len(argv) >= 4:
        input_file_name = argv[3]
    output_file_name = ''
    if len(argv) >= 5:
        output_file_name = argv[4]
    solve_file(mode, prog_file_name, input_file_name, output_file_name)


if __name__ == '__main__':
    main()
