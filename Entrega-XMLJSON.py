#Denardi Bruno, Scarafia Juan Ignacio
# -*- coding: utf-8 -*-
from ply import lex
from ply import yacc

#########################################################
# LEXX                                                  #
#########################################################


class Lex:
    states = (
        ('t', 'exclusive'),
        ('a1', 'exclusive'),
        ('a2', 'exclusive'),
    )

    tokens = [
        'PD',
        'MENOR',
        'MENORBARRA',
        'TEXT',
        'MAYOR',
        'BARRAMAYOR',
        'IGUAL',
        'AV1O',
        'AV1TEXT',
        'AV1C',
        'AV2O',
        'AV2TEXT',
        'AV2C',
    ]

    r_digito = r'([0-9])'
    r_nodigito = r'([_A-Za-z])'
    r_ID = r'(' + r_nodigito + r'(' + r_digito + r'|' + r_nodigito + r')*)'

    t_ignore = ''
    t_a2_ignore = ''
    literals = '$%^'
    t_t_ignore = ' \t'
    t_a1_ignore = ''
    t_t_IGUAL = r'='


    def t_MENORBARRA(self, t):
        r'</'
        t.lexer.push_state('t')
        return t


    def t_MENOR(self, t):
        r'<'
        t.lexer.push_state('t')
        return t


    def t_PD(self, t):
        '[^<]+'
        return t


    def t_t_MAYOR(self, t):
        r'>'
        t.lexer.pop_state()
        return t


    def t_t_BARRAMAYOR(self, t):
        r'/>'
        t.lexer.pop_state()
        return t


    def t_t_AV1O(self, t):
        r'\''
        t.lexer.push_state('a1')
        return t


    def t_t_AV2O(self, t):
        r'"'
        t.lexer.push_state('a2')
        return t


    def t_a1_AV1TEXT(self, t):
        r'[^\']+'
        t.value = unicode(t.value)
        return t


    def t_a1_AV1C(self, t):
        r'\''
        t.lexer.pop_state()
        return t


    def t_a2_AV2TEXT(self, t):
        r'[^"]+'
        t.value = unicode(t.value)
        return t


    def t_a2_AV2C(self, t):
        r'"'
        t.lexer.pop_state()
        return t

    def t_t_TEXT(self, t):
        return t
    t_t_TEXT.__doc__ = r_ID

    def t_ANY_newline(self, t):
        r'\n'
        t.lexer.lineno += len(t.value)

    def t_ANY_error(self, t):
        print("Illegal character")

    def build(self):
        self.lexer = lex.lex(object=self)
    def test(self, data):
        self.lexer.input(data)

xml_reservados = {
    "&": "&amp;",
    '"': "&quot;",
    "'": "&apos;",
    ">": "&gt;",
    "<": "&lt;",
    }

def reservado(texto):
    LISTADO=[]
    for cantidad in texto:
        LISTADO.append(xml_reservados.get(cantidad, cantidad))
    return "".join(LISTADO)


def noreservado(solucion):
    reglas = xml_reservados.items()
    reglas.reverse()
    for reservado, listado in reglas:
        solucion = solucion.replace(listado, reservado)
    return solucion

###################################################
# YACC                                            #
###################################################

def p_root_elemento(p):
    '''root : elemento
            | elemento PD'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 2:
        p[0] = p[1] + p[2]

def p_root_PD(p):
    '''root : PD elemento
            | PD elemento PD'''
    if len(p) == 3:
        p[0] = p[1] + p[2]
    elif len(p) == 4:
        p[0] = p[1] + p[2] + p[3]

def p_elemento(p):
    '''elemento : EI hijos EF
                | especial'''
    x = ""
    for lugar in (p[2]):
        x = x + lugar
    if len(p) == 4:
        p[0] = p[1] + x + p[3]
    elif len(p) == 2:
        p[0]

def p_EI(p):
    '''EI : MENOR TEXT AS MAYOR'''
    p[0] = '{0}{1}{2}'.format('{ "', p[2], '":',)

def p_EF(p):
    '''EF : MENORBARRA TEXT MAYOR'''
    p[0] = '{0}'.format("}")

def p_especial(p):
    '''especial : MENOR TEXT AS BARRAMAYOR'''
    p[0] = p[1] + p[2] + p[3] + ","

def p_AS(p):
    '''AS : AS A
          | empty'''
    if len(p) == 3:
        if p[2]:
            p[0] = p[2]
        else:
            p[0] = p[1] + p[2]

def p_A(p):
    '''A : TEXT IGUAL valorA'''
    p[0] = ' {0}: {2} "{0}": "{1}",  '.format(p[1], p[3], '[')

def p_valorA(p):
    '''valorA : AV1O AV1TEXT AV1C
              | AV2O AV2TEXT AV2C'''
    p[0] = noreservado(p[2])

def p_hijos(p):
    '''hijos : hijo hijos
             | empty'''
    if len(p) >= 3:
        if p[2]:
            p[0] = [p[1]] + p[2]
        else:
            p[0] = [p[1]]

def p_ce(p):
    '''hijo : elemento'''
    p[0] = p[1]

def p_cpd(p):
    '''hijo : PD'''
    p[0] = p[1]

def p_empty(p):
    '''empty :'''
    pass

def p_error(p):
    print("Parse error")
    pass

def parser_XML_JSON(data):
    # LEXX
    lexer = Lex()
    lexer.build()
    lexer.test(data)
    # YACC
    global tokens
    tokens = Lex.tokens
    yacc.yacc(method="LALR")
    root = yacc.parse(data, lexer=lexer.lexer)
    return root


def main():
    #data = open('/home/bletzer/Escritorio/TPXML/ejemploTP.xml').read()
    data = '''<Data>
	<Customers CustomerID="45183">
		<ContactName>Martín Sánchez</ContactName>
		<Phone>5557555</Phone>
		<FullAddress>
			<Address>Mitre 4511</Address>
			<City>Buenos Aires</City>
			<PostalCode>C1094</PostalCode>
			<Country>Argentina</Country>
		</FullAddress>
	</Customers>
	<Customers CustomerID="46977">
		<ContactName>Marianela Montenegro</ContactName>
		<Phone>5566874</Phone>
		<FullAddress>
			<Address>Callao 6531 2o B</Address>
			<City>Buenos Aires</City>
			<PostalCode>C1066</PostalCode>
			<Country>Argentina</Country>
		</FullAddress>
	</Customers>
</Data>'''
    root = parser_XML_JSON(data)
    print (root)

if __name__ == '__main__':
    main()