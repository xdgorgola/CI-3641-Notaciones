from Notaciones import calcular_valor_prefijo, calcular_valor_postfijo, \
    NodoNotacion, crear_arbol_prefijo, crear_arbol_postfijo, recorrer_infijo

# Tokens programa
TOKEN_MOSTRAR = "MOSTRAR"
TOKEN_EVALUAR = "EVAL"
TOKEN_SALIR = "SALIR"
TOKEN_POST = "POST"
TOKEN_PRE = "PRE"

run : bool = True
def simulator_usage():
    print("Uso:\n\tEVAL <ORDEN> <EXPRESION>")
    print("\tEvalua la expresion <EXPRESION> escrita en orden <ORDEN>")

    print("\n\tMOSTRAR <ORDEN> <EXPRESION>")
    print("\tConvierte a orden infijo la expresion <EXPRESION> con orden <ORDEN>")

    print("\n\tORDENES PERMITIDOS:")
    print("\t\t-PRE: Orden pre-fijo")
    print("\t\t-POST: Orden post-fijo")

    print("\n\tSALIR\n\tMata\\sale del programa.")


def wrong_params():
    print("Parametro invalido o numero de parametros incorrecto.")
    simulator_usage()


def comando_mostrar(tokens : list[str]) -> None:
    if (len(tokens) < 2):
        wrong_params()
        return
    
    tipo : str = tokens.pop(0).upper()
    if (tipo != TOKEN_PRE and tipo != TOKEN_POST):
        wrong_params()
        return
    pre : bool = (tipo == TOKEN_PRE)
    exp : str = ' '.join(tokens).strip()
    if (pre):
        recorrer_infijo(crear_arbol_prefijo(exp))
    else:
        recorrer_infijo(crear_arbol_postfijo(exp))
    print()


def comando_evaluar(tokens : list[str]) -> None:
    if (len(tokens) < 2):
        wrong_params()
        return

    tipo : str = tokens.pop(0).upper()
    if (tipo != TOKEN_PRE and tipo != TOKEN_POST):
        wrong_params()
        return
    pre : bool = (tipo == TOKEN_PRE)
    exp : str = ' '.join(tokens).strip()
    if (pre):
        print(str(calcular_valor_prefijo(exp)).lower())
    else:
        print(str(calcular_valor_postfijo(exp)).lower())


while (run):
    tokens : list[str] = input("Introduce un comando>").split()
    if (len(tokens) == 0):
        print("Comando no valido.")
        continue

    comando : str = tokens.pop(0).upper()
    if (comando == TOKEN_EVALUAR):
        comando_evaluar(tokens)
    elif (comando == TOKEN_MOSTRAR):
        comando_mostrar(tokens)
    elif (comando == TOKEN_SALIR):
        run = False
    else:
        wrong_params()
