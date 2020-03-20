import ply.lex as lex
import ply.yacc as yacc

tokens = [
    'LPAREN',
    'RPAREN',
    'LARROW',
    'RARROW',
    'LSQUARE',
    'RSQUARE',
    'COMMA',
    'DOT',
    'PIPE',
    'DOUBLEPLUS',
    'DOUBLEMULT',
    'DOUBLEDOT',
    'COLON',
    'EQ',
    'NOTEQ',
    'LT',
    'LTEQ',
    'GT',
    'GTEQ',
    'PLUS',
    'MINUS',
    'MULT',
    'DIV',
    'MOD',
    'DIVIDE',
    'TIMES',
    'NUMBER_LITERAL',
    'STRING_LITERAL',
    'varIDENT',
    'constIDENT',
    'tupleIDENT',
    'funcIDENT',
    'PROGRAM',
    'FACTOR',
    'FORMALS',
    'TERM',
    'FUNCTION_DEFINITION',
    'TUPLE_ATOM',
    'FUNCTION_CALL',
    'SIMPLE_EXPRESSION',
    'PIPE_EXPRESSION',
    'ARGUMENTS',
    'CONSTANT_EXPRESSION',
]

reserved = {
    'define': 'DEFINE',
    'end': 'END',
    'begin': 'BEGIN',
    'each': 'EACH',
    'select': 'SELECT'
}

tokens += reserved.values()

t_END = r'end'
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULT = r'\*'
t_DIV = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LARROW = r'<-'
t_RARROW = r'->'
t_LSQUARE = r'\['
t_RSQUARE = r'\]'
t_COMMA = r','
t_DOT = r'\.'
t_PIPE = r'\|'
t_DOUBLEPLUS = r'\+\+'
t_DOUBLEMULT = r'\*\*'
t_DOUBLEDOT = r'\.\.'
t_COLON = r':'
t_EQ = r'='
t_NOTEQ = r'!='
t_LT = r'<'
t_LTEQ = r'<='
t_GT = r'>'
t_GTEQ = r'>='
t_MOD = r'%'

'''def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in reserved:
        t.type = reserved[ t.value ]
    return t
'''


