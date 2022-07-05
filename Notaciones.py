from __future__ import annotations

ASOC_IZ = "IZ"
ASOC_DE = "DE"

class NodoNotacion:
    
    def __init__(self : NodoNotacion, tok : str, lv : NodoNotacion, rv : NodoNotacion) -> None:
        self.tok : str = tok
        self.lv : NodoNotacion = lv
        self.rv : NodoNotacion = rv


def precedencia(simbolo : str) -> int:
    assert(simbolo == "^" or simbolo == "&" or simbolo == "|" \
            or simbolo == "=>")

    if (simbolo == "^"):
        return 10000
    
    if (simbolo == "&" or simbolo == "|"):
        return 10
    
    return 8
    

def asociacion(simbolo : str) -> str:
    assert(simbolo == "&" or simbolo == "|" or simbolo == "=>")
    if (simbolo == "&" or simbolo == "|"):
        return ASOC_IZ
    return ASOC_DE
    

def es_simbolo(token : str) -> bool:
    """_summary_

    Arguments:
        token -- _description_

    Returns:
        _description_
    """

    token : str = token.strip()
    assert(len(token) > 0)

    return token == "&" or token == "|" \
        or token == "=>" or token == "^"


def valor_booleano(valor : str) -> bool:
    """_summary_

    Arguments:
        valor -- _description_

    Returns:
        _description_
    """

    valor = valor.lower()
    assert(valor == "true" or valor == "false")
    return valor == "true"


def realizar_operacion_binaria(izq : bool, der : bool, ope : str) -> bool:
    """_summary_

    Arguments:
        izq -- _description_
        der -- _description_
        ope -- _description_

    Returns:
        _description_
    """
    
    assert(ope == "&" or ope == "|" or ope == "=>")

    if (ope == "&"):
        return izq and der
    elif (ope == "|"):
        return izq or der
    return (not izq) or der


def calcular_valor_prefijo(expresion : str) -> bool:
    """_summary_

    Arguments:
        expresion -- _description_

    Returns:
        _description_
    """

    tokens : list[str] = expresion.split()
    assert(len(tokens) > 0)

    valores : list[bool] = []
    while len(tokens) > 0:
        i : str = tokens.pop()
        if (not es_simbolo(i)):
            valores.append(valor_booleano(i))
            continue
        
        if (i != "^"):
            izq : bool = valores.pop()
            der : bool = valores.pop()
            valores.append(realizar_operacion_binaria(izq, der, i))
            print(f"{izq} {i} {der} -> {realizar_operacion_binaria(izq, der, i)}")
            continue
            
        valores.append(not valores.pop())
    
    return valores.pop()


def calcular_valor_postfijo(expresion : str) -> bool:
    """_summary_

    Arguments:
        expresion -- _description_

    Returns:
        _description_
    """

    tokens : list[str] = expresion.split()
    tokens = tokens[::-1]
    assert(len(tokens) > 0)
    
    valores : list[bool] = []
    while len(tokens) > 0:
        i : str = tokens.pop()
        if (not es_simbolo(i)):
            valores.append(valor_booleano(i))
            continue
        
        if (i != "^"):
            der : bool = valores.pop()
            izq : bool = valores.pop()
            valores.append(realizar_operacion_binaria(izq, der, i))
            continue
            
        valores.append(not valores.pop())
    
    return valores.pop()


def realizar_operacion_binaria_arbol(izq : NodoNotacion, der : NodoNotacion, ope : str) -> NodoNotacion:
    """_summary_

    Arguments:
        izq -- _description_
        der -- _description_
        ope -- _description_

    Returns:
        _description_
    """
    
    assert(ope == "&" or ope == "|" or ope == "=>")
    return NodoNotacion(ope, izq, der)


