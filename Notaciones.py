from __future__ import annotations

# TOKENS REPRESENTATIVOS DE ASOCIACION A IZQUIERDA Y A DERECHA
ASOC_IZ = "IZ"
ASOC_DE = "DE"

class NodoNotacion:
    """
    Nodo que contiene un token de una expresion logica a evaluar/traducir.
    """
    def __init__(self : NodoNotacion, tok : str, lv : NodoNotacion, rv : NodoNotacion) -> None:
        self.tok : str = tok
        self.lv : NodoNotacion = lv
        self.rv : NodoNotacion = rv


def precedencia(simbolo : str) -> int:
    """
    Calcula la precedencia de un operador.

    Arguments:
        simbolo -- Operador

    Returns:
        Precedencia del operador
    """

    assert(simbolo == "^" or simbolo == "&" or simbolo == "|" \
            or simbolo == "=>")

    if (simbolo == "^"):
        return 10000
    
    if (simbolo == "&" or simbolo == "|"):
        return 10
    
    return 8
    

def asociacion(simbolo : str) -> str:
    """
    Devuelve el tipo de asociacion de un operador

    Arguments:
        simbolo -- Operador

    Returns:
        Asociacion del operador
    """
    assert(simbolo == "&" or simbolo == "|" or simbolo == "=>")
    if (simbolo == "&" or simbolo == "|"):
        return ASOC_IZ
    return ASOC_DE
    

def es_operador(token : str) -> bool:
    """
    Indica si un simbolo es un operador logico

    Arguments:
        token -- Simbolo a examinar

    Returns:
        True si el simbolo es un operador logico. False en otro caso.
    """

    token : str = token.strip()
    assert(len(token) > 0)

    return token == "&" or token == "|" \
        or token == "=>" or token == "^"


def valor_booleano(valor : str) -> bool:
    """
    Calcula el valor booleano de un simbolo

    Arguments:
        valor -- Simbolo a convertir a booleano

    Returns:
        True si el simbolo es true. False si es false.
    """

    valor = valor.lower()
    assert(valor == "true" or valor == "false")
    return valor == "true"


def realizar_operacion_binaria(izq : bool, der : bool, ope : str) -> bool:
    """
    Realiza la operacion binaria representada por un operador.

    Arguments:
        izq -- Operando izquierdo
        der -- Operando derecho
        ope -- Operador

    Returns:
        Resultado de la operacion binaria
    """
    
    assert(ope == "&" or ope == "|" or ope == "=>")

    if (ope == "&"):
        return izq and der
    elif (ope == "|"):
        return izq or der
    return (not izq) or der


def calcular_valor_prefijo(expresion : str) -> bool:
    """
    Calcula el valor de una expresion logica prefija

    Arguments:
        expresion -- Expresion prefija a evaluar

    Returns:
        Valor de la expresion prefija
    """

    tokens : list[str] = expresion.split()
    assert(len(tokens) > 0)

    valores : list[bool] = []
    while len(tokens) > 0:
        i : str = tokens.pop()
        if (not es_operador(i)):
            valores.append(valor_booleano(i))
            continue
        
        if (i != "^"):
            izq : bool = valores.pop()
            der : bool = valores.pop()
            valores.append(realizar_operacion_binaria(izq, der, i))
            continue
            
        valores.append(not valores.pop())
    
    return valores.pop()


def calcular_valor_postfijo(expresion : str) -> bool:
    """
    Calcula el valor de una expresion logica postfija

    Arguments:
        expresion -- Expresion postfija a evaluar

    Returns:
        Valor de la expresion postfija
    """


    tokens : list[str] = expresion.split()
    tokens = tokens[::-1]
    assert(len(tokens) > 0)
    
    valores : list[bool] = []
    while len(tokens) > 0:
        i : str = tokens.pop()
        if (not es_operador(i)):
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
    """
    Realiza una operacion binaria entre dos nodos de tokens y 
    crea el nodo resultante de esta peracon

    Arguments:
        izq -- Operando izquierdo
        der -- Operando derecho
        ope -- Operador

    Returns:
        Nodo representativo de la operacion binaria
    """
    
    assert(ope == "&" or ope == "|" or ope == "=>")
    return NodoNotacion(ope, izq, der)


def crear_arbol_prefijo(expresion : str) -> NodoNotacion:
    """
    Crea un arbol que representa una expresion prefija

    Arguments:
        expresion -- Expresion base

    Returns:
        Raiz del arbol
    """

    tokens : list[str] = expresion.split()
    assert(len(tokens) > 0)

    valores : list[NodoNotacion] = []
    while len(tokens) > 0:
        i : str = tokens.pop()
        if (not es_operador(i)):
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
    """
    Crea un arbol que representa una expresion postfija

    Arguments:
        expresion -- Expresion base

    Returns:
        Raiz del arbol
    """

    tokens : list[str] = expresion.split()
    tokens = tokens[::-1]
    assert(len(tokens) > 0)
    
    valores : list[bool] = []
    while len(tokens) > 0:
        i : str = tokens.pop()
        if (not es_operador(i)):
            valores.append(NodoNotacion(i, None, None))
            continue
        
        if (i != "^"):
            der : bool = valores.pop()
            izq : bool = valores.pop()
            valores.append(realizar_operacion_binaria_arbol(izq, der, i))
            continue
            
        valores.append(NodoNotacion("^", None, valores.pop()))
    
    return valores.pop()


