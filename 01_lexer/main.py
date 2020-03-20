import ply.lex as lex

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
    'funcIDENT'
]

reserved = {
  'define' : 'DEFINE',
  'end' :'END',
  'begin' : 'BEGIN',
  'each' : 'EACH',
  'select' : 'SELECT'
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
t_COMMA  = r','
t_DOT = r'\.'
t_PIPE  = r'\|'
t_DOUBLEPLUS = r'\+\+'
t_DOUBLEMULT = r'\*\*'
t_DOUBLEDOT  = r'\.\.'
t_COLON = r':'
t_EQ  = r'='
t_NOTEQ = r'!='
t_LT  = r'<'
t_LTEQ  = r'<='
t_GT  = r'>'
t_GTEQ  = r'>='
t_MOD  = r'%'

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
    t.type = reserved[ t.value ]
  return t

def t_constIDENT(t):
  r'[A-Z]+[^[a-z]'
  if t.value in reserved:
    t.type = reserved[ t.value ]
  return t

def t_tupleIDENT(t):
  r'<[a-z]+>'
  if t.value in reserved:
    t.type = reserved[ t.value ]
  return t

def t_funcIDENT(t):
  r'[A-Z]{1}([a-z]|[0-9]|_)+'
  if t.value in reserved:
    t.type = reserved[ t.value ]
  return t

def t_newline(t):
  r'\n+'
  t.lexer.lineno += len(t.value)

t_ignore  = '\n \r\t'
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

def main():
    while True:
        command = input()
        task = command.split(' ')[0]
        if (task == "-h" or task == "--help"):
            print("usage: main.py [-h] [--who | -f FILE]\n-h, --help  show this help message and exit\n --who  print out student IDs and NAMEs of authors\n -f FILE, --file FILE  filename to process")
            break
        elif (task == "--who"):
            print("Evgeniia Onosovskaia, 281251")
        elif ((task == "-f" or task == "--file") and len(command.split(' ')) == 2):
            file_name = command.split(' ')[1]
            try:
                with open(file_name, 'r', encoding='utf-8') as INFILE:
                    data = INFILE.read()
                    build_lexer(data)
            except:
                print("Some error in file reading occur. Try again!")
        else:
          print("Incorrect command, please try again!")


main()