def crear_arbol_prefijo(expresion : str) -> NodoNotacion:
    tokens : list[str] = expresion.split()
    assert(len(tokens) > 0)

    valores : list[NodoNotacion] = []
    while len(tokens) > 0:
        i : str = tokens.pop()
        if (not es_simbolo(i)):
            valores.append(NodoNotacion(i, None, None))
            continue
        
        if (i != "^"):
            izq : NodoNotacion = valores.pop()
            der : NodoNotacion = valores.pop()
            valores.append(realizar_operacion_binaria_arbol(izq, der, i))
            continue
            
        valores.append(NodoNotacion("^", None, valores.pop()))
    
    return valores.pop()


def crear_arbol_postfijo(expresion : str) -> NodoNotacion:
    """_summary_

    Arguments:
        expresion -- _description_

    Returns:
        _description_
    """

    tokens : list[str] = expresion.split()
    tokens = tokens[::-1]
    assert(len(tokens) > 0)
    
    valores : list[bool] = []
    while len(tokens) > 0:
        i : str = tokens.pop()
        if (not es_simbolo(i)):
            valores.append(NodoNotacion(i, None, None))
            continue
        
        if (i != "^"):
            der : bool = valores.pop()
            izq : bool = valores.pop()
            valores.append(realizar_operacion_binaria_arbol(izq, der, i))
            continue
            
        valores.append(NodoNotacion("^", None, valores.pop()))
    
    return valores.pop()


def tiene_mayor_preced(raiz : NodoNotacion, hijo : NodoNotacion) -> bool:
    return es_simbolo(hijo.tok) and precedencia(raiz.tok) > precedencia(hijo.tok)


def tiene_misma_preced(raiz : NodoNotacion, hijo : NodoNotacion) -> bool:
    return es_simbolo(hijo.tok) and precedencia(raiz.tok) == precedencia(hijo.tok)


def tiene_misma_asoc(raiz : NodoNotacion, hijo : NodoNotacion) -> bool:
    return es_simbolo(hijo.tok) and asociacion(raiz.tok) == asociacion(hijo.tok)


def recorrer_infijo(raiz : NodoNotacion) -> None:
    
    if (raiz.lv != None):
        if (tiene_mayor_preced(raiz, raiz.lv)):
            print("(", end="")
            recorrer_infijo(raiz.lv)
            print(")", end="")
        elif (tiene_misma_preced(raiz, raiz.lv) and tiene_misma_asoc(raiz, raiz.lv) and asociacion(raiz.tok) == ASOC_DE):
            print("(", end="")
            recorrer_infijo(raiz.lv)
            print(")", end="")
        else:
            recorrer_infijo(raiz.lv)

    print(raiz.tok, end=" ")

    if (raiz.rv != None):
        if (tiene_mayor_preced(raiz, raiz.rv)):
            print("(", end="")
            recorrer_infijo(raiz.rv)
            print(")", end="")
        elif (tiene_misma_preced(raiz, raiz.rv) and tiene_misma_asoc(raiz, raiz.rv) and asociacion(raiz.tok) == ASOC_IZ):
            print("(", end="")
            recorrer_infijo(raiz.rv)
            print(")", end="")
        else:
            recorrer_infijo(raiz.rv)
    

a = crear_arbol_prefijo("| & => true true false ^ true")
recorrer_infijo(a)
print()

b = crear_arbol_prefijo("& | => true true false | true ^ false")
recorrer_infijo(b)
print()

c = crear_arbol_prefijo("=> => => => true false true false true")
recorrer_infijo(c)
print()

d = crear_arbol_prefijo("| & | & true true true true true")
recorrer_infijo(d)
print()

e = crear_arbol_prefijo("| & ^ => true true false true")
recorrer_infijo(e)
print()

f = crear_arbol_prefijo("=> true => true => true => true true")
recorrer_infijo(f)
print()

g = crear_arbol_prefijo("| true & true & true | true & true true")
recorrer_infijo(g)
print()

h = crear_arbol_prefijo("| & & | & true true true true true true")
recorrer_infijo(h)
print()