# Proyecto Calculadora de liquidación definitiva


## ¿Quién hizo esto?

David Santiago Rodríguez Ruiz
Víctor Manuel Monsalve Aguilar 

## ¿Qué es y para qué es?

Este proyecto es una calculadora de liquidación definitiva diseñada para facilitar el cálculo de aspectos relacionados con la liquidación laboral en Colombia.

## ¿Cómo lo hago funcionar?

Prerrequisitos:

Python instalado en su sistema.
Ejecución:
Para ejecutar el programa fuera del entorno de desarrollo, siga estos pasos:

Clone este repositorio en su máquina local.

Navegue a la carpeta src en la línea de comandos.

Ejecute el siguiente comando:

arduino
Copy code
python -m unittest discover ..\tests -p '*test*.py'

Para ejecutar a interfaz grafica, tener instalado kivy.
Para instalar kivy ejecuete el siguiente comando
pip install [kivy_base]

## ¿Cómo está hecho?

El proyecto sigue una estructura organizativa que promueve prácticas de Clean Code. A continuación se detalla la arquitectura del proyecto, bibliotecas utilizadas y la organización de los módulos:

## Estructura sugerida

Carpeta src: Contiene el código fuente de la lógica de la aplicación. Tiene subcarpetas por cada capa de la aplicación.

Carpeta tests: Contiene las pruebas unitarias.

Recuerde que cada carpeta de código fuente debe contener un archivo __init__.py que permite que Python reconozca la carpeta como un Módulo y pueda hacer import.

## Uso

Para ejecutar las pruebas unitarias, desde la carpeta src, use el comando:

css
Copy code
cleancode-01\src> python -m unittest discover ..\tests -p '*test*.py'
Para poder ejecutarlas desde la carpeta raíz, debe indicar la ruta de búsqueda donde se encuentran los módulos, incluyendo las siguientes líneas al inicio del módulo de pruebas:
"
python
Copy code
import sys
sys.path.append("src")
"
