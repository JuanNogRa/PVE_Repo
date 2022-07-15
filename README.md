# Repositorio del PVE del dinamómetro
En este repositorio se tiene el programa que permite utilizar el dinamómetro de Metrocali. Este programa está realizado en código Python y esta divido en tres módulos los cuales son: provisional_gui.py, CallbacksDino.py y ThreadsDino.py.  

## Descripción del módulo provisional_gui.py 
En provisional_gui.py, se tiene la interfaz diseñada en Qt Designer la cual es exportada a código python por medio de la librería PyQt5. Esta interfaz esta divida en dos pestañas, la primera corresponde a “Configuración” la cual tiene todos los campos que permiten configurar los parámetros propios del dinamómetro a utilizar. Menú para seleccionar el modo de uso con lazo de control abierto o cerrado. Menú para visualizar la señal proveniente del tacómetro con la posibilidad de cambiar la unidad de representación. Menú para visualizar las señales obtenidas de la celda de carga, PAU y excitación de los sensores también presenta la capacidad de cambiar las unidades de medición. También permite visualizar la fuerza, la potencia y potencia acumulada calculadas a partir de las señales medidas con el tacómetro y las celdas de carga. Y el menú que permite capturar las pruebas en formato “.csv” y activar la visualización en tiempo de ejecución las señales. En la pestaña “Gráfica de señales” se realiza en tiempo de ejecución las gráficas de velocidad en km y el par de torques de las celdas de torque en Newton-metro.

## Descripción del módulo CallbacksDino.py 

En CallbacksDino.py, está la lógica para el programa. Los métodos que hacen parte de este módulo son: 

init: Este método se utiliza para declarar las variables que utiliza el sistema, así como los objetos que se necesitan ejecutarse cuando se abre la aplicación. 

CloseEvent: Este método se utiliza para ejecutar el método stop() de la clase ReadVoltage que es un hilo cuando se cierre la aplicación y así garantizar que el puerto GPIO 17 que se utiliza para leer la frecuencia del tacómetro se cierre. 

ParamsInput: Este método se utiliza para definir los parámetros del dinamómetro si el mismo es cambiado. Estos parámetros son pulsos por vuelta, diámetro del rodillo y sensibilidad de celdas de carga. 


