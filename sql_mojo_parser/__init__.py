import ply.lex as lex
import ply.yacc as yacc

from pprint import pprint

reserved = [
    'SELECT', 'FROM', 'WHERE', 'LIMIT', 'AND', 'OR', 'ORDER', 'BY', 'NOT'
]

tokens = (
    *reserved,
    'NAME', 'NUMBER', 'STRING',
    'EQUALS', 'LPAREN', 'RPAREN', 'STAR', 'COMMA'
)

t_STAR = r'\*'
t_COMMA = r','

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
    t.value = t.value.replace(r'\\', chr(92)).replace(r"\'", r"'")[1:-1]
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
    ('left', 'NOT'),
    ('left', 'EQUALS'),
)

def p_empty(p):
    'empty :'
    pass

def p_statement_select(p):
    'statement : select postpositions'
    p[0] = {**p[1], **p[2]}

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
    'select : SELECT colspec FROM value condition'
    p[0] = {
        "type": "select",
        "columns": p[2],
        "table": p[4],
    }
    if p[5]:
        p[0]["condition"] = p[5]

def p_colspec(p):
    '''
    colspec : STAR
            | NAME
            | function
            | NAME COMMA colspec
            | function COMMA colspec
    '''
    rest = p[3] if len(p) > 3 else []
    if p[1] == "*":
        p[0] = [{"type": "star"}]
    elif isinstance(p[1], dict) and p[1].get("type") == "function":
        p[0] = [p[1], *rest]
    elif p[1]:
        p[0] = [
            {
                "type": "name",
                "value": p[1],
            },
            *rest,
        ]
    else:
        p[0] = []

def p_condition(p):
    '''
    condition : WHERE expression
              | empty
    '''
    if len(p) > 2:
        p[0] = p[2]
    else:
        p[0] = None

def p_function(p):
    'function : NAME LPAREN value RPAREN'
    p[0] = {
        "type": "function",
        "value": {
            "name": p[1],
            "arg": p[3],
        },
    }

def p_expression(p):
    '''
    expression : value
               | expression AND expression
               | expression OR expression
               | expression EQUALS expression
               | NOT expression
               | LPAREN expression RPAREN
    '''
    if len(p) < 3:
        p[0] = p[1]
    elif len(p) == 3:  # not
        p[0] = {
            "op": "not",
            "args": [p[2]],
        }
    elif p[1] == "(":
        p[0] = p[2]
    else:
        p[0] = {
            "op": p[2].lower(),
            "args": [p[1], p[3]],
        }

def p_value(p):
    '''
    value : NUMBER
          | STRING
          | NAME
    '''
    p[0] = {
        "type": "name" if p.slice[1].type == "NAME" else "literal",
        "value": p[1],
    }

def p_error(p):
    raise SyntaxError("Invalid mojo-sql statement")

yacc.yacc(start="statement")
