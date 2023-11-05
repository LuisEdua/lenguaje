import sys

def tokenizar(codigo):
    tokens = ['class', 'func', 'main', 'while', 'do', 'for', 'range', 'true', 'false', ' if', 'else', 'elsif', 'switch', '(', ')', '{', '}', 'case', 'default',
              'exit', 'in', 'sqrt', 'print', 'println', '+', '-', '*', '/', '**', '[', ']', '=', '==', '>=', '<=', '>', '<', '!=', '>>', 'and', 'or', '&&', '||',
              '!', 'not', '+=', '-=', '*=', '/=', '%', '%=', '+=', '-=', '++', '--', '//']
    token_list = []
    lineas = codigo.split('\n')
    i = 1
    for linea in lineas:
        token_list_linea = []
        palabras = linea.split()
        for palabra in palabras:
            if palabra in tokens:
                token_list_linea.append(palabra)
        if token_list_linea.__len__() > 0:
            token_list.append((i, token_list_linea))
        i += 1
    return token_list

def analizar_codigo(codigo):
    return tokenizar(codigo)

if len(sys.argv) != 2:
    print("Use: zaphyr <archivo.zph>")
    sys.exit(1)
else:
    ruta_archivo = sys.argv[1]
    with open(ruta_archivo, 'r') as archivo:
        codigo = archivo.read()
        token_lines=analizar_codigo(codigo)
        for tokens in token_lines:
            tokens = tokens[1]
            for token in tokens:
                print(token)
                