from z3 import *
from commands import Command, Variable, GoTo, Stop, Assign
from typing import List


def create_solver(commands: List[Command], variables: List[Variable]):
    lines = Array('lines', IntSort(), IntSort())
    vars = dict()
    s = Solver()
    for var in variables:
        vars[var.name] = Array(var.name, IntSort(), IntSort())
        s.add(vars[var.name][0] == 0)
    s.add(lines[0] == 0)
    i = Int('i')
    goal_i = Int('goal_i')
    s.add(0 <= goal_i)
    s.add(goal_i <= 10)
    for command in commands:
        if isinstance(command, GoTo):
            s.add(ForAll([i], Implies(And(0 <= i, i < goal_i, lines[i] == command.line,
                                          command.condition.evaluate(vars, i)), command.other_line == lines[i + 1])))
            s.add(ForAll([i], Implies(And(0 <= i, i < goal_i, lines[i] == command.line,
                                          Not(command.condition.evaluate(vars, i))), command.line + 1 == lines[i + 1])))
        else:
            s.add(ForAll([i], Implies(And(0 <= i, i < goal_i, lines[i] == command.line),
                                      command.line + 1 == lines[i + 1])))
        if isinstance(command, Stop):
            s.add(ForAll([i], Implies(And(0 <= i, i < goal_i), Not(lines[i] == command.line))))
            s.add(lines[goal_i] == command.line)
        for var in variables:
            if isinstance(command, Assign) and command.var == var:
                s.add(ForAll([i], Implies(And(0 <= i, i < goal_i, lines[i] == command.line),
                                          vars[var.name][i + 1] == command.expr.evaluate(vars, i))))
            else:
                s.add(ForAll([i], Implies(And(0 <= i, i < goal_i, lines[i] == command.line),
                                          vars[var.name][i + 1] == vars[var.name][i])))
    for var in variables:
        final_var = Int(var.name + '_final')
        s.add(final_var == vars[var.name][goal_i])
    return s


def get_solver_final_values(s: Solver, variables: List[Variable]):
    if s.check() is sat:
        values = s.model()
        final_values = dict()
        for var in variables:
            final_var = Int(var.name + '_final')
            final_values[var.name] = values[final_var]
        return final_values
    else:
        print("Unsat!")
        return {}
