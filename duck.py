# -----------------------------------------------------------------------------
# calc.py
# -----------------------------------------------------------------------------

import sys
sys.path.append('../..')

from sly import Lexer, Parser

class CalcLexer(Lexer):
        # Set of token names.   This is always required
    tokens = { INTNUMBER, FLOATNUMBER, ID, 
               VAR, IF, ELSE, PRINT, INT, FLOAT, PROGRAM,
               PLUS, MINUS, TIMES, DIVIDE, ASSIGN,
               EQ, LT, LE, GT, GE, NE }


    literals = { '(', ')', '{', '}', ';', ':', ',' }

    # String containing ignored characters
    ignore = ' \t'

    # Regular expression rules for tokens
    PLUS    = r'\+'
    MINUS   = r'-'
    TIMES   = r'\*'
    DIVIDE  = r'/'
    ASSIGN  = r'='
    EQ      = r'=='
    NE      = r'<>'
    LE      = r'<='
    LT      = r'<'
    GE      = r'>='
    GT      = r'>'

    
    @_(r'[0-9]+\.[0-9]+')
    def FLOATNUMBER(self, t):
        t.value = float(t.value)
        return t

    @_(r'\d+')
    def INTNUMBER(self, t):
        t.value = int(t.value)
        return t

    # Identifiers and keywords
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ID['var'] = VAR
    ID['if'] = IF
    ID['else'] = ELSE
    ID['print'] = PRINT
    ID['int'] = INT
    ID['float'] = FLOAT
    ID['program'] = PROGRAM

    ignore_comment = r'\#.*'

    # Line number tracking
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print('Line %d: Bad character %r' % (self.lineno, t.value[0]))
        self.index += 1

class CalcParser(Parser):
    # Get the token list from the lexer (required)
    tokens = CalcLexer.tokens
    
    def __init__(self):
        self.ids = { }
    '''
    @_('VAR var1')
    def vars(self, p):
        return p.var1
    
    @_('ID "," var1')
    def var1(self, p):
        self.ids[p.ID] = 0
        return p.var1

    @_('":" tipo ";"')
    def var1(self, p):
        self.ids[p.ID] = 0

    @_('INT')
    def tipo(self, p):
        return 'int'

    @_('FLOAT')
    def tipo(self, p):
        return 'float'

    @_('ID ASSIGN expres ";"')
    def asig(self, p):
        self.ids[p.ID] = p.expres
    '''    
    @_('PRINT "(" escr1')
    def escritura(self, p):
        for elem in p.escr1:
            print(elem)

    @_('expres ")" ";"')
    def escr1(self, p):
        return [p.expres]

    @_('expres "," escr1')
    def escr1(self, p):
        return [p.expres] + p.escr1
        
    @_('exp NE exp')
    def expres(self, p):
        return p[0] != p[2]

    @_('exp GT exp')
    def expres(self, p):
        return p[0] > p[2]

    @_('exp LT exp')
    def expres(self, p):
        return p[0] < p[2]

    @_('exp EQ exp')
    def expres(self, p):
        return p[0] == p[2]

    @_('exp')
    def expres(self, p):
        return p.exp

    @_('term MINUS exp')
    def exp(self, p):
        return p.term - p.exp

    @_('term PLUS exp')
    def exp(self, p):
        return p.term + p.exp

    @_('term')
    def exp(self, p):
        return p.term
    
    @_('"(" expres ")"')
    def factor(self, p):
        return p.expres
    
    @_('factor DIVIDE term')
    def term(self, p):
        return p.factor / p.term

    @_('factor TIMES term')
    def term(self, p):
        return p.factor * p.term

    @_('factor')
    def term(self, p):
        return p.factor

    @_('PLUS var')
    def factor(self, p):
        return p.var

    @_('MINUS var')
    def factor(self, p):
        return - p.var

    @_('var')
    def factor(self, p):
        return p.var

    @_('FLOATNUMBER')
    def var(self, p):
        return float(p.FLOATNUMBER)

    @_('INTNUMBER')
    def var(self, p):
        return int(p.INTNUMBER)

    @_('ID')
    def var(self, p):
        try:
            return self.ids[p.ID]
        except LookupError:
            print(f'Undefined ID {p.ID!r}')
            return 0

if __name__ == '__main__':
    lexer = CalcLexer()
    parser = CalcParser()
    while True:
        try:
            text = input('calc > ')
        except EOFError:
            break
        if text:
            parser.parse(lexer.tokenize(text))