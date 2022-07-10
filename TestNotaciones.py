import unittest
from Notaciones import *

class BuddyAllocationTests(unittest.TestCase):

    def test_valores(self):
        """
        Prueba que los valores se parseen correctamente
        """

        self.assertFalse(calcular_valor("false", True))
        self.assertTrue(calcular_valor("true", True))

        self.assertFalse(calcular_valor("false", False))
        self.assertTrue(calcular_valor("true", False))

    
    def test_tabla_not(self):
        """
        Prueba la tabla de la verdad del operador not
        """
        
        self.assertFalse(calcular_valor("^ true", True))
        self.assertTrue(calcular_valor("^ false", True))

        self.assertFalse(calcular_valor("true ^", False))
        self.assertTrue(calcular_valor("false ^", False))


    def test_tabla_and(self):
        """
        Prueba la tabla de la verdad del operador and
        """

        self.assertFalse(calcular_valor("& false true", True))
        self.assertFalse(calcular_valor("& true false", True))
        self.assertFalse(calcular_valor("& false false", True))
        self.assertTrue(calcular_valor("& true true", True))

        self.assertFalse(calcular_valor("false true &", False))
        self.assertFalse(calcular_valor("true false &", False))
        self.assertFalse(calcular_valor("false false &", False))
        self.assertTrue(calcular_valor("true true &", False))
    

    def test_tabla_or(self):
        """
        Prueba la tabla de la verdad del operador or
        """

        self.assertTrue(calcular_valor("| true true", True))
        self.assertTrue(calcular_valor("| true false", True))
        self.assertTrue(calcular_valor("| false true", True))
        self.assertFalse(calcular_valor("| false false", True))

        self.assertTrue(calcular_valor("true true |", False))
        self.assertTrue(calcular_valor("true false |", False))
        self.assertTrue(calcular_valor("false true |", False))
        self.assertFalse(calcular_valor("false false |", False))
    

    def test_tabla_imp(self):
        """
        Prueba la tabla de la verdad del operador implicacion
        """

        self.assertTrue(calcular_valor("=> true true", True))
        self.assertFalse(calcular_valor("=> true false", True))
        self.assertTrue(calcular_valor("=> false true", True))
        self.assertTrue(calcular_valor("=> false false", True))

        self.assertTrue(calcular_valor("true true =>", False))
        self.assertFalse(calcular_valor("true false =>", False))
        self.assertTrue(calcular_valor("false true =>", False))
        self.assertTrue(calcular_valor("false false =>", False))


    def test_asociatividad(self):
        """
        Prueba de parentizado por reglas de asociatividad izquierda y derecha
        """
        
        exp = "(((true => true) => true) => true) => true"
        self.assertTrue(exp == calcular_infijo("=> => => => true true true true true", True))
        self.assertTrue(exp == calcular_infijo("true true => true => true => true =>", False).strip())

        exp = "true => true => true => true => true"
        self.assertTrue(exp == calcular_infijo("=> true => true => true => true true", True))
        self.assertTrue(exp == calcular_infijo("true true true true true => => => =>", False).strip())

        exp = "true & (true & (true & (true & true)))"
        self.assertTrue(exp == calcular_infijo("& true & true & true & true true", True))
        self.assertTrue(exp == calcular_infijo("true true true true true & & & &", False).strip())

        exp = "true & true & true & true & true"
        self.assertTrue(exp == calcular_infijo("& & & & true true true true true", True))
        self.assertTrue(exp == calcular_infijo("true true & true & true & true &",False).strip())

        exp = "true | (true | (true | (true | true)))"
        self.assertTrue(exp == calcular_infijo("| true | true | true | true true", True))
        self.assertTrue(exp == calcular_infijo("true true true true true | | | |", False).strip())

        exp = "true | true | true | true | true"
        self.assertTrue(exp == calcular_infijo("| | | | true true true true true", True))
        self.assertTrue(exp == calcular_infijo("true true | true | true | true |",False).strip())

    
    def test_precedencia(self):
        """
        Pruebas de precedencia de operadores
        """

        exp = "(true => true) & true"
        self.assertTrue(exp == calcular_infijo("& => true true true", True))
        self.assertTrue(exp == calcular_infijo("true true => true &", False).strip())

        exp = "true & (true => true)"
        self.assertTrue(exp == calcular_infijo("& true => true true", True))
        self.assertTrue(exp == calcular_infijo("true true true => &", False).strip())

        exp = "(true => true) | true"
        self.assertTrue(exp == calcular_infijo("| => true true true", True))
        self.assertTrue(exp == calcular_infijo("true true => true |", False).strip())

        exp = "true | (true => true)"
        self.assertTrue(exp == calcular_infijo("| true => true true", True))
        self.assertTrue(exp == calcular_infijo("true true true => |", False).strip())

        exp = "^ (true & true)"
        self.assertTrue(exp == calcular_infijo("^ & true true", True).strip())
        self.assertTrue(exp == calcular_infijo("true true & ^", False).strip())

        exp = "^ (true | true)"
        self.assertTrue(exp == calcular_infijo("^ | true true", True).strip())
        self.assertTrue(exp == calcular_infijo("true true | ^", False).strip())

        exp = "^ (true => true)"
        self.assertTrue(exp == calcular_infijo("^ => true true", True).strip())
        self.assertTrue(exp == calcular_infijo("true true => ^", False).strip())

if __name__ == '__main__':  # pragma: no cover
    unittest.main()