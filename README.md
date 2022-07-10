# CI-3641-Notaciones
Evaluador de expresiones lógicas en notación pre/post fija y traductor hacia expresiones infijas hecho en Python 3.10.5 para CI-3641.

## Modo de uso
### Ejecución
Correr el archivo **SimulaDor.py** con Python 3.10.5.
### Comandos del programa
```
EVAL <ORDEN> <EXPRESION>
	Evalua la expresion <EXPRESION> escrita en orden <ORDEN>

MOSTRAR <ORDEN> <EXPRESION>
	Convierte a orden infijo la expresion <EXPRESION> con orden <ORDEN>

ORDENES PERMITIDOS:
	-PRE: Orden pre-fijo
	-POST: Orden post-fijo

SALIR
	Mata\sale del programa.
```

## Unit Testing
### Requisitos de las pruebas
- Librería **unittest** para el unit testing.
- Librería **coverage** para el code coverage.

### Ejecución de las pruebas
Para ejecutar unicamente las pruebas, ejecute sobre el archivo **TestNotaciones.py** el siguiente comando:

	py -m unittest .\TestNotaciones.py
    
Para ejecutar el code coverage, priemro ejecute sobre el archivo **TestNotaciones.py** los siguientes comandos:

	coverage run --branch -m unittest TestNotaciones.py
	coverage report

Y para una visualización html de las pruebas, luego use:

	coverage html

Lo cual generará una carpeta de nombre html que contendrá adentro un archivo **index.html** que debe abrirse con un navegador.

## De interés
- [Code Coverage](https://coverage.readthedocs.io/en/6.4.1/#:~:text=Coverage.py%20is%20a%20tool,gauge%20the%20effectiveness%20of%20tests. "Code Coverage")
- [unittest](https://docs.python.org/3/library/unittest.html "unittest")
