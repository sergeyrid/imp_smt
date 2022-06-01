from lrparsing import *

from commands import *
from typing import List as ListType


class Parser(Grammar):  # TODO fix everything
    class T(TokenRegistry):
        number = Token(re="[0-9]+")
        variable = Token(re="[A-Za-z_][A-Za-z_0-9]*")
    expr = Ref('expr')
    brackets_expr = '(' << expr << ')'
    plus_expr = expr << '+' << expr
    minus_expr = expr << '-' << expr
    product_expr = expr << '*' << expr
    division_expr = expr << '/' << expr
    equal_expr = expr << '==' << expr
    less_expr = expr << '<' << expr
    and_expr = expr << '&&' << expr
    or_expr = expr << '||' << expr
    not_expr = Token('!') << expr
    atom = T.variable | T.number
    expr = Prio(
        atom,
        brackets_expr,
        product_expr,
        division_expr,
        plus_expr,
        minus_expr,
        not_expr,
        and_expr,
        or_expr,
        less_expr,
        equal_expr
    )
    commands = Ref('commands')
    while_command = Keyword('while') + expr + '{' + commands + '}'
    if_command = Keyword('if') + expr + '{' + commands + '}' + Keyword('else') + '{' + commands + '}'
    stop_command = Keyword('stop')
    assign_command = T.variable + '=' + expr
    commands = List(while_command | if_command | stop_command | assign_command, ';', opt=True)
    START = commands

    variables = dict()

    def __init__(self, text: str):
        super(Parser, self).__init__()
        self.text = text

    def parse_expr(self, tree: tuple) -> Expression:
        if tree[0] is Parser.expr or tree[0] is Parser.atom:
            return self.parse_expr(tree[1])
        if tree[0] is Parser.brackets_expr:
            return self.parse_expr(tree[1])
        if tree[0] is Parser.T.variable:
            name = tree[1]
            if name not in self.variables:
                self.variables[name] = Variable(name)
            return VariableValue(name)
        if tree[0] is Parser.T.number:
            return Constant(Type.NAT, int(tree[1]))
        if tree[0] is Parser.product_expr:
            expr1 = self.parse_expr(tree[1])
            expr2 = self.parse_expr(tree[3])
            return Product(expr1, expr2)
        if tree[0] is Parser.division_expr:
            expr1 = self.parse_expr(tree[1])
            expr2 = self.parse_expr(tree[3])
            return Division(expr1, expr2)
        if tree[0] is Parser.plus_expr:
            expr1 = self.parse_expr(tree[1])
            expr2 = self.parse_expr(tree[3])
            return Plus(expr1, expr2)
        if tree[0] is Parser.minus_expr:
            expr1 = self.parse_expr(tree[1])
            expr2 = self.parse_expr(tree[3])
            return Minus(expr1, expr2)
        if tree[0] is Parser.not_expr:
            return Not(self.parse_expr(tree[2]))
        if tree[0] is Parser.and_expr:
            expr1 = self.parse_expr(tree[1])
            expr2 = self.parse_expr(tree[3])
            return And(expr1, expr2)
        if tree[0] is Parser.or_expr:
            expr1 = self.parse_expr(tree[1])
            expr2 = self.parse_expr(tree[3])
            return Or(expr1, expr2)
        if tree[0] is Parser.less_expr:
            expr1 = self.parse_expr(tree[1])
            expr2 = self.parse_expr(tree[3])
            return Less(expr1, expr2)
        if tree[0] is Parser.equal_expr:
            expr1 = self.parse_expr(tree[1])
            expr2 = self.parse_expr(tree[3])
            return Equal(expr1, expr2)

    def parse_commands(self, tree: tuple, line: int) -> ListType[Command]:
        if tree[0] is Parser.commands:
            answer = []
            for i in range(1, len(tree), 2):
                new_lines = self.parse_commands(tree[i], line)
                line = new_lines[-1].line + 1
                answer += new_lines
            return answer
        if tree[0] is Parser.stop_command:
            return [Stop(line)]
        if tree[0] is Parser.assign_command:
            name = tree[1][1]
            if name not in self.variables:
                self.variables[name] = Variable(name)
            expr = self.parse_expr(tree[3])
            return [Assign(line, self.variables[name], expr)]
        if tree[0] is Parser.if_command:
            expr = Not(self.parse_expr(tree[2]))
            new_line = line + 1
            commands1 = self.parse_commands(tree[4], new_line)
            if len(commands1) != 0:
                new_line = commands1[-1].line + 1
            commands2 = self.parse_commands(tree[8], new_line)
            goto: Command = GoTo(line, expr, new_line)  # FIXME
            return [goto] + commands1 + commands2
        if tree[0] is Parser.while_command:
            expr = Not(self.parse_expr(tree[2]))
            new_line = line + 1
            commands = self.parse_commands(tree[4], new_line)
            if len(commands) != 0:
                new_line = commands[-1].line + 1
            goto1: Command = GoTo(line, expr, new_line + 1)  # FIXME
            goto2: Command = GoTo(new_line, Constant(Type.BOOL, True), line) # FIXME
            return [goto1] + commands + [goto2]

    def get_parsed(self) -> tuple:
        tree = Parser.parse(self.text)
        commands = self.parse_commands(tree[1], 0)
        return commands, self.variables


parser = Parser("a = a && b;"
                "while a - 7 < 0 {"
                "   b = b + 1;"
                "   stop;"
                "   stop;"
                "   stop;"
                "};"
                "stop;"
                "stop;"
                "stop;"
                "stop;"
                "stop;"
                "stop;"
                "stop;")

for command in parser.get_parsed()[0]:
    print(command)
