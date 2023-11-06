from lark import Lark, exceptions
import tkinter as tk

grammar = """
?start: program

?program:class_declaration | class_main

?class_main: "class" "main" "{" class_body "}"
?class_declaration: "class" IDENTIFIER "{" class_body "}"

IDENTIFIER: LETTER+

class_body: var_declaration
            | func_def
            | func_main

func_def: "func" IDENTIFIER "{" body "}"
func_main: "func" "main" "{" body "}"

body: var_declaration
    | ciclo
    | condicional
    | print
    | in
    | sqrt


print: "print" "(" STRING ")" | "println" "(" STRING ")"
in: "in" ">>" IDENTIFIER
sqrt: "sqrt" "(" NUM ")" | "sqrt" "(" NUM ")"
ciclo: "while" "(" condition ")" "{" body "}" | "do" "{" body "}" "while" "(" condition ")" | "for" IDENTIFIER "range""("IDENTIFIER")""{"body"}"
condicional: "if" "(" condition ")" "{" body "}" ("elsif" "(" condition ")" "{" body "}")* ("else" "{" body "}")? | "switch""("IDENTIFIER")""{"switch_body"}"
condition: IDENTIFIER "==" IDENTIFIER | IDENTIFIER "!=" IDENTIFIER | IDENTIFIER ">" IDENTIFIER | IDENTIFIER "<" IDENTIFIER | IDENTIFIER ">=" IDENTIFIER | IDENTIFIER "<=" IDENTIFIER
var_declaration: (IDENTIFIER | ",")+ "=" (NUM | STRING | BOOLEAN | ",")+
switch_body: "case" "==" (NUM | STRING) "{"body "}" | "default" "{" "exit" "}"
STRING: /"(\\"|[^"])*"/
DIGIT: "0".."9"
POINT: "."
NUM: DIGIT+ | DIGIT+ POINT DIGIT+
LETTER: "a".."z" | "A".."Z"
BOOLEAN: "true" | "false"

%import common.WS
%ignore WS
"""

parser = Lark(grammar, start='start')

def evaluar_cadena():
    try:
        input_text = entrada_texto.get("1.0", tk.END)
        parsed = parser.parse(input_text)
        print(parsed)
    except exceptions.LarkError as e:
        print(f"Error: {e}")

root = tk.Tk()
root.title("Lyra: Analizador Sintáctico")

entrada_texto = tk.Text(root, height=15, width=60)
entrada_texto.pack()

boton_evaluar = tk.Button(root, text="Evaluar cadena", command=evaluar_cadena)
boton_evaluar.pack()

root.mainloop()
