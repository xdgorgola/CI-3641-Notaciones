import unittest
from Notaciones import calcular_valor_prefijo, calcular_valor_postfijo, \
    NodoNotacion, crear_arbol_prefijo, crear_arbol_postfijo, recorrer_infijo_string

class BuddyAllocationTests(unittest.TestCase):

    def test_valores(self):
        """
        Prueba que los valores se parseen correctamente
        """

        self.assertFalse(calcular_valor_prefijo("false"))
        self.assertTrue(calcular_valor_prefijo("true"))

        self.assertFalse(calcular_valor_postfijo("false"))
        self.assertTrue(calcular_valor_postfijo("true"))

    
    def test_tabla_not(self):
        """
        Prueba la tabla de la verdad del operador not
        """
        
        self.assertFalse(calcular_valor_prefijo("^ true"))
        self.assertTrue(calcular_valor_prefijo("^ false"))

        self.assertFalse(calcular_valor_postfijo("true ^"))
        self.assertTrue(calcular_valor_postfijo("false ^"))


    def test_tabla_and(self):
        """
        Prueba la tabla de la verdad del operador and
        """

        self.assertFalse(calcular_valor_prefijo("& false true"))
        self.assertFalse(calcular_valor_prefijo("& true false"))
        self.assertFalse(calcular_valor_prefijo("& false false"))
        self.assertTrue(calcular_valor_prefijo("& true true"))

        self.assertFalse(calcular_valor_postfijo("false true &"))
        self.assertFalse(calcular_valor_postfijo("true false &"))
        self.assertFalse(calcular_valor_postfijo("false false &"))
        self.assertTrue(calcular_valor_postfijo("true true &"))
    

    def test_tabla_or(self):
        """
        Prueba la tabla de la verdad del operador or
        """

        self.assertTrue(calcular_valor_prefijo("| true true"))
        self.assertTrue(calcular_valor_prefijo("| true false"))
        self.assertTrue(calcular_valor_prefijo("| false true"))
        self.assertFalse(calcular_valor_prefijo("| false false"))

        self.assertTrue(calcular_valor_postfijo("true true |"))
        self.assertTrue(calcular_valor_postfijo("true false |"))
        self.assertTrue(calcular_valor_postfijo("false true |"))
        self.assertFalse(calcular_valor_postfijo("false false |"))
    

    def test_tabla_imp(self):
        """
        Prueba la tabla de la verdad del operador implicacion
        """

        self.assertTrue(calcular_valor_prefijo("=> true true"))
        self.assertFalse(calcular_valor_prefijo("=> true false"))
        self.assertTrue(calcular_valor_prefijo("=> false true"))
        self.assertTrue(calcular_valor_prefijo("=> false false"))

        self.assertTrue(calcular_valor_postfijo("true true =>"))
        self.assertFalse(calcular_valor_postfijo("true false =>"))
        self.assertTrue(calcular_valor_postfijo("false true =>"))
        self.assertTrue(calcular_valor_postfijo("false false =>"))


if __name__ == '__main__':
    unittest.main()