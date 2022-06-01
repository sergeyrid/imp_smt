from lrparsing import *

from commands import *


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
        plus_expr,
        minus_expr,
        product_expr,
        division_expr,
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


parse_tree = Parser.parse("a = b && c || a;"
                          "while a - 7 < 0 {"
                          "   b = b + 1;"
                          "}; #(This is a comment)"
                          "stop")
print(Parser.repr_parse_tree(parse_tree))




