# -----------------------------------------------------------------------------
# calc.py
# -----------------------------------------------------------------------------

import sys
sys.path.append('../..')

from sly import Lexer, Parser

class CalcLexer(Lexer):
        # Set of token names.   This is always required
    tokens = { STRING, INTNUMBER, FLOATNUMBER, ID, 
               VAR, IF, ELSE, PRINT, INT, FLOAT, PROGRAM,
               PLUS, MINUS, TIMES, DIVIDE, ASSIGN,
               EQ, LT, GT, NE }

    literals = { '(', ')', '{', '}', ';', ':', ',' }

    # String containing ignored characters
    ignore = ' \t'

    # Regular expression rules for tokens
    PLUS    = r'\+'
    MINUS   = r'-'
    TIMES   = r'\*'
    DIVIDE  = r'/'
    EQ      = r'=='
    ASSIGN  = r'='
    NE      = r'<>'
    LT      = r'<'
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

    @_(r'\"(.*?)\"')
    def STRING(self, t):
        t.value = str(t.value[1: len(t.value) - 1])
        return t

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
        self.programs = { }
    
    @_('PROGRAM ID ":" program2')
    def programa(self, p):
        self.programs[p.ID] = ""
        return p.program2
    
    @_('vars bloque')
    def program2(self, p):
        return p.bloque
    
    @_('bloque')
    def program2(self, p):
        return p.bloque

    @_('VAR var1')
    def vars(self, p):
        pass

    @_('ID var2 ":" tipo ";" var1')
    def var1(self, p):
        self.ids[p.ID] = 0

    @_('empty')
    def var1(self, p):
        pass

    @_('"," ID var2')
    def var2(self, p):
        self.ids[p.ID] = 0

    @_('empty')
    def var2(self, p):
        pass

    @_('"{" estatuto bloque1')
    def bloque(self, p):
        return p.bloque1

    @_('estatuto bloque1')
    def bloque1(self, p):
        return p.bloque1

    @_('"}"')
    def bloque1(self, p):
        pass

    @_('asig')
    def estatuto(self, p):
        return p.asig

    @_('condition')
    def estatuto(self, p):
        return p.condition

    @_('escritura')
    def estatuto(self, p):
        return p.escritura

    @_('IF "(" expres ")" bloque condition2 ";"')
    def condition(self, p):
        if p.expres:
            return p.bloque
        else:
            return p.condition2

    @_('ELSE bloque')
    def condition2(self, p):
        return p.bloque

    @_('empty')
    def condition2(self, p):
        pass

    @_('ID ASSIGN expres ";"')
    def asig(self, p):
        self.ids[p.ID] = p.expres
    
    @_('INT')
    def tipo(self, p):
        return 'int'

    @_('FLOAT')
    def tipo(self, p):
        return 'float'
        
    @_('PRINT "(" escr1')
    def escritura(self, p):
        for elem in p.escr1:
            elem
            #print(elem)
            
    @_('escr2 ")" ";"')
    def escr1(self, p):
        return [p.escr2]

    @_('escr2 "," escr1')
    def escr1(self, p):
        return [p.escr2] + p.escr1
    
    @_('expres')
    def escr2(self, p):
        return p.expres

    @_('STRING')
    def escr2(self, p):
        return p.STRING
    
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

    @_('')
    def empty(self, p):
        pass

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
    filename = input("write the file name:")
    f=open(filename, "r")
    data = f.read()

    for tok in lexer.tokenize(data):
        print(tok)
    
    parser.parse(lexer.tokenize(data))