def t_NUMBER_LITERAL(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_STRING_LITERAL(t):
    r'\".*\"'
    return t


def t_varIDENT(t):
    r'[a-z]{1}([a-z]|[A-Z]|[0-9]|_)+'
    if t.value in reserved:
        t.type = reserved[t.value]
    return t


def t_constIDENT(t):
    r'\b[A-Z]+\b'
    if t.value in reserved:
        t.type = reserved[t.value]
    return t


def t_tupleIDENT(t):
    r'<[a-z]+>'
    if t.value in reserved:
        t.type = reserved[t.value]
    return t


def t_funcIDENT(t):
    r'[A-Z]{1}([a-z]|[0-9]|_)+'
    if t.value in reserved:
        t.type = reserved[t.value]
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


t_ignore = '\n \r\t'
t_ignore_COMMENT = r'{.*}'


def build_lexer(data):
    lexer = lex.lex()
    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok:
            break  # No more input
        print(tok)


def t_error(t):
    print("Illegal character %s at line %d" % (t.value[0], t.lineno))
    t.lexer.skip(all)


def p_program(p):
    '''program : regexp_function_or_variable_definition return_value DOT'''


def p_function_definition(p):
    '''function_definition : DEFINE funcIDENT LSQUARE regexp_formals RSQUARE BEGIN regexp_variable_definition return_value DOT END DOT'''
    print("func_definition( {0} )".format(p[2]))


def p_variable_definition(p):
    '''variable_definition : simple_variable_definition
    | constant_definition
    | tuplevariable_definition
    | pipe_definition'''


def p_simple_variable_definition(p):
    '''simple_variable_definition : varIDENT LARROW simple_expression DOT'''
    print("variable_definition( {0} )".format(p[1]))


def p_constant_definition(p):
    '''constant_definition : constIDENT LARROW constant_expression DOT'''
    print("constant_definition( {0} )".format(p[1]))


def p_tuplevariable_definition(p):
    '''tuplevariable_definition : tupleIDENT LARROW tuple_expression DOT'''
    print("tuplevariable_definition( {0} )".format(p[1]))


def p_pipe_definition(p):
    '''pipe_definition : pipe_expression RARROW tupleIDENT DOT'''
    print("pipe_expression")


def p_regexp_variable_definition(p):
    '''regexp_variable_definition : variable_definition regexp_variable_definition
    | variable_definition '''


def p_function_or_variable_definition(p):
    '''function_or_variable_definition : variable_definition
    | function_definition'''


def p_regexp_function_or_variable_definition(p):
    '''regexp_function_or_variable_definition : function_or_variable_definition
                                            | function_or_variable_definition regexp_function_or_variable_definition'''


def p_regexp_formals(p):
    '''regexp_formals : formals
    | '''


def p_formals(p):
    '''formals : varIDENT regexp_COMMA_varIDENT
                | varIDENT'''


def p_regexp_COMMA_varIDENT(p):
    '''regexp_COMMA_varIDENT : COMMA varIDENT regexp_COMMA_varIDENT
    | COMMA varIDENT'''


def p_return_value(p):
    '''return_value : EQ simple_expression
    | NOTEQ pipe_expression'''


def p_constant_expression(p):
    '''constant_expression : constIDENT
    | NUMBER_LITERAL'''


def p_pipe_expression(p):
  '''pipe_expression : tuple_expression
                        | pipe_expression PIPE pipe_operation'''



def p_regexp_pipe_operation(p):
    '''regexp_pipe_operation : PIPE pipe_operation regexp_pipe_operation
    | '''


def p_pipe_operation(p):
    '''pipe_operation : funcIDENT
                 | MULT
                 | PLUS
                 | each_statement'''


def p_each_statement(p):
    '''each_statement : EACH COLON funcIDENT'''


def p_tuple_expression(p):
    '''tuple_expression : tuple_atom regexp_tuple_operation'''


def p_regexp_tuple_operation(p):
    '''regexp_tuple_operation : tuple_operation tuple_atom regexp_tuple_operation
                       | '''


def p_tuple_operation(p):
    '''tuple_operation : DOUBLEPLUS'''


def p_tuple_atom(p):
    '''tuple_atom : tupleIDENT
     | function_call
     | LSQUARE constant_expression DOUBLEMULT constant_expression RSQUARE
     | LSQUARE constant_expression DOUBLEDOT  constant_expression RSQUARE
     | LSQUARE arguments RSQUARE'''


def p_function_call(p):
    '''function_call : funcIDENT LSQUARE regexp_arguments RSQUARE'''
    print("function_call( {0} )".format(p[2]))


def p_regexp_arguments(p):
    '''regexp_arguments : arguments
    | '''


def p_arguments(p):
    '''arguments : simple_expression regexp_COMMA_simple_expression
 '''


def p_regexp_COMMA_simple_expression(p):
    '''regexp_COMMA_simple_expression : COMMA simple_expression regexp_COMMA_simple_expression
                       |'''


def p_atom_with_value(p):
    '''atom_with_value : NUMBER_LITERAL
    | STRING_LITERAL
    | varIDENT
    | constIDENT'''
    print("atom( {0} )".format(p[1]))


def p_atom_without_value(p):
    '''atom_without_value : function_call
    | LPAREN simple_expression RPAREN
    | SELECT COLON constant_expression LSQUARE tuple_expression RSQUARE'''
    print("atom")


def p_atom(p):
    '''atom : atom_with_value
    | atom_without_value'''


def p_factor(p):
    '''factor : MINUS atom
                | atom'''
    print("factor")


def p_regexp_MINUS(p):
    '''regexp_MINUS : MINUS
    | '''


def p_term(p):
    '''term : factor regexp_MULT_DIV_factor
            | factor'''
    print("term")


def p_regexp_MULT_DIV_factor(p):
    '''regexp_MULT_DIV_factor : MULT_DIV factor regexp_MULT_DIV_factor
                       | '''


def p_MULT_DIV(p):
    '''MULT_DIV : MULT
                | DIV'''


def p_simple_expression(p):
    '''simple_expression : term regexp_PLUS_MINUS_term
                         | term'''
    print('simple_expression')


def p_regexp_PLUS_MINUS_term(p):
    '''regexp_PLUS_MINUS_term : PLUS_MINUS term regexp_PLUS_MINUS_term
                       | PLUS_MINUS term'''


def p_PLUS_MINUS(p):
    '''PLUS_MINUS : PLUS
    | MINUS'''


def p_error(p):
    print("syntax error" , p)
    raise SystemExit

parser = yacc.yacc()

def main():
    # file_name = input()
    while True:
        command = input()
        task = command.split(' ')[0]
        if (task == "-h" or task == "--help"):
            print(
                "usage: main.py [-h] [--who | -f FILE]\n-h, --help  show this help message and exit\n --who  print out student IDs and NAMEs of authors\n -f FILE, --file FILE  filename to process")
            break
        elif (task == "--who"):
            print("Evgeniia Onosovskaia, 281251")
        elif ((task == "-f" or task == "--file") and len(command.split(' ')) == 2):
            file_name = command.split(' ')[1]
            try:
                with open(file_name, 'r', encoding='utf-8') as INFILE:
                    data = INFILE.read()
                    lexer0 = lex.lex()
                    lexer0.input(data)
                    result = parser.parse(data, lexer=lexer0, debug=False)
                    # print(result)
                    if (result is None):
                        print("syntax OK")
            except:
                print("Some error in file reading occur. Try again!")
        else:
            print("Incorrect command, please try again!")


main()
