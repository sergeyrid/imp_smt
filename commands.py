from enum import Enum


class Type(Enum):
    BOOL = 0
    NAT = 1


class Expression:
    def __init__(self, expr_type: Type) -> None:
        self.type = expr_type

    def evaluate(self) -> None:  # TODO choose correct return type
        pass


class Plus(Expression):
    def __init__(self, e1: Expression, e2: Expression) -> None:
        super(Plus, self).__init__(Type.NAT)
        self.e1 = e1
        self.e2 = e2


class Minus(Expression):
    def __init__(self, e1: Expression, e2: Expression) -> None:
        super(Minus, self).__init__(Type.NAT)
        self.e1 = e1
        self.e2 = e2


class VariableValue(Expression):
    def __init__(self, name: str) -> None:
        super(VariableValue, self).__init__(Type.NAT)
        self.name = name


class And(Expression):
    def __init__(self, e1: Expression, e2: Expression) -> None:
        super(And, self).__init__(Type.BOOL)
        self.e1 = e1
        self.e2 = e2


class Or(Expression):
    def __init__(self, e1: Expression, e2: Expression) -> None:
        super(Or, self).__init__(Type.BOOL)
        self.e1 = e1
        self.e2 = e2


class Not(Expression):
    def __init__(self, e: Expression) -> None:
        super(Not, self).__init__(Type.BOOL)
        self.e = e


class Variable:
    def __init__(self, name: str) -> None:
        self.name = name


class Command:
    def __init__(self, line: int) -> None:
        self.line = line


class Assign(Command):
    def __init__(self, line: int, var: Variable, expr: Expression) -> None:
        super(Assign, self).__init__(line)
        self.var = var
        self.expr = expr


class GoTo(Command):
    def __init__(self, line: int, condition: Expression,
                 other_line: int) -> None:
        super(GoTo, self).__init__(line)
        self.condition = condition
        self.other_line = other_line