def tiene_mayor_preced(a : NodoNotacion, b : NodoNotacion) -> bool:
    """
    Indica si un nodo a tiene mayor precedencia que un nodo b
    Arguments:
        a -- Nodo a
        b -- Nodo b

    Remarks:
        Ambos nodos deben ser operadores o devuelve false

    Returns:
        True si a tiene mayor precedencia que b. False en caso contrairo
    """

    return es_operador(b.tok) and precedencia(a.tok) > precedencia(b.tok)


def tiene_misma_preced(a : NodoNotacion, b : NodoNotacion) -> bool:
    """
    Indica si un nodo a tiene igual precedencia que un nodo b
    Arguments:
        a -- Nodo a
        b -- Nodo b

    Remarks:
        Ambos nodos deben ser operadores o devuelve false

    Returns:
        True si a tiene igual precedencia que b. False en caso contrairo
    """

    return es_operador(b.tok) and precedencia(a.tok) == precedencia(b.tok)


def tiene_misma_asoc(a : NodoNotacion, b : NodoNotacion) -> bool:
    """
    Indica si un nodo a tiene igual asociacion que un nodo b
    Arguments:
        a -- Nodo a
        b -- Nodo b

    Remarks:
        Ambos nodos deben ser operadores o devuelve false

    Returns:
        True si a tiene igual asociacion que b. False en caso contrairo
    """

    return es_operador(b.tok) and asociacion(a.tok) == asociacion(b.tok)


def recorrer_infijo_string(raiz : NodoNotacion, acum : str = "") -> str:
    """
    Recorre un arbol de expresion y crea un string infijo de una
    expresion logica

    Arguments:
        raiz -- Raiz del arbol
    """
    
    if (raiz.lv != None):
        if (tiene_mayor_preced(raiz, raiz.lv)):
            acum += "("
            acum += recorrer_infijo_string(raiz.lv)
            acum += ")"
        elif (tiene_misma_preced(raiz, raiz.lv) and tiene_misma_asoc(raiz, raiz.lv) and asociacion(raiz.tok) == ASOC_DE):
            acum += "("
            acum += recorrer_infijo_string(raiz.lv)
            acum += ")"
        else:
            acum += recorrer_infijo_string(raiz.lv)

    if (es_operador(raiz.tok)):
        acum += f" {raiz.tok} "
    else:
        acum += f"{raiz.tok}"

    if (raiz.rv != None):
        if (tiene_mayor_preced(raiz, raiz.rv)):
            acum += "("
            acum += recorrer_infijo_string(raiz.rv)
            acum += ")"
        elif (tiene_misma_preced(raiz, raiz.rv) and tiene_misma_asoc(raiz, raiz.rv) and asociacion(raiz.tok) == ASOC_IZ):
            acum += "("
            acum += recorrer_infijo_string(raiz.rv)
            acum += ")"
        else:
            acum += recorrer_infijo_string(raiz.rv)
    
    return acum
    

#a = crear_arbol_prefijo("| & => true true false ^ true")
#recorrer_infijo(a)
#print()
#print(f"{recorrer_infijo_string(a)}\n")
#
#b = crear_arbol_prefijo("& | => true true false | true ^ false")
#recorrer_infijo(b)
#print()
#print(f"{recorrer_infijo_string(b)}\n")
#
#c = crear_arbol_prefijo("=> => => => true false true false true")
#recorrer_infijo(c)
#print()
#print(f"{recorrer_infijo_string(c)}\n")
#
#d = crear_arbol_prefijo("| & | & true true true true true")
#recorrer_infijo(d)
#print()
#print(f"{recorrer_infijo_string(d)}\n")
#
#e = crear_arbol_prefijo("| & ^ => true true false true")
#recorrer_infijo(e)
#print()
#print(f"{recorrer_infijo_string(e)}\n")
#
#f = crear_arbol_prefijo("=> true => true => true => true true")
#recorrer_infijo(f)
#print()
#print(f"{recorrer_infijo_string(f)}\n")
#
#g = crear_arbol_prefijo("| true & true & true | true & true true")
#recorrer_infijo(g)
#print()
#print(f"{recorrer_infijo_string(g)}\n")
#
#h = crear_arbol_prefijo("| & & | & true true true true true true")
#recorrer_infijo(h)
#print()
#print(f"{recorrer_infijo_string(h)}\n")