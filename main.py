import sys
import re

# Definir los tipos de tokens
TOKENS = [
    ('KEYWORD', r'\b(class|func|if|else|elsif|switch|case|default|exit|while|do|for|range|in|sqrt|println|print)\b'),
    ('IDENTIFIER', r'\b[a-zA-Z][a-zA-Z0-9]*\b'),
    ('NUMBER', r'\b\d+(\.\d*)?\b'),
    ('STRING', r'"[^"]*"'),
    ('OPERATOR', r'==|!=|>=|<=|='),
    ('PUNCTUATION', r'[{}(),.]'),
    ('WHITESPACE', r'\s+'),
    ('UNKNOWN', r'.')
]

# Definir la gramática
GRAMMAR = {
    'program': [['statement', 'program'], ['statement']],
    'statement': [['KEYWORD', 'IDENTIFIER', 'PUNCTUATION', 'expression', 'PUNCTUATION']],
    'expression': [['IDENTIFIER'], ['NUMBER'], ['STRING'], ['expression', 'OPERATOR', 'expression']]
}

def tokenizar(codigo):
    lineas = codigo.split('\n')
    token_list = []
    for i, linea in enumerate(lineas):
        token_list_linea = []
        palabras = linea.split(' ')
        for palabra in palabras:
            if palabra in TOKENS:
                token_list_linea.append(palabra)
        if token_list_linea:
            token_list.append((i, token_list_linea))
    return token_list

def analizar_codigo(codigo):
    return tokenizar(codigo)

def validar_tokens(token_lines):
    stack = [['program']]
    line_number = 0
    for line_number, tokens in token_lines:
        for token_type, value in tokens:
            while True:
                if not stack:
                    return False, line_number
                top = stack[-1]
                if isinstance(top, list):
                    if not top:
                        stack.pop()
                        continue
                    next_symbol = top[0]
                    if next_symbol in GRAMMAR:
                        stack.append(GRAMMAR[next_symbol].pop(0))
                    elif next_symbol == token_type:
                        top.pop(0)
                        break
                    else:
                        return False, line_number
                else:
                    stack.pop()
    return not stack, line_number

if len(sys.argv) != 2:
    print("Use: zaphyr <archivo.zph>")
    sys.exit(1)
else:
    ruta_archivo = sys.argv[1]
    with open(ruta_archivo, 'r') as archivo:
        codigo = archivo.read()
        token_lines = analizar_codigo(codigo)
        valido, line_number = validar_tokens(token_lines)
        if valido:
            print("El código es válido.")
        else:
            print(f"El código no es válido. Error en la línea {line_number + 1}.")
            sys.exit(1)