from lark import Lark, exceptions
import tkinter as tk

grammar = """
?start: stament

content_class: declaration
      | function
      | main_func

stament:main_class 
      | class_def
      | declaration
      | loop
      | conditional
      | print_data
      | input_data
      | square_root

?declaration: sv
sv: (IDENTIFIER ","*)+ EQ (complex_arg ","*)+
var_list: LETTER (COMMA LETTER rdv?)*
IDENTIFIER: LETTER+

complex_arg: STRING | number | BOOLEAN | var_value

?function: sf
sf: "func" func_name "{" content "}"
func_name: IDENTIFIER "(" param_list ")" | IDENTIFIER "(" ")"
param_list: IDENTIFIER (COMMA param_list)?

?class_def: sc
sc: "class" class_name "{" content_class "}"
class_name: LETTER rdv?

?loop: sl
sl: "while" "(" condition ")" "{" content "}"
   | "do" "{" content "}" "while" "(" condition ")"
   | "for" loop_config
loop_config: LETTER rdv? "range" "(" range_arg ")"
range_arg: number | LETTER rdv?

?conditional: sco
sco: "if" "(" condition ")" "{" content "}" ("elsif" "(" condition ")" "{" content "}")* ("else" "{" content "}")?
    | "switch" "{" case_action "}"
condition: var_value | condition_var
condition_var: var_value EQ_OP var_value | var_value EQ_OP complex_arg
EQ_OP: "==" | "!=" | ">=" | "<=" | ">" | "<"
default_arg: STRING | BOOLEAN | number
case_action: case+ default?
case:"case" "==" (number | STRING | IDENTIFIER) "{" content "}"
default: "default" "{" "exit" "}"

?main_func: sfm
sfm: "func main() {" content "}"

?main_class: scm
scm: "class main {" content_class "}"

?print_data: sp
sp: "println" "(" complex_arg ")" | "print" "(" complex_arg ")"

var_value: LETTER rdv? 

?input_data: si
si: "in" ">>" var_value

?square_root: sq
sq: "sqrt" "(" number ")" | "sqrt" "(" var_value ")"

LETTER: "a".."z" | "A".."Z"
number: (DIGIT)+ | (DIGIT)+ POINT (DIGIT)+
rdv: LETTER rdv?
DIGIT: "0".."9"
POINT: "."
EQ: "="
COMMA: ","
BOOLEAN: "true" | "false"
STRING: /"(\\"|[^"])*"/
content: (function | declaration | loop | conditional | main_func | print_data | input_data | square_root)*

%import common.WS
%ignore WS
"""

parser = Lark(grammar, start='start')

def evaluar_cadena():
    try:
        input_text = entrada_texto.get("1.0", tk.END)
        parsed = parser.parse(input_text)
        print(parsed.pretty())
    except exceptions.LarkError as e:
        print(f"Error: {e}")

root = tk.Tk()
root.title("Lyra: Analizador Sintáctico")

entrada_texto = tk.Text(root, height=15, width=60)
entrada_texto.pack()

boton_evaluar = tk.Button(root, text="Evaluar cadena", command=evaluar_cadena)
boton_evaluar.pack()

root.mainloop()
