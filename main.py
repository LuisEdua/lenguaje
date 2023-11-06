import os
import re
import sys

error = False
line_number = 0
nombres_declarados = set()

gramatica = {
    'L': r'[a-zA-Z]+',
    'LB': r'{',
    'RB': r'}',
    'LP': r'\(',
    'OS': r'"|"',
    'N': r'[0-9]+',
    'CO': r'\,',
    'P': r'\.',
    'E': r'=',
    'B': r'(true|false)',
    'F': r'^(func)',
    'C': r'^(class)',
    'CC': r'^(while|do|for)',
    'O': r'==|!=|>=|<=|+|-|*|/|**',
    'RC': r'(range)',
    'SC': r'^(if|elsif|else|switch)',
    'CA': r'^(case|default)',
    'EX': r'^(exit)$',
    'M': r'(main)',
    'RP': r'^(print|println)',
    'RI': r'^(in)',
    'OI': r'(>>)',
    'RR': r'^(return)'
}

regex_identifiers = fr'({gramatica["L"]})(\s*,\s*{gramatica["L"]})*'

regex_number = fr'({gramatica["N"]}{gramatica["P"]}{gramatica["N"]})|({gramatica["N"]})'

regex_string = r'("([^"\\]|\\.)*")'

regex_valor = ( fr'({gramatica["L"]}|{regex_number}|{gramatica["B"]})|({gramatica["L"]}|{regex_number}|{gramatica["B"]}|{regex_string}){gramatica["CO"]}')

regex_sv = ( fr'\s*({regex_identifiers})\s*' fr'\s*({gramatica["E"]})\s*' fr'\s*({regex_valor})\s*' )

regex_data_print = (fr'({regex_string}|{gramatica["L"]}|\s+|\+)+')

regex_print = fr'\s*({gramatica["RP"].lstrip("^")})\s*{gramatica["LP"]}{regex_data_print}\)\s*'

regex_input = fr'\s*({gramatica["RI"].lstrip("^")}\s*{gramatica["OI"]}\s*{gramatica["L"]})'

variables = []

def error_message(i, missing):
    print('Syntax error: Se esperaba "'+ missing + '" en la linea ' + str(i+1))
    exit(1)

def error_unrecognize(i, u):
    print('Syntax error: "'+ u + '" no se reconoce en la linea ' + str(i+1))
    exit(1)

def validar_print(tokens, i):
    print(tokens)
    if re.match(gramatica['LP'], tokens[1]):
        print(re.match(regex_string, "cadena"))#tokens[1:-2]):
    else:
        error_message(i, '(')

def validar_declaracion_variables(tokens, l):
    lenList = len(tokens)
    mid_pos = (lenList)//2
    i = 0
    tokens = [token.replace(',', '') for token in tokens]
    if lenList % 2 != 0:
        if re.match(gramatica["E"], tokens[mid_pos]):
            while i < mid_pos:
                if not re.match(gramatica["L"], tokens[i]):
                    error_message (l, "identificador")
                else:
                    if not tokens[i] in variables:
                        variables.append(tokens[i])
                    else:
                        error_message (l, "variable nueva")
                i += 1
            i += 1
            while i < len(tokens):
                if not re.match(regex_valor, tokens[i]):
                    error_message (l, "valor")
                i += 1
        else:
            error_message (l, "= en el medio")
    else:
        error_message (l, "= en el medio")
    return l + 1

def validar_cuerpo_funcion(lineas, i):
    linea = lineas[i]
    if linea.strip() == '':
        i = validar_cuerpo_funcion(lineas, i+1)
    else:
        tokens = linea.split()
        if re.match(regex_sv, lineas[i]):
            i = validar_declaracion_variables(tokens, i)
            i = validar_cuerpo_funcion(lineas, i)
        elif re.match(regex_print, lineas[i]):
            i += 1
            i = validar_cuerpo_funcion(lineas, i)
        elif re.match(regex_input, lineas[i]):
            i += 1
            i = validar_cuerpo_funcion(lineas, i)
    return i

def validar_funciones(lineas, i):
    tokens = re.findall(r'\,|\(|\)|\{|\w+', lineas[i])
    if re.match(gramatica['F'], tokens[0]):
        if re.match(gramatica['M'], tokens[1]):
            if re.match(gramatica['LP'], tokens[2]):
                if ")" == tokens[3]:
                    if re.match(gramatica['LB'], tokens[4]):
                        i = validar_cuerpo_funcion(lineas, i+1)
                        if not re.match(gramatica['RB'], lineas[i]):
                            error_message(i, '}')
                    else:
                        error_message(i, '{')
                else:
                    error_message(i, ')')
            else:
                error_message(i, '(')
        elif re.match(gramatica['L'], tokens[1]):
            if re.match(gramatica['LP'], tokens[2]):
                j = 3
                while j < len(tokens) and tokens[j] != ')':
                    if j%2 != 0:
                        if not re.match(gramatica["L"], tokens[j]):
                            error_message (i, "identificador")
                    else:
                        if ',' != tokens[j]:
                            error_message (i, ",")
                    j += 1
                if ")" == tokens[j]:
                    if j+1 < len(tokens) and re.match(gramatica['LB'], tokens[j+1]):
                        i = validar_cuerpo_funcion(lineas, i+1)
                        if not re.match(gramatica['RB'], lineas[i]):
                            error_message(i, '}')
                    else:
                        error_message(i, '{')
                else:
                    error_message(i, ')')
            else:
                error_message(i, '(')
        else:
            error_message(i, 'identificador')
    else:
        error_message(i, 'func')
    return i

def validar_cuerpo_class(lineas, i):
    linea = lineas[i]
    if linea.strip() == '':
        i = validar_cuerpo_class(lineas, i+1)
    else:
        tokens = re.findall(r'\(|\)|\{|\w+', linea)
        if re.match(regex_sv, lineas[i]):
            tokensV = linea.split()
            i = validar_declaracion_variables(tokensV, i)
            i = validar_cuerpo_class(lineas, i)
        elif re.match(gramatica["F"], tokens[0]):
            i = validar_funciones(lineas, i)
            i = validar_cuerpo_class(lineas, i)
    return i

def validar_classes(lineas, i):
    linea = lineas[i]
    if linea == '':
        validar_classes(lineas, i+1)
    else:
        tokens = linea.split(' ')
        if re.match(gramatica['C'], tokens[0]):
            if re.match(gramatica['L'], tokens[1]) or re.match(gramatica['M'], tokens[1]):
                if re.match(gramatica['LB'], tokens[2]):
                    i = validar_cuerpo_class(lineas, i+1)
                    if not re.match(gramatica['RB'], lineas[i]):
                        error_message(i, '}')
                else:
                    error_message(i, '{')
            else:
                error_message(i, 'nombre de clase')
        else:
            error_message(i, 'class')


def validar_codigo(codigo):
    lineas = codigo.split('\n')
    validar_classes(lineas, 0)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Use: zaphyr <archivo.zph>")
        sys.exit(1)
    else:
        ruta_archivo = sys.argv[1]
        _, extension_archivo = os.path.splitext(ruta_archivo)
        if extension_archivo != ".zph":
            print("El archivo debe ser .zph")
            sys.exit(1)
        
        with open(ruta_archivo, 'r') as archivo:
            codigo = archivo.read()
            validar_codigo(codigo)