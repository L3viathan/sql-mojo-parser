import ply.lex as lex
import ply.yacc as yacc

reserved = [
    'SELECT', 'FROM', 'WHERE', 'LIMIT', 'AND', 'OR', 'ORDER', 'BY',
]

tokens = (
    *reserved,
    'NAME', 'NUMBER', 'STRING',
    'EQUALS', 'LPAREN', 'RPAREN', 'STAR'
)

t_STAR = r'\*'

def t_NAME(t):
    r'[A-Za-z_][A-Za-z0-9_]*'
    # to simplify lexing, we match identifiers and keywords as a single thing
    # if it's a keyword, we change the type to the name of that keyword
    if t.value.upper() in reserved:
        t.type = t.value.upper()
        t.value = t.value.upper()
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r"'([^'\\]+|\\'|\\\\)*'"
    t.value = t.value.replace(r'\\', chr(92)).replace(r"\'", r"'")
    return t

t_EQUALS = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'

t_ignore = " \t\n"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lex.lex()

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQUALS'),
)

def p_empty(p):
    'empty :'
    pass

def p_statement_select(p):
    'statement : select postpositions'
    p[0] = ("select", p[1], p[2])

def p_postpositions(p):
    '''
    postpositions : LIMIT NUMBER postpositions
                  | ORDER BY colspec postpositions
                  | empty
    '''
    if len(p) > 2:
        if p[1] == "LIMIT":
            postposition = {
                "limit": p[2]
            }
            rest = p[3] if p[3] else {}
        elif p[1:3] == ["ORDER", "BY"]:
            postposition = {
                "order by": p[3]
            }
            rest = p[4] if p[4] else {}
        else:
            breakpoint()
        p[0] = {**postposition, **rest}
    else:
        p[0] = {}

def p_select(p):
    'select : SELECT colspec FROM NAME condition'
    p[0] = (p[2], p[4], p[5])

def p_colspec(p):
    '''
    colspec : STAR
            | NAME colspec
            | funcapp colspec
            | empty
    '''
    if len(p) < 3:
        p[0] = p[1]
    elif p[2]:
        p[0] = [p[1], *p[2]]
    else:
        p[0] = [p[1]]

def p_condition(p):
    '''
    condition : WHERE expression
              | empty
    '''
    if len(p) > 2:
        p[0] = p[2]
    else:
        p[0] = None

def p_funcapp(p):
    'funcapp : NAME LPAREN NAME RPAREN'
    p[0] = (p[1], p[3])

def p_expression(p):
    '''
    expression : value
               | expression AND expression
               | expression OR expression
               | expression EQUALS expression
    '''
    if len(p) < 3:
        p[0] = p[1]
    else:
        p[0] = (p[2], p[1], p[3])

def p_value(p):
    '''
    value : NUMBER
          | STRING
          | NAME
    '''
    p[0] = p[1]

def p_error(p):
    print("Error:", p)
    raise RuntimeError

yacc.yacc(start="statement")
print(yacc.parse("SELECT foo FROM bar WHERE a=3 AND b=4 OR c=5 AND d=2 LIMIT 10 ORDER BY bar"))
