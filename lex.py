import ply.lex as lex

tokens = [
    'ID',
    'DOT',
    'SEMICOLON',
    'COMMA',
    'LEFTBRACKET',
    'RIGHTBRACKET',
    'SHTOPOR'
]

t_ID = r'[a-zA-Z_][a-zA-Z_0-9]*'
t_DOT = '\.'
t_SEMICOLON = ';'
t_COMMA = ','
t_LEFTBRACKET = '\('
t_RIGHTBRACKET = '\)'
t_SHTOPOR = r':-'

t_ignore = ' \t'


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


lexer = lex.lex()
