#!/usr/bin/env python3
import ply.lex as lex

tokens = [
    'ID',
    'DOT',
    'SEMICOLON',
    'COMMA',
    'LBR',
    'RBR',
    'SHTOPOR'
]

t_ID = r'[a-zA-Z_][a-zA-Z_0-9]*'
t_DOT = '\.'
t_SEMICOLON = ';'
t_COMMA = ','
t_LBR = '\('
t_RBR = '\)'
t_SHTOPOR = r':-'

t_ignore = ' \t'


def t_error(t):
    raise SyntaxError("Illegal character '%s'" % t.value[0])


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


lexer = lex.lex()
