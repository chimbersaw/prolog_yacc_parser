#!/usr/bin/env python3
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
            | ID atom_args"""
    if len(p) == 3:
        p[0] = 'atom\n' + tab('identifier = ' + p[1] + '\n' + p[2])
    elif len(p) == 2:
        p[0] = 'identifier = ' + p[1]


def p_atom_args(p):
    """atom_args : ID
                | ID atom_args
                | LBR brackets RBR
                | LBR brackets RBR atom_args"""
    if len(p) == 5:
        p[0] = 'atom\n' + tab(p[2]) + p[4]
    elif len(p) == 4:
        p[0] = 'atom\n' + tab(p[2])
    elif len(p) == 3:
        p[0] = 'identifier = ' + p[1] + '\n' + p[2]
    if len(p) == 2:
        p[0] = 'identifier = ' + p[1]


def p_id(p):
    """element : LBR disjunction RBR
               | atom"""
    if len(p) == 4:
        p[0] = p[2]
    elif len(p) == 2:
        p[0] = p[1]


def p_brackets(p):
    """brackets : LBR brackets RBR
                | ID
                | ID atom_args"""
    if len(p) == 4:
        p[0] = 'atom\n' + tab(p[2])
    elif len(p) == 3:
        p[0] = 'identifier = ' + p[1] + '\n' + p[2]
    elif len(p) == 2:
        p[0] = 'identifier = ' + p[1]


def p_relation(p):
    """relation : atom DOT
                | atom SHTOPOR disjunction DOT"""
    if len(p) == 5:
        p[0] = 'relation\n' + tab('head\n' + tab(p[1]) + '\n' + 'body\n' + tab(p[3]))
    elif len(p) == 3:
        p[0] = 'relation\n' + tab('head\n' + tab(p[1]))


def p_conjunction(p):
    """conjunction : element COMMA conjunction
                   | element"""
    if len(p) == 4:
        p[0] = 'conjunction\n' + tab(p[1] + '\n' + p[3])
    elif len(p) == 2:
        p[0] = p[1]


def p_disjunction(p):
    """disjunction : conjunction SEMICOLON disjunction
                   | conjunction"""
    if len(p) == 4:
        p[0] = 'disjunction\n' + tab(p[1] + '\n' + p[3])
    elif len(p) == 2:
        p[0] = p[1]


def p_error(p):
    if p:
        raise SyntaxError("Syntax error: line " + str(p.lineno) + ', col ' + str(p.lexpos) + '.')
    else:
        raise SyntaxError('Syntax error: unexpected end of file.')


def main(args):
    parser = yacc.yacc()
    filename = args[0]
    out = sys.stdout if "test" in args else open(filename + '.out', 'w')
    with open(filename, 'r') as file:
        try:
            result = parser.parse(file.read())
            print(result, file=out)
        except SyntaxError as e:
            print(e)


if __name__ == '__main__':
    main(sys.argv[1:])
