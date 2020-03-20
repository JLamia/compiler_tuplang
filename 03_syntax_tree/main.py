import ply.lex as lex
import ply.yacc as yacc
import tree_print

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
    'SPACE'
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
t_SPACE = r'\s'

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


class ASTnode:
    def __init__(self, typestr):
        self.nodetype = typestr


def p_program(p):
    '''program : regexp_function_or_variable_definition return_value DOT'''
    p[0] = ASTnode('program')
    p[0].child_return = p[2]
    p[0].child_vars = p[1]


def p_regexp_func_or_var_single(p):
    '''regexp_function_or_variable_definition : function_or_variable_definition'''
    p[0] = ASTnode('regexp')
    p[0].children_vars = [p[1]]


def p_regexp_function_or_variable_definition(p):
    '''regexp_function_or_variable_definition : regexp_function_or_variable_definition function_or_variable_definition'''
    p[0] = p[1]
    p[0].children_vars.append(p[2])


def p_function_or_variable_definition(p):
    '''function_or_variable_definition : variable_definition
    | function_definition'''
    p[0] = p[1]


def p_function_definition(p):
    '''function_definition : DEFINE funcIDENT LSQUARE regexp_formals RSQUARE BEGIN regexp_variable_definition return_value DOT END DOT'''
    print("func_definition( {0} )".format(p[2]))
    p[0] = ASTnode('function_definition')
    p[0].value = p[2]
    p[0].children_formals = [p[4]]
    p[0].children_vars = [p[7]]
    p[0].child_return = p[8]


def p_regexp_variable_single(p):
    '''regexp_variable_definition : variable_definition'''
    p[0] = p[1]
    p[0].children_vars = []


def p_regexp_variable_definition(p):
    '''regexp_variable_definition : regexp_variable_definition variable_definition'''
    p[0] = p[1]
    p[0].children_vars.append(p[2])


def p_variable_definition(p):
    '''variable_definition : simple_variable_definition
    | constant_definition
    | tuplevariable_definition
    | pipe_definition'''
    p[0] = p[1]


def p_simple_variable_definition(p):
    '''simple_variable_definition : varIDENT LARROW simple_expression DOT'''
    print("variable_definition( {0} )".format(p[1]))
    p[0] = ASTnode('variable_defintion')
    p[0].value = p[1]
    p[0].child_expr = p[3]


def p_constant_definition(p):
    '''constant_definition : constIDENT LARROW constant_expression DOT'''
    print("constant_definition( {0} )".format(p[1]))
    p[0] = ASTnode('constant_definition')
    p[0].child_expr = p[3]


def p_tuplevariable_definition(p):
    '''tuplevariable_definition : tupleIDENT LARROW tuple_expression DOT'''
    print("tuplevariable_definition( {0} )".format(p[1]))
    p[0] = ASTnode('tuplevariable_definition')
    p[0].child_expr = p[3]


def p_pipe_definition(p):
    '''pipe_definition : pipe_expression RARROW tupleIDENT DOT'''
    print("pipe_expression")
    p[0] = ASTnode('pipe_definition')
    p[0].child_expr = p[3]
    # p[0].value = p[3]


def p_regexp_formals(p):
    '''regexp_formals : formals
    | '''


def p_formals(p):
    '''formals : regexp_COMMA_varIDENT
              | varIDENT'''
    p[0] = ASTnode('formals')
    p[0].child_var = p[1]


def p_single_regex_verIDENT(p):
    '''regexp_COMMA_varIDENT : varIDENT'''
    p[0].children_vars = [p[1]]


def p_regexp_COMMA_varIDENT(p):
    '''regexp_COMMA_varIDENT : regexp_COMMA_varIDENT COMMA varIDENT'''
    p[0] = p[1]
    p[0].children_vars.append(p[3])


def p_return_value(p):
    '''return_value : EQ simple_expression
    | NOTEQ pipe_expression'''
    p[0] = ASTnode('return_value')
    p[0].child_expr = p[2]


def p_constant_expression(p):
    '''constant_expression : constIDENT
    | NUMBER_LITERAL'''
    p[0] = ASTnode('conatant_expression')
    p[0].value = p[1]


def p_define_pipe_operation(p):
    '''define_pipe_operation : pipe_expression PIPE pipe_operation'''
    p[0] = ASTnode('pipe_expression')
    p[0].child_opr = p[3]


def p_pipe_expression(p):
    '''pipe_expression : tuple_expression
                          | define_pipe_operation'''
    p[0] = p[1]


def p_pipe_operation(p):
    '''pipe_operation : funcIDENT
                 | MULT
                 | PLUS
                 | each_statement'''
    p[0] = ASTnode(p[1])


def p_each_statement(p):
    '''each_statement : EACH COLON funcIDENT'''
    p[0] = ASTnode('each_statement')
    p[0].value = p[3]


def p_tuple_expression(p):
    '''tuple_expression : tuple_atom regexp_tuple_operation'''
    p[0] = ASTnode('tuple_expression')
    p[0].child_atm = p[1]
    # p[0].value = p[1].value


def p_tuple_op_single(p):
    '''tuple : tuple_operation tuple_atom'''
    p[0] = ASTnode('tuple_operations')
    p[0].chilren_op = [p[1]]
    p[0].children_atm = [p[2]]


def p_tuple_op_more(p):
    '''tuple : tuple_operation tuple_atom tuple'''
    p[0] = p[3]
    p[0].children_op.append(p[1])
    p[0].children_atm.append(p[2])


def p_regexp_tuple_operation(p):
    '''regexp_tuple_operation : tuple regexp_tuple_operation
                       | '''


