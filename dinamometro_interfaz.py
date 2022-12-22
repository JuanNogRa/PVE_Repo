# -*- coding: utf-8 -*-
"""
Created on Thu Jun 02 20:06:09 2022

@author: CRONERO
"""

from daqhats import mcc128, mcc152, OptionFlags, HatIDs, HatError, AnalogInputMode, AnalogInputRange
from daqhats_utils import select_hat_device
import pigpio
import read_PWM

from threading import Thread
import threading
import time
from time import sleep
from tkinter import ttk
from tkinter import *
import pandas as pd
from datetime import datetime
import math 

root = Tk()

def hilo_interfaz(args):
    global root
    
    def hilo_lectura_datos(args):
        
        def leer_voltaje(*args):   
            try:
                voltaje = float(ingreso_voltaje.get().replace(",","."))
                
                if (voltaje < voltaje_generar_minimo) or (voltaje > voltaje_generar_maximo):
                    mostrar_error.set('Por favor ingrese un número\nentre '
                          +str(voltaje_generar_minimo)+' y '
                          +str(voltaje_generar_maximo))
                    print('Por favor ingrese un número entre '
                          +str(voltaje_generar_minimo)+' y '
                          +str(voltaje_generar_maximo))
                else:
                    modulo_mcc152.a_out_write(canal_salida_analoga, voltaje, opciones)
                    print('Voltaje generado: {:.5f}'.format(voltaje, ' V  '))
                    mostrar_voltaje_canal_0.set('{:.5f}'.format(voltaje, ' V'))
                    lista_PAU.append(mostrar_voltaje_canal_0.get().replace(' V', ''))
                    entrada_PAU.delete(0, 'end')
                    mostrar_error.set('')
            except Exception:
                mostrar_error.set('Por favor ingrese un número.')
                print('Por favor ingrese un número.')
        
        boton_aplicar.configure(command=leer_voltaje)
        entrada_PAU.focus()
        root.bind('<Return>', leer_voltaje)
        
        opciones = OptionFlags.DEFAULT
        canal_salida_analoga = 0                            # Canal a usar para generar voltaje.
        canales_lectura = [0, 4]                      # Canales a usar para leer voltaje.
        modo_lectura_voltaje = AnalogInputMode.SE           # Tipo de lectura análoga (diferencial o single ended).
        rango_lectura_voltaje = AnalogInputRange.BIP_2V     # Rango de lectura análoga (-2 V a +2 V).
        
        # Inicialización MCC 128 módulo conversor análogo a digital.
        direccion_mcc128 = select_hat_device(HatIDs.MCC_128)
        modulo_mcc128 = mcc128(direccion_mcc128)
        modulo_mcc128.a_in_mode_write(modo_lectura_voltaje)
        modulo_mcc128.a_in_range_write(rango_lectura_voltaje)
        
        # Inicialización MCC 152 módulo conversor digital a análogo.
        direccion_mcc152 = select_hat_device(HatIDs.MCC_152)
        modulo_mcc152 = mcc152(direccion_mcc152)
        voltaje_generar_minimo = modulo_mcc152.info().AO_MIN_RANGE
        voltaje_generar_maximo = modulo_mcc152.info().AO_MAX_RANGE
        
        PWM_GPIO = 4
        pi = pigpio.pi()
        p = read_PWM.reader(pi, PWM_GPIO)
        
        lista_tiempo = []
        lista_excitacion = []
        lista_celda_01 = []
        lista_celda_02 = []
        lista_PAU = []
        lista_frecuencia = []
        modulo_mcc152.a_out_write(canal_salida_analoga, 0, opciones)
        print('Voltaje generado: {:.5f}'.format(0, ' V  '))
        mostrar_voltaje_canal_0.set('{:.5f}'.format(0, ' V'))
        tiempo_inicio = time.time()
        
        sensibilidad_celdas = 0.003         # Sensibilidad de las celdas de carga.
        capacidad_celdas = 2000             # Capacidad de las celdas de carga en libras.
        factor_amplificacion = 100          # Factor de amplificación del voltaje diferencial de las celdas de carga.
        factor_libras_kilos = 2.205         # Factor de conversión de libras a kilogramos.
        factor_kilos_newton = 9.80665
        
        diametro_rodillo = 19.75            # Diametro del rodillo del dinamómetro en pulgadas.
        factor_pulgadas_metros = 0.0254     # Factor de conversión de pulgadas a metros.
        pulsos_vuelta = 60                  # Cantidad de pulsos que entrega el rodillo por vuelta.
        factor_velocidad = 3.6              # Factor de conversión de velocidad(m/s) a velocidad (km/h).
        
        cantidad_muestras = 10
        
        hilo_1 = threading.currentThread()
        while getattr(hilo_1, "do_run", True):
            
            
            print ("working on %s" % args)
            
            muestras = 0
            voltaje_celda_01 = 0
            voltaje_celda_02 = 0
            
            while muestras < cantidad_muestras:
                muestras += 1
                for chan in canales_lectura:
                    if chan == 0:
                        voltaje_celda_01 += modulo_mcc128.a_in_read(chan, opciones)
                        
                    elif chan == 4:
                        voltaje_celda_02 += modulo_mcc128.a_in_read(chan, opciones)
            
            voltaje_excitacion = modulo_mcc128.a_in_read(1, opciones)
            mostrar_voltaje_excitacion.set('{:.5f}'.format(voltaje_excitacion*3, ' V'))
            lista_excitacion.append(mostrar_voltaje_excitacion.get().replace(' V', ''))
            
            mostrar_voltaje_celda_01.set('{:.5f}'.format(voltaje_celda_01/factor_amplificacion, ' V'))
            lista_celda_01.append(mostrar_voltaje_celda_01.get().replace(' V', ''))
            masa_celda_01 = (voltaje_celda_01*capacidad_celdas)/(factor_amplificacion*sensibilidad_celdas*factor_libras_kilos*voltaje_excitacion)
            torque_celda_01 = masa_celda_01*factor_kilos_newton*((diametro_rodillo*factor_pulgadas_metros)/2)
            mostrar_torque_celda_01.set('{:.2f}'.format(torque_celda_01, ' N-m'))
            
            mostrar_voltaje_celda_02.set('{:.5f}'.format(voltaje_celda_02/factor_amplificacion, ' V'))
            lista_celda_02.append(mostrar_voltaje_celda_02.get().replace(' V', ''))
            masa_celda_02 = (voltaje_celda_02*capacidad_celdas)/(factor_amplificacion*sensibilidad_celdas*factor_libras_kilos*voltaje_excitacion)
            torque_celda_02 = masa_celda_02*factor_kilos_newton*((diametro_rodillo*factor_pulgadas_metros)/2)
            mostrar_torque_celda_02.set('{:.2f}'.format(torque_celda_02, ' N-m'))
            
            frecuencia = p.frequency()
            mostrar_frecuencia.set('{:.2f}'.format(frecuencia, ' Hz'))
            lista_frecuencia.append(mostrar_frecuencia.get().replace(' Hz', ''))
            revoluciones = frecuencia/pulsos_vuelta
            #velocidad = frecuencia*((diametro_rodillo*factor_pulgadas_metros*math.pi)/pulsos_vuelta)*factor_velocidad
            mostrar_velocidad.set('{:.2f}'.format(revoluciones, ' rps'))
            
            lista_PAU.append(mostrar_voltaje_canal_0.get().replace(' V', ''))
            tiempo_final = time.time()
            lista_tiempo.append('{:.5f}'.format(tiempo_final-tiempo_inicio))
                
        print("Stopping as you wish.")
        
        datos = {'Tiempo':lista_tiempo, 
                 'Voltaje Excitación':lista_excitacion, 
                 'Voltaje Celda 01':lista_celda_01, 
                 'Voltaje Celda 02':lista_celda_02,
                 'Voltaje PAU':lista_PAU,
                 'Frecuencia':lista_frecuencia}
        #dataframe_datos = pd.DataFrame(datos)
        #fecha_hora = datetime.now().strftime("%d/%m/%Y %H/%M/%S")
        #fecha_hora = fecha_hora.replace('/', '_').replace(' ', '-')
        #dataframe_datos.to_csv(fecha_hora+'.csv', index=False)
        
    def on_closing():
        hilo_1.do_run=False
        root.destroy()
            
    def iniciar_captura(*args):
        boton_aplicar.config(state='normal')
        entrada_PAU.config(state='normal')
        boton_iniciar.config(state='disable')
        boton_detener.config(state='normal')
        hilo_1.start()
        
    def detener_captura(*args):
        hilo_1.do_run=False
        boton_aplicar.config(state='disable')
        entrada_PAU.config(state='disable')
        boton_iniciar.config(state='normal')
        boton_detener.config(state='disable')
        mostrar_voltaje_canal_0.set('')
        mostrar_error.set('')
        mostrar_voltaje_excitacion.set('')
        mostrar_voltaje_celda_01.set('')
        mostrar_voltaje_celda_02.set('')

    hilo_1 = Thread(target = hilo_lectura_datos, args = ('12',))

    w = Canvas(root, width=458, height=270)
    w.create_rectangle(166, 50, 292, 130, fill="#abb3b9")
    w.create_rectangle(312, 50, 438, 130, fill="#abb3b9")
    w.create_rectangle(20, 150, 146, 250, fill="#abb3b9")
    w.create_rectangle(166, 150, 292, 250, fill="#abb3b9")
    w.create_rectangle(312, 150, 438, 250, fill="#abb3b9")
    w.pack()
    
    ingreso_voltaje = StringVar()
    mostrar_voltaje_canal_0 = StringVar()
    mostrar_error =  StringVar()
    mostrar_voltaje_excitacion = StringVar()
    mostrar_voltaje_celda_01 = StringVar()
    mostrar_torque_celda_01 = StringVar()
    mostrar_voltaje_celda_02 = StringVar()
    mostrar_torque_celda_02 = StringVar()
    mostrar_frecuencia = StringVar()
    mostrar_velocidad = StringVar()

    boton_iniciar = ttk.Button(root, text=" Iniciar Captura ", command = iniciar_captura)
    boton_iniciar.place(x = 170, y = 20, in_ = root, anchor='center')
    
    boton_detener = ttk.Button(root, text=" Detener Captura ", command = detener_captura)
    boton_detener.place(x = 288, y = 20, in_ = root, anchor='center')
    boton_detener.config(state='disable')
    
    boton_aplicar = ttk.Button(root, text=" Aplicar Voltaje ")
    boton_aplicar.place(x = 83, y = 90, in_ = root, anchor='center')
    boton_aplicar.config(state='disable')

    entrada_PAU = ttk.Entry(root, width=10, textvariable=ingreso_voltaje)
    entrada_PAU.place(x = 83, y = 60, in_ = root, anchor='center')
    entrada_PAU.config(state='disable')

    ttk.Label(root, textvariable=mostrar_error
              ).place(x = 83, y = 120, in_ = root, anchor='center')

    ttk.Label(root, text = "Voltaje Control PAU"
              ).place(x = 229, y = 65, in_ = root, anchor='center')

    ttk.Label(root, textvariable=mostrar_voltaje_canal_0, background="#abb3b9"
              ).place(x = 229, y = 100, in_ = root, anchor='center')

    ttk.Label(root, text = "Excitación Sensores"
              ).place(x = 376, y = 65, in_ = root, anchor='center')

    ttk.Label(root, textvariable=mostrar_voltaje_excitacion, background="#abb3b9"
              ).place(x = 376, y = 100, in_ = root, anchor='center')

    ttk.Label(root, text = "Celda de Carga 01"
              ).place(x = 83, y = 165, in_ = root, anchor='center')

    ttk.Label(root, textvariable=mostrar_voltaje_celda_01, background="#abb3b9"
              ).place(x = 83, y = 195, in_ = root, anchor='center')

    ttk.Label(root, textvariable=mostrar_torque_celda_01, background="#abb3b9"
              ).place(x = 83, y = 225, in_ = root, anchor='center')

    ttk.Label(root, text = "Celda de Carga 02"
              ).place(x = 229, y = 165, in_ = root, anchor='center')

    ttk.Label(root, textvariable=mostrar_voltaje_celda_02, background="#abb3b9"
              ).place(x = 229, y = 195, in_ = root, anchor='center')

    ttk.Label(root, textvariable=mostrar_torque_celda_02, background="#abb3b9"
              ).place(x = 229, y = 225, in_ = root, anchor='center')

    ttk.Label(root, text = "Sensor de Velocidad"
              ).place(x = 376, y = 165, in_ = root, anchor='center')

    ttk.Label(root, textvariable=mostrar_frecuencia, background="#abb3b9"
              ).place(x = 376, y = 195, in_ = root, anchor='center')

    ttk.Label(root, textvariable=mostrar_velocidad, background="#abb3b9"
              ).place(x = 376, y = 225, in_ = root, anchor='center')
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
        
if __name__ == "__main__":
    root.geometry("458x270") #Dimensiones de la ventana, AnchoxAlto
    root.resizable(False, False)
    root.title("Pruebas Dinamómetro") #Titulo de la ventana principal
    #root.iconbitmap('univalle_02.ico') #Logo de la ventana principal
    
    hilo_2 = Thread(target = hilo_interfaz, args = (12,))
    hilo_2.start()
    
    root.mainloop()
