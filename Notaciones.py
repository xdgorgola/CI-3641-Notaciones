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
    return ASOC_IZ if (simbolo == "&" or simbolo == "|") else ASOC_DE
    

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

    return token == "&" or token == "|" or token == "=>" or token == "^"


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


def crear_arbol(expresion : str, pre : bool) -> bool:
    """
    Crea un arbol representando las operaciones y valores de la 
    expresion

    Arguments:
        expresion -- Expresion a crear arbol
        pre -- El arbol es prefijo

    Returns:
        Raiz del arbol de expresion creado
    """

    tokens : list[str] = expresion.split() if pre else (expresion.split())[::-1]
    valores : list[NodoNotacion] = []
    
    while len(tokens) > 0:
        i : str = tokens.pop()
        if (not es_operador(i)):
            valores.append(NodoNotacion(i, None, None))
            continue
        
        if (i != "^"):
            izq, der = (valores[-1 if pre else -2], valores[-2 if pre else -1])
            valores = (valores[:-2]) + [(realizar_operacion_binaria_arbol(izq, der, i))]
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


def conflicto_asociativo(raiz : NodoNotacion, hijo : NodoNotacion, asoc_prueba : str) -> bool:
    """
    Determina si hay conflictos entre operadores de misma precedencia y asociatividad.

    Arguments:
        raiz -- Nodo raiz
        hijo -- Nodo hijo
        asoc_prueba -- Asociacion de los nodos

    Returns:
        True si hay conflicto. False en caso contrario.
    """

    return tiene_misma_preced(raiz, hijo) and tiene_misma_asoc(raiz, hijo) and asociacion(raiz.tok) == asoc_prueba

    
def recorrer_infijo(raiz : NodoNotacion, acumS : str = "") -> tuple[bool, str]:
    """
    Recorre un arbol de expresion y calcula tanto un string en notacion infija,
    como el valor de la expresion

    Arguments:
        raiz -- Raiz del arbol
    
    Returns:
        Tupla con valor de la expresion y traduccion a forma infija. En ese orden
    """
    l, r = (None, None)
    if (raiz.lv != None):
        l = recorrer_infijo(raiz.lv)
        if (tiene_mayor_preced(raiz, raiz.lv) or conflicto_asociativo(raiz, raiz.lv, ASOC_DE)):
            acumS += f"({l[1]})"
        else:
            acumS += f"{l[1]}"

    acumS += f" {raiz.tok} " if es_operador(raiz.tok) else f"{raiz.tok}"

    if (raiz.rv != None):
        r = recorrer_infijo(raiz.rv)
        if (tiene_mayor_preced(raiz, raiz.rv) or conflicto_asociativo(raiz, raiz.rv, ASOC_IZ)):
            acumS += f"({r[1]})"
        else:
            acumS += f"{r[1]}"
    
    if (es_operador(raiz.tok)):
        if (raiz.tok == "^"):
            return (not r[0], acumS)
        return (realizar_operacion_binaria(l[0], r[0], raiz.tok), acumS)
    
    return (valor_booleano(raiz.tok), acumS)


def calcular_valor(exp : str, pre : bool) -> bool:
    """
    Calcula el valor de una expresion

    Arguments:
        exp -- Expresion
        pre -- Es prefija o no

    Returns:
        Valor booleano de la expresion
    """

    return recorrer_infijo(crear_arbol(exp, pre))[0]


def calcular_infijo(exp : str, pre : bool) -> str:
    """
    Calcula el string infijo de una expresion

    Arguments:
        exp -- Expresion
        pre -- Es prefija o no

    Returns:
        String infijo de la expresion
    """

    return recorrer_infijo(crear_arbol(exp, pre))[1]


if __name__ == '__main__':
    print("You found a secret area!")
    quit()