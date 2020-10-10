import ply.yacc as yacc
from lex import tokens
import sys


def tab(s):
    return '\t' + '\t'.join(s.splitlines(True))


def p_program(p):
    """program : relation
               | program relation"""
    if len(p) == 3:
        p[0] = p[1] + '\n' + p[2]
    elif len(p) == 2:
        p[0] = p[1]


def p_atom(p):
    """atom : ID
            | ID bracket_atom"""
    if len(p) == 2:
        p[0] = 'atom\n' + tab('identifier = ' + p[1])
    elif len(p) == 3:
        p[0] = 'atom\n' + tab('identifier = ' + p[1] + '\n' + p[2])


def p_id(p):
    """element : LEFTBRACKET disjunction RIGHTBRACKET
               | atom"""
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = p[1]


def p_brackets(p):
    """bracket_atom : LEFTBRACKET bracket_atom RIGHTBRACKET
                    | atom"""
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = p[2]


def p_relation(p):
    """relation : atom DOT
                | atom SHTOPOR disjunction DOT"""
    if len(p) == 3:
        p[0] = 'relation\n' + tab('head\n' + tab(p[1]))
    elif len(p) == 5:
        p[0] = 'relation\n' + tab('head\n' + tab(p[1]) + '\n' + 'body\n' + tab(p[3]))


def p_conjunction(p):
    """conjunction : element COMMA conjunction
                   | element"""
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = 'conjunction\n' + tab(p[1] + '\n' + p[3])


def p_disjunction(p):
    """disjunction : conjunction SEMICOLON disjunction
                   | conjunction"""
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = 'disjunction\n' + tab(p[1] + '\n' + p[3])


def p_error(p):
    if p:
        print("Syntax error: line " + str(p.lineno) + ' col ' + str(p.lexpos) + '.')
        exit(1)
    else:
        print('Syntax error: unexpected end of file.')
        exit(1)


def main(args):
    parser = yacc.yacc()
    filename = args[0]
    with open(filename, 'r') as file:
        result = parser.parse(file.read())
        sys.stdout = open(filename + '.out', 'w')
        print(result)


if __name__ == '__main__':
    main(sys.argv[1:])
