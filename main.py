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

def analizar_codigo(codigo):
    tokens = []
    while codigo:
        match = None
        for token_type, pattern in TOKENS:
            regex = re.compile(pattern)
            match = regex.match(codigo)
            if match:
                value = match.group(0)
                if token_type != 'WHITESPACE':
                    tokens.append((token_type, value))
                codigo = codigo[match.end():]
                break
        if not match:
            sys.stderr.write('Error: Invalid character\n')
            sys.exit(1)
    return tokens

def validar_tokens(tokens):
    stack = [['program']]
    for token_type, value in tokens:
        while True:
            if not stack:
                return False
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
                    return False
            else:
                stack.pop()
    return not stack

if len(sys.argv) != 2:
    print("Use: zaphyr <archivo.zph>")
    sys.exit(1)
else:
    ruta_archivo = sys.argv[1]
    with open(ruta_archivo, 'r') as archivo:
        codigo = archivo.read()
        tokens = analizar_codigo(codigo)
        if validar_tokens(tokens):
            print("El código es válido.")
        else:
            print("El código no es válido.")
            sys.exit(1)