def p_tuple_operation(p):
    '''tuple_operation : DOUBLEPLUS'''


def p_atom_DOUPLEOP(p):
    '''atom_DOUBLEOP : LSQUARE constant_expression DOUBLEMULT constant_expression RSQUARE
                    | LSQUARE constant_expression DOUBLEDOT  constant_expression RSQUARE'''
    p[0] = ASTnode('tuple_atom_DOUBLEOP')
    p[0].children_exprs = [p[2], p[4]]


def p_atom_arguments(p):
    '''atom_arguments : LSQUARE arguments RSQUARE'''
    p[0] = ASTnode('tuple_atom_arguments')
    p[0].child_arg = p[2]


def p_atom_tupleIDENT(p):
    '''p_atom_tupleIDENT : tupleIDENT'''
    p[0] = ASTnode('tupleIDENT')
    p[0].value = p[1]


def p_tuple_atom(p):
    '''tuple_atom : tupleIDENT
     | function_call
     | atom_DOUBLEOP
     | atom_arguments'''
    p[0] = p[1]


def p_function_call(p):
    '''function_call : funcIDENT LSQUARE regexp_arguments RSQUARE'''
    print("function_call( {0} )".format(p[2]))
    p[0] = ASTnode('function_call')
    p[0].value = p[1]
    p[0].args = p[3]


def p_regexp_arguments(p):
    '''regexp_arguments : arguments
    | '''


def p_arguments(p):
    '''arguments : simple_expression regexp_COMMA_simple_expression
  '''
    p[0] = ASTnode('arguments')
    p[0].child_expr = p[1]


def p_comma_expr_single(p):
    '''comma_expr : COMMA simple_expression'''
    p[0] = ASTnode('comma_expr')
    p[0].children_expr = [p[2]]


def p_comma_expr_more(p):
    '''comma_expr : comma_expr COMMA simple_expression'''
    p[0] = p[1]
    p[0].children_expr.append(p[3])


def p_regexp_COMMA_simple_expression(p):
    '''regexp_COMMA_simple_expression : comma_expr regexp_COMMA_simple_expression
                       |'''


def p_atom_with_value(p):
    '''atom_with_value : NUMBER_LITERAL
    | STRING_LITERAL
    | varIDENT
    | constIDENT'''
    print("atom( {0} )".format(p[1]))
    p[0] = ASTnode('atom')
    p[0].value = p[1]
    # p[0] = p[1].value
    # p[0] = p[1].value


def p_atom_simple_expr(p):
    '''atom_simple_expr : LPAREN simple_expression RPAREN'''
    p[0] = p[2]


def p_atom_const_expr(p):
    '''atom_const_expr : SELECT COLON constant_expression LSQUARE tuple_expression RSQUARE'''
    p[0] = ASTnode('atom_const_expression')
    p[0].children_exprs = [p[3], p[5]]


def p_atom_without_value(p):
    '''atom_without_value : function_call
    | atom_simple_expr
    | atom_const_expr'''
    print("atom")
    p[0] = p[1]


def p_atom(p):
    '''atom : atom_with_value
    | atom_without_value'''
    p[0] = p[1]


def p_MINUS_atom(p):
    '''MINUS_atom : MINUS atom'''
    p[0] = p[2]


def p_factor(p):
    '''factor : MINUS_atom
                | atom'''
    print("factor")
    p[0] = ASTnode('factor')
    p[0].child_atom = p[1]


def p_regexp_MINUS(p):
    '''regexp_MINUS : MINUS
    | '''


def p_mult_div_factor(p):
    '''mult_div_factor : factor regexp_MULT_DIV_factor'''
    p[0] = p[1]


def p_term(p):
    '''term : mult_div_factor
            | factor'''
    print("term")
    p[0] = ASTnode('term')
    p[0].children_factors = [p[1]]


def p_mult_div_fact_h_single(p):
    '''regexp_MULT_DIV_factor_h : MULT_DIV factor'''
    p[0] = ASTnode('mult_div_factor')
    p[0].children_facrtos = [p[2]]


def p_mult_div_fact_h_multi(p):
    '''regexp_MULT_DIV_factor_h : regexp_MULT_DIV_factor MULT_DIV factor'''
    p[0] = p[1]
    p[0].append([3])


def p_regexp_MULT_DIV_factor(p):
    '''regexp_MULT_DIV_factor : regexp_MULT_DIV_factor_h
                       | '''


def p_MULT_DIV(p):
    '''MULT_DIV : MULT
                | DIV'''


def p_simple_expression(p):
    '''simple_expression : term regexp_PLUS_MINUS_term
                         | term'''
    print('simple_expression')
    p[0] = ASTnode('simple_expression')
    p[0].child_term = p[1]


def p_regexp_plus_minus_term_h_single(p):
    '''regexp_PLUS_MINUS_term : PLUS_MINUS term'''
    p[0] = ASTnode('plus_minus_term')
    p[0].children_terms = [p[2]]


def p_regexp_PLUS_MINUS_term(p):
    '''regexp_PLUS_MINUS_term : regexp_PLUS_MINUS_term PLUS_MINUS term'''
    p[0] = p[1]
    p[0].children_terms.append(p[3])


def p_PLUS_MINUS(p):
    '''PLUS_MINUS : PLUS
    | MINUS'''
    p[0] = ASTnode('plus_minus')
    p[0].value = p[1]  # MAY CAUSE ERROR


def p_error(p):
    print("syntax error", p)
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
                    outformat = "unicode"
                    tree_print.treeprint(result, outformat)
                    if (result is None):
                        print("syntax OK")
            except:
                print("Some error in file reading occur. Try again!")
        else:
            print("Incorrect command, please try again!")


main()
