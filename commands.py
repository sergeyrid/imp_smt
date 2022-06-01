from enum import Enum
from typing import Union
from z3 import And as zAnd, Or as zOr, Not as zNot


class Type(Enum):
    BOOL = 0
    NAT = 1


class Expression:
    def __init__(self, expr_type: Type) -> None:
        self.type = expr_type

    def evaluate(self, vars: dict, i: int) -> Union[int, bool]:
        pass


class VariableValue(Expression):
    def __init__(self, name: str) -> None:
        super(VariableValue, self).__init__(Type.NAT)
        self.name = name

    def evaluate(self, vars: dict, i: int) -> int:
        return vars[self.name][i]

    def __repr__(self) -> str:
        return repr(f'{self.name}')


class Constant(Expression):
    def __init__(self, expr_type: Type, value: Union[int, bool]) -> None:
        super(Constant, self).__init__(expr_type)
        self.value = value

    def evaluate(self, vars: dict, i: int) -> Union[int, bool]:
        return self.value

    def __repr__(self) -> str:
        return repr(f'{self.value}')


class Plus(Expression):
    def __init__(self, e1: Expression, e2: Expression) -> None:
        super(Plus, self).__init__(Type.NAT)
        self.e1 = e1
        self.e2 = e2

    def evaluate(self, vars: dict, i: int) -> int:
        return self.e1.evaluate(vars, i) + self.e2.evaluate(vars, i)

    def __repr__(self) -> str:
        return repr(f'({self.e1} + {self.e2})')


class Minus(Expression):
    def __init__(self, e1: Expression, e2: Expression) -> None:
        super(Minus, self).__init__(Type.NAT)
        self.e1 = e1
        self.e2 = e2

    def evaluate(self, vars: dict, i: int) -> int:
        return self.e1.evaluate(vars, i) - self.e2.evaluate(vars, i)

    def __repr__(self) -> str:
        return repr(f'({self.e1} - {self.e2})')


class Product(Expression):
    def __init__(self, e1: Expression, e2: Expression) -> None:
        super(Product, self).__init__(Type.NAT)
        self.e1 = e1
        self.e2 = e2

    def evaluate(self, vars: dict, i: int) -> int:
        return self.e1.evaluate(vars, i) * self.e2.evaluate(vars, i)

    def __repr__(self) -> str:
        return repr(f'({self.e1} * {self.e2})')


class Division(Expression):
    def __init__(self, e1: Expression, e2: Expression) -> None:
        super(Division, self).__init__(Type.NAT)
        self.e1 = e1
        self.e2 = e2

    def evaluate(self, vars: dict, i: int) -> int:
        return self.e1.evaluate(vars, i) // self.e2.evaluate(vars, i)

    def __repr__(self) -> str:
        return repr(f'({self.e1} / {self.e2})')


class Equal(Expression):
    def __init__(self, e1: Expression, e2: Expression) -> None:
        super(Equal, self).__init__(Type.BOOL)
        self.e1 = e1
        self.e2 = e2

    def evaluate(self, vars: dict, i: int) -> bool:
        return self.e1.evaluate(vars, i) == self.e2.evaluate(vars, i)

    def __repr__(self) -> str:
        return repr(f'({self.e1} == {self.e2})')


class Less(Expression):
    def __init__(self, e1: Expression, e2: Expression) -> None:
        super(Less, self).__init__(Type.BOOL)
        self.e1 = e1
        self.e2 = e2

    def evaluate(self, vars: dict, i: int) -> bool:
        return self.e1.evaluate(vars, i) < self.e2.evaluate(vars, i)

    def __repr__(self) -> str:
        return repr(f'({self.e1} < {self.e2})')


class And(Expression):
    def __init__(self, e1: Expression, e2: Expression) -> None:
        super(And, self).__init__(Type.BOOL)
        self.e1 = e1
        self.e2 = e2

    def evaluate(self, vars: dict, i: int) -> bool:
        return zAnd(self.e1.evaluate(vars, i), self.e2.evaluate(vars, i))

    def __repr__(self) -> str:
        return repr(f'({self.e1} && {self.e2})')


class Or(Expression):
    def __init__(self, e1: Expression, e2: Expression) -> None:
        super(Or, self).__init__(Type.BOOL)
        self.e1 = e1
        self.e2 = e2

    def evaluate(self, vars: dict, i: int) -> bool:
        return zOr(self.e1.evaluate(vars, i), self.e2.evaluate(vars, i))

    def __repr__(self) -> str:
        return repr(f'({self.e1} || {self.e2})')


class Not(Expression):
    def __init__(self, e: Expression) -> None:
        super(Not, self).__init__(Type.BOOL)
        self.e = e

    def evaluate(self, vars: dict, i: int) -> bool:
        print(self.e.evaluate(vars, i))
        return zNot(self.e.evaluate(vars, i))

    def __repr__(self) -> str:
        return repr(f'!({self.e})')


class Variable:
    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return repr(self.name)


class Command:
    def __init__(self, line: int) -> None:
        self.line = line


class Assign(Command):
    def __init__(self, line: int, var: Variable, expr: Expression) -> None:
        super(Assign, self).__init__(line)
        self.var = var
        self.expr = expr

    def __repr__(self) -> str:
        return repr(f'{self.line}: {self.var.name} = {self.expr}')


class GoTo(Command):
    def __init__(self, line: int, condition: Expression,
                 other_line: int) -> None:
        super(GoTo, self).__init__(line)
        self.condition = condition
        self.other_line = other_line

    def __repr__(self) -> str:
        return repr(f'{self.line}: {self.condition} => goto {self.other_line}')


class Stop(Command):
    def __init__(self, line: int) -> None:
        super(Stop, self).__init__(line)

    def __repr__(self) -> str:
        return repr(f'{self.line}: stop')

