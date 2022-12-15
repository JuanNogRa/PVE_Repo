# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 12:05:54 2022

@author: pve_u
"""

import numpy as np
from scipy.signal import savgol_filter

#Se ingresa la velocidad maxima del vehículo

velocidadMax = 50

vel_delta_1 = 5
vel_delta_2 = 10

if velocidadMax > 130:
    vel_especificas = np.array([100, 80, 60, 40, 20])
elif velocidadMax <= 130 & velocidadMax > 100:
    vel_especificas = np.array([90, 80, 60, 40, 20])
elif velocidadMax <= 100 & velocidadMax > 70:
    vel_especificas = np.array([60, 50, 40, 30, 20])
else:
    #Preguntar si el vehículo puede alcanzar los 55 km/h
    puede = 'si'
    if puede == 'si':
        vel_especificas = np.array([50, 40, 30, 20])
    elif puede == 'no':
        vel_especificas = np.array([40, 30, 20, 30])
        
for i in vel_especificas:
    numero_pruebas = 0
    suma_interna_promedio_tiempos = 0
    promedio_tiempos = 0
    lista_promedio_tiempo_desacel = np.array([])
    precision_estadistica = 5
    
    while precision_estadistica>=4:
        
        #Pedir que se ubique el vehículo en la posición de ida. Cuando esté ubicado continuar.
        
        #VIAJE DE IDA
        #Pedir alcanzar velocidad = i+vel_delta_2, contar que se mantenga estable 5 segundos.
        #Pedir que se suelte el acelerador y se ponga el vehículo en neutro.
        #Al alcanzar velocidad = i+vel_delta_1, empezar a contar el tiempo.
        #Al alcanzar velocidad = i, empezar a guardar velocidad y aceleracion.
        #Al alcanzar velocidad = i-vel_delta_1, terminar de contar el tiempo.
        tiempo_ida = 15
        #Al alcanzar velocidad = vel_delta_1, dejar de guardar velocidad y aceleración.
        #Aplicar filtro de suavizado a señal de aceleración
        ay_sm = savgol_filter(ay, 101, 1) # window size 101, polynomial order 1
        #Obtenemos los coeficientes del polinomio de segundo grado que mejor se ajusta a velocidad vs aceleración.
        p = np.polyfit(velocidad, ay_sm, 2)
        #Guardar los tres coeficientes.
        
        #Pedir que se ubique el vehículo en la posición de vuelta. Cuando esté ubicado continuar.

        #VIAJE DE VUELTA
        #Pedir alcanzar velocidad = i+vel_delta_2, contar que se mantenga estable 5 segundos.
        #Pedir que se suelte el acelerador y se ponga el vehículo en neutro.
        #Al alcanzar velocidad = i+vel_delta_1, empezar a contar el tiempo.
        #Al alcanzar velocidad = i, empezar a guardar velocidad y aceleracion.
        #Al alcanzar velocidad = i-vel_delta_1, terminar de contar el tiempo.
        tiempo_vuelta = 17
        #Al alcanzar velocidad = vel_delta_1, dejar de guardar velocidad y aceleración.
        #Aplicar filtro de suavizado a señal de aceleración
        ay_sm = savgol_filter(ay, 101, 1) # window size 101, polynomial order 1
        #Obtenemos los coeficientes del polinomio de segundo grado que mejor se ajusta a velocidad vs aceleración.
        p = np.polyfit(velocidad, ay_sm, 2)
        #Guardar los tres coeficientes.
        
        promedio_tiempo_desacel = (tiempo_ida+tiempo_vuelta)/2
        numero_pruebas = numero_pruebas + 1
        suma_interna_promedio_tiempos += promedio_tiempo_desacel
        promedio_tiempos = (suma_interna_promedio_tiempos)/numero_pruebas;
        lista_promedio_tiempo_desacel.append([promedio_tiempo_desacel])
    
        if numero_pruebas>=4:
            if numero_pruebas == 4:
                coeficiente = 3.2
            elif numero_pruebas == 5:
                coeficiente = 2.8
            elif numero_pruebas == 6:
                coeficiente = 2.6
            elif numero_pruebas == 7:
                coeficiente = 2.5
            elif numero_pruebas == 8:
                coeficiente = 2.4
            else:
                coeficiente = 2.3
    
            suma_interna_desviacion_estandar = 0;
            for j in lista_promedio_tiempo_desacel:
                sumatoria_desviacion_estandar = (j-promedio_tiempos)^(2)
                suma_interna_desviacion_estandar += sumatoria_desviacion_estandar
        
            desviacion_estandar = (suma_interna_desviacion_estandar/(numero_pruebas-1))^(1/2)
            precision_estadistica = ((coeficiente*desviacion_estandar)/((numero_pruebas)^(1/2)))*(100/promedio_tiempos)
            #Mostrar precisión estadistica en pantalla y continuar.
        
    #Mostrar precisión estadistica en pantalla y continuar.
    #Tomar los coeficientes que se fueron guardando durante la prueba y promediarlos.
    #Mostrar los coeficientes promediados, guardar y continuar.
    
    #Preguntar si se quiere continuar con la siguiente velocidad especifica (i)
    continuar = 'si'
    if continuar == 'si':
        #Continuar con la siguiente velocidad especifica (i)
        pass
    elif continuar == 'no':
        #Salir del ciclo for
        break