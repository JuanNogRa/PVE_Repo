# Repositorio del PVE del dinamómetro
En este repositorio se tiene el programa que permite utilizar el dinamómetro de Metrocali. Este programa está realizado en código Python y esta divido en tres módulos los cuales son: provisional_gui.py, CallbacksDino.py y ThreadsDino.py.  

## Descripción del módulo provisional_gui.py 
En provisional_gui.py, se tiene la interfaz diseñada en Qt Designer la cual es exportada a código python por medio de la librería PyQt5. Esta interfaz esta divida en dos pestañas, la primera corresponde a “Configuración” la cual tiene todos los campos que permiten configurar los parámetros propios del dinamómetro a utilizar. Menú para seleccionar el modo de uso con lazo de control abierto o cerrado. Menú para visualizar la señal proveniente del tacómetro con la posibilidad de cambiar la unidad de representación. Menú para visualizar las señales obtenidas de la celda de carga, PAU y excitación de los sensores también presenta la capacidad de cambiar las unidades de medición. También permite visualizar la fuerza, la potencia y potencia acumulada calculadas a partir de las señales medidas con el tacómetro y las celdas de carga. Y el menú que permite capturar las pruebas en formato “.csv” y activar la visualización en tiempo de ejecución las señales. En la pestaña “Gráfica de señales” se realiza en tiempo de ejecución las gráficas de velocidad en km y el par de torques de las celdas de torque en Newton-metro.

## Descripción del módulo CallbacksDino.py 

En CallbacksDino.py, está la lógica para el programa. Los métodos que hacen parte de este módulo son: 

init: Este método se utiliza para declarar las variables que utiliza el sistema, así como los objetos que se necesitan ejecutarse cuando se abre la aplicación. 

CloseEvent: Este método se utiliza para ejecutar el método stop() de la clase ReadVoltage que es un hilo cuando se cierre la aplicación y así garantizar que el puerto GPIO 17 que se utiliza para leer la frecuencia del tacómetro se cierre. 

ParamsInput: Este método se utiliza para definir los parámetros del dinamómetro si el mismo es cambiado. Estos parámetros son pulsos por vuelta, diámetro del rodillo y sensibilidad de celdas de carga. 

DACVoltageDC: Este método se ejecuta al presionar el botón “Aplicar” y dependiendo del modo de control la salida de voltaje es el que se digita en el campo de edición de texto para cuando el lazo está abierto o el torque de referencia cuando el sistema de control está en lazo cerrado. 

listVelocidad  y listDistance: Los métodos listVelocidad  y listDistance son para tomar el campo seleccionado de texto correspondiente en la QList y almacenarlo en una variable para cambiar las unidades de velocidad y de distancia a las deseadas. 

OnClicked: Este método guarda el texto del botón de selección activado para luego cambiar las unidades de medición de las celdas de carga a las deseadas. 

ClickedLazo: Este método guarda el texto con la opción “Lazo abierto” o “Lazo cerrado” y así indicar al programa el modo de control. Este método se ejecuta al generarse un llamamiento al presionar alguno de los dos botones de selección. 

startTest: Método que permite guardar las variables necesarias para registrar la prueba como es la fecha y el tiempo de inicio. También como de limpiar las variables que cambiaron al ejecutar la prueba. Por último, iniciar el hilo  “Do_every” que es un temporizador que gráfica y guarda cada vez que se cumple el tiempo de muestreo definido. Este método se ejecuta al presionar el botón “Empezar”. 

stopTest: Método que permite guardar las variables que están en memoria a disco en un archivo en formato “.csv”. El método se ejecuta al presionar el botón de “Terminar”. 

VoltageSlotUpdate: Método slot que está conectado a la señal “VoltageUpdate” del hilo “ReadVoltage”  el cual cada vez que hay una emisión el método transforma las señales de voltaje de la celda de carga en masa y torque. A su vez que aplica los parámetros de calibración para los voltajes sensados. A su vez que permite imprimir los valores de las señales en la interfaz gráfica. 

FrecuencySlotUpdate: Método slot conectado a la señal “FrecuencyUpdate” del hilo “ReadVoltage” el cual cada vez que hay una emisión toma el valor de frecuencia y lo procesa para ser representada en la unidad selecciona en el método listVelocidad. También realiza el procesamiento de la distancia recorrida para representar la unidad seleccionada en el método listDistance. También se procesa junto con las variables obtenidas del método “VoltageSlotUpdate” obtener la fuerza, potencia y potencia acumulada. Se guarda en un array los valores provenientes de las señales sensadas para posterior guardado en formato “.csv”, si el sistema está operando en lazo abierto. En lazo cerrado se aplica el controlador del método “sistema_sugeno” (fuzzy logic) y también se guarda en un array tanto las señales sensadas como la señal de error del sistema.  

Time_MuestreoSlotUpdate: Método slot conectado a la señal “Muestreo_Time” del hilo “Do_every” el cual es ejecutado cada vez que se cumpla el tiempo dado al sistema o que es lo mismo cuando se cumpla la frecuencia de muestreo establecido. A parte de guardar el tiempo para posterior guardado se utiliza también para graficar las señales de velocidad y el torque de las celdas de carga. 

sistema_sugeno: método donde se tiene el sistema de control basado en lógica difusa, el cual solo se ejecuta cuando se está operando el sistema de control en lazo cerrado. 

## Descripción del módulo ThreadsDino.py 
En este módulo están todos los procesos en paralelo necesarios para usar la aplicación, los cuales están divido en los siguientes QThreads (hilos usando la librería PyQt5): ReadVoltage y Do_every. Y también la clase SendVoltage. 
