import sys



if len(sys.argv) != 2:
    print("Use: zaphyr <archivo.zph>")
    sys.exit(1)
else:
    ruta_archivo = sys.argv[1]
    with open(ruta_archivo, 'r') as archivo:
        codigo = archivo.read()
        print(codigo)