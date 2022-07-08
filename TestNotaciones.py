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


if __name__ == '__main__':
    unittest.main()