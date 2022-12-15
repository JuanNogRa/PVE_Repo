# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 12:16:19 2022

@author: CRONERO
"""

from simpful import *
from daqhats import mcc128, mcc152, OptionFlags, HatIDs, HatError, AnalogInputMode, AnalogInputRange
from daqhats_utils import select_hat_device
import pigpio
import read_PWM

from threading import Thread
import threading
import time
from time import sleep
import pandas as pd
from datetime import datetime
import math

torque_deseado = 1

def hilo_lectura(args):
    
    def hilo_cambio_torque(args):
        global torque_deseado
        
        hilo_2 = threading.currentThread()
        while getattr(hilo_2, "do_run", True):
            
            mensaje = ("Ingrese el torque deseado (entre 1 y 400 N-m). "
                       "Para salir, escriba un valor no numerico: ")
    
            valor = input(mensaje)
            
            try:
                torque_deseado = float(valor)
            except ValueError:
                hilo_2.do_run=False
                hilo_1.do_run=False
    
    def sistema_mamdani():
        FS = FuzzySystem()

        T_1 = FuzzySet(function=Triangular_MF(a=0, b=37, c=94), term="N")
        T_2 = FuzzySet(function=Triangular_MF(a=37, b=94, c=175), term="MB")
        T_3 = FuzzySet(function=Triangular_MF(a=94, b=175, c=270), term="B")
        T_4 = FuzzySet(function=Triangular_MF(a=175, b=270, c=388), term="M")
        T_5 = FuzzySet(function=Triangular_MF(a=270, b=388, c=520), term="A")
        T_6 = FuzzySet(function=Triangular_MF(a=388, b=520, c=520), term="MA")
        LV1 = LinguisticVariable([T_1, T_2, T_3, T_4, T_5, T_6], concept="Torque Medido", universe_of_discourse=[0,500])
        FS.add_linguistic_variable("T", LV1)

        RPM_1 = FuzzySet(function=Triangular_MF(a=0, b=0, c=50), term="N")
        RPM_2 = FuzzySet(function=Triangular_MF(a=0, b=50, c=100), term="B")
        RPM_3 = FuzzySet(function=Trapezoidal_MF(a=80, b=150, c=400, d=550), term="M")
        RPM_4 = FuzzySet(function=Triangular_MF(a=450, b=550, c=550), term="A")
        LV2 = LinguisticVariable([RPM_1, RPM_2, RPM_3, RPM_4], concept="RPM Medido", universe_of_discourse=[0,550])
        FS.add_linguistic_variable("RPM", LV2)

        ET_1 = FuzzySet(function=Triangular_MF(a=-500, b=-500, c=-400), term="NMA")
        ET_2 = FuzzySet(function=Triangular_MF(a=-500, b=-400, c=-300), term="NA")
        ET_3 = FuzzySet(function=Triangular_MF(a=-400, b=-300, c=-200), term="NM")
        ET_4 = FuzzySet(function=Triangular_MF(a=-300, b=-200, c=-100), term="NB")
        ET_5 = FuzzySet(function=Triangular_MF(a=-200, b=-100, c=0), term="NMB")
        ET_6 = FuzzySet(function=Triangular_MF(a=-100, b=-2, c=0), term="NN")
        ET_7 = FuzzySet(function=Triangular_MF(a=0, b=2, c=100), term="PN")
        ET_8 = FuzzySet(function=Triangular_MF(a=0, b=100, c=200), term="PMB")
        ET_9 = FuzzySet(function=Triangular_MF(a=100, b=200, c=300), term="PB")
        ET_10 = FuzzySet(function=Triangular_MF(a=200, b=300, c=400), term="PM")
        ET_11 = FuzzySet(function=Triangular_MF(a=300, b=400, c=500), term="PA")
        ET_12 = FuzzySet(function=Triangular_MF(a=400, b=500, c=500), term="PMA")
        LV3 = LinguisticVariable([ET_1, ET_2, ET_3, ET_4, ET_5, ET_6, ET_7, ET_8, ET_9, ET_10, ET_11, ET_12], concept="Error de Torque", universe_of_discourse=[-500,500])
        FS.add_linguistic_variable("ET", LV3)

        CET_1 = FuzzySet(function=Triangular_MF(a=-100, b=-100, c=-80), term="NMA")
        CET_2 = FuzzySet(function=Triangular_MF(a=-100, b=-80, c=-60), term="NA")
        CET_3 = FuzzySet(function=Triangular_MF(a=-80, b=-60, c=-40), term="NM")
        CET_4 = FuzzySet(function=Triangular_MF(a=-60, b=-40, c=-20), term="NB")
        CET_5 = FuzzySet(function=Triangular_MF(a=-40, b=-20, c=0), term="NMB")
        CET_6 = FuzzySet(function=Triangular_MF(a=-20, b=0, c=20), term="N")
        CET_7 = FuzzySet(function=Triangular_MF(a=0, b=20, c=40), term="PMB")
        CET_8 = FuzzySet(function=Triangular_MF(a=20, b=40, c=60), term="PB")
        CET_9 = FuzzySet(function=Triangular_MF(a=40, b=60, c=80), term="PM")
        CET_10 = FuzzySet(function=Triangular_MF(a=60, b=80, c=100), term="PA")
        CET_11 = FuzzySet(function=Triangular_MF(a=80, b=100, c=100), term="PMA")
        LV4 = LinguisticVariable([CET_1, CET_2, CET_3, CET_4, CET_5, CET_6, CET_7, CET_8, CET_9, CET_10, CET_11], concept="Cambio en Error de Torque", universe_of_discourse=[-100,100])
        FS.add_linguistic_variable("CET", LV4)

        V_1 = FuzzySet(function=Triangular_MF(a=0, b=0, c=0.2), term="N")
        V_2 = FuzzySet(function=Triangular_MF(a=0, b=0.2, c=0.4), term="MB")
        V_3 = FuzzySet(function=Triangular_MF(a=0.2, b=0.4, c=0.6), term="B")
        V_4 = FuzzySet(function=Triangular_MF(a=0.4, b=0.6, c=0.8), term="M")
        V_5 = FuzzySet(function=Triangular_MF(a=0.6, b=0.8, c=1.0), term="A")
        V_6 = FuzzySet(function=Triangular_MF(a=0.8, b=1.0, c=1.2), term="MA")
        V_7 = FuzzySet(function=Triangular_MF(a=1.0, b=1.2, c=1.4), term="EA")
        V_8 = FuzzySet(function=Triangular_MF(a=1.2, b=1.4, c=1.4), term="L")
        LV5 = LinguisticVariable([V_1, V_2, V_3, V_4, V_5, V_6, V_7, V_8], concept="Voltaje de Control", universe_of_discourse=[0,1.4])
        FS.add_linguistic_variable("V", LV5)

        RULES = []
        RULES.append("IF ((RPM IS N) OR (RPM IS B)) AND (T IS N) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS M)")
        RULES.append("IF ((RPM IS N) OR (RPM IS B)) AND (T IS N) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS N) OR (CET IS PMB)) THEN (V IS A)")
        RULES.append("IF ((RPM IS N) OR (RPM IS B)) AND (T IS N) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS MA)")
        RULES.append("IF ((RPM IS N) OR (RPM IS B)) AND (T IS N) AND ((ET IS NN) OR (ET IS PN)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS MB)")
        RULES.append("IF ((RPM IS N) OR (RPM IS B)) AND (T IS N) AND ((ET IS NN) OR (ET IS PN)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS N)")
        RULES.append("IF ((RPM IS N) OR (RPM IS B)) AND (T IS N) AND ((ET IS PMB) OR (ET IS PB) OR (ET IS PM) OR (ET IS PA) OR (ET IS PMA)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS B)")
        RULES.append("IF ((RPM IS N) OR (RPM IS B)) AND (T IS N) AND ((ET IS PMB) OR (ET IS PB) OR (ET IS PM) OR (ET IS PA) OR (ET IS PMA)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS MB)")
        RULES.append("IF ((RPM IS N) OR (RPM IS B)) AND (T IS MB) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS M)")
        RULES.append("IF ((RPM IS N) OR (RPM IS B)) AND (T IS MB) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS N) OR (CET IS PMB)) THEN (V IS A)")
        RULES.append("IF ((RPM IS N) OR (RPM IS B)) AND (T IS MB) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS MA)")
        RULES.append("IF ((RPM IS N) OR (RPM IS B)) AND (T IS MB) AND ((ET IS NN) OR (ET IS PN)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS M)")
        RULES.append("IF ((RPM IS N) OR (RPM IS B)) AND (T IS MB) AND ((ET IS NN) OR (ET IS PN)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS B)")
        RULES.append("IF ((RPM IS N) OR (RPM IS B)) AND (T IS MB) AND ((ET IS PMB) OR (ET IS PB) OR (ET IS PM) OR (ET IS PA) OR (ET IS PMA)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS N)")
        RULES.append("IF ((RPM IS N) OR (RPM IS B)) AND (T IS MB) AND ((ET IS PMB) OR (ET IS PB) OR (ET IS PM) OR (ET IS PA) OR (ET IS PMA)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS B)")
        RULES.append("IF ((RPM IS N) OR (RPM IS B)) AND (T IS B) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS A)")
        RULES.append("IF ((RPM IS N) OR (RPM IS B)) AND (T IS B) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS MA)")
        RULES.append("IF ((RPM IS N) OR (RPM IS B)) AND (T IS B) AND ((ET IS NN) OR (ET IS PN)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS A)")
        RULES.append("IF ((RPM IS N) OR (RPM IS B)) AND (T IS B) AND ((ET IS NN) OR (ET IS PN)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS M)")
        RULES.append("IF ((RPM IS N) OR (RPM IS B)) AND (T IS B) AND ((ET IS PMB) OR (ET IS PB) OR (ET IS PM) OR (ET IS PA) OR (ET IS PMA)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS MB)")
        RULES.append("IF ((RPM IS N) OR (RPM IS B)) AND (T IS B) AND ((ET IS PMB) OR (ET IS PB) OR (ET IS PM) OR (ET IS PA) OR (ET IS PMA)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS B)")
        RULES.append("IF ((RPM IS N) OR (RPM IS B)) AND (T IS M) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS A)")
        RULES.append("IF ((RPM IS N) OR (RPM IS B)) AND (T IS M) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS MA)")
        RULES.append("IF ((RPM IS N) OR (RPM IS B)) AND (T IS M) AND ((ET IS NN) OR (ET IS PN)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS MA)")
        RULES.append("IF ((RPM IS N) OR (RPM IS B)) AND (T IS M) AND ((ET IS NN) OR (ET IS PN)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS A)")
        RULES.append("IF ((RPM IS N) OR (RPM IS B)) AND (T IS M) AND ((ET IS PMB) OR (ET IS PB) OR (ET IS PM) OR (ET IS PA) OR (ET IS PMA)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS MB)")
        RULES.append("IF ((RPM IS N) OR (RPM IS B)) AND (T IS M) AND ((ET IS PMB) OR (ET IS PB) OR (ET IS PM) OR (ET IS PA) OR (ET IS PMA)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS M)")
        RULES.append("IF ((RPM IS N) OR (RPM IS B)) AND (T IS A) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS A)")
        RULES.append("IF ((RPM IS N) OR (RPM IS B)) AND (T IS A) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS MA)")
        RULES.append("IF ((RPM IS N) OR (RPM IS B)) AND (T IS A) AND ((ET IS NN) OR (ET IS PN)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA) OR (CET IS N)) THEN (V IS MA)")
        RULES.append("IF ((RPM IS N) OR (RPM IS B)) AND (T IS A) AND ((ET IS NN) OR (ET IS PN)) AND ((CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS A)")
        RULES.append("IF ((RPM IS N) OR (RPM IS B)) AND (T IS A) AND ((ET IS PMB) OR (ET IS PB) OR (ET IS PM) OR (ET IS PA) OR (ET IS PMA)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS MB)")
        RULES.append("IF ((RPM IS N) OR (RPM IS B)) AND (T IS A) AND ((ET IS PMB) OR (ET IS PB) OR (ET IS PM) OR (ET IS PA) OR (ET IS PMA)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS M)")
        RULES.append("IF ((RPM IS N) OR (RPM IS B)) AND (T IS MA) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA) OR (CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS MA)")
        RULES.append("IF ((RPM IS N) OR (RPM IS B)) AND (T IS MA) AND ((ET IS NN) OR (ET IS PN)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA) OR (CET IS N)) THEN (V IS MA)")
        RULES.append("IF ((RPM IS N) OR (RPM IS B)) AND (T IS MA) AND ((ET IS NN) OR (ET IS PN)) AND ((CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS MA)")
        RULES.append("IF ((RPM IS N) OR (RPM IS B)) AND (T IS MA) AND ((ET IS PMB) OR (ET IS PB) OR (ET IS PM) OR (ET IS PA) OR (ET IS PMA)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS MB)")
        RULES.append("IF ((RPM IS N) OR (RPM IS B)) AND (T IS MA) AND ((ET IS PMB) OR (ET IS PB) OR (ET IS PM) OR (ET IS PA) OR (ET IS PMA)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS M)")

        RULES.append("IF (RPM IS M) AND (T IS N) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS A)")
        RULES.append("IF (RPM IS M) AND (T IS N) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS N) OR (CET IS PMB)) THEN (V IS MA)")
        RULES.append("IF (RPM IS M) AND (T IS N) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS EA)")
        RULES.append("IF (RPM IS M) AND (T IS N) AND ((ET IS NN) OR (ET IS PN)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS MB)")
        RULES.append("IF (RPM IS M) AND (T IS N) AND ((ET IS NN) OR (ET IS PN)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS N)")
        RULES.append("IF (RPM IS M) AND (T IS N) AND ((ET IS PMB) OR (ET IS PB) OR (ET IS PM) OR (ET IS PA) OR (ET IS PMA)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS B)")
        RULES.append("IF (RPM IS M) AND (T IS N) AND ((ET IS PMB) OR (ET IS PB) OR (ET IS PM) OR (ET IS PA) OR (ET IS PMA)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS MB)")
        RULES.append("IF (RPM IS M) AND (T IS MB) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS A)")
        RULES.append("IF (RPM IS M) AND (T IS MB) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS N) OR (CET IS PMB)) THEN (V IS MA)")
        RULES.append("IF (RPM IS M) AND (T IS MB) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS EA)")
        RULES.append("IF (RPM IS M) AND (T IS MB) AND ((ET IS NN) OR (ET IS PN)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS M)")
        RULES.append("IF (RPM IS M) AND (T IS MB) AND ((ET IS NN) OR (ET IS PN)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS B)")
        RULES.append("IF (RPM IS M) AND (T IS MB) AND ((ET IS PMB) OR (ET IS PB) OR (ET IS PM) OR (ET IS PA) OR (ET IS PMA)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS N)")
        RULES.append("IF (RPM IS M) AND (T IS MB) AND ((ET IS PMB) OR (ET IS PB) OR (ET IS PM) OR (ET IS PA) OR (ET IS PMA)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS B)")
        RULES.append("IF (RPM IS M) AND (T IS B) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS MA)")
        RULES.append("IF (RPM IS M) AND (T IS B) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS EA)")
        RULES.append("IF (RPM IS M) AND (T IS B) AND ((ET IS NN) OR (ET IS PN)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS A)")
        RULES.append("IF (RPM IS M) AND (T IS B) AND ((ET IS NN) OR (ET IS PN)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS M)")
        RULES.append("IF (RPM IS M) AND (T IS B) AND ((ET IS PMB) OR (ET IS PB) OR (ET IS PM) OR (ET IS PA) OR (ET IS PMA)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS MB)")
        RULES.append("IF (RPM IS M) AND (T IS B) AND ((ET IS PMB) OR (ET IS PB) OR (ET IS PM) OR (ET IS PA) OR (ET IS PMA)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS B)")
        RULES.append("IF (RPM IS M) AND (T IS M) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS MA)")
        RULES.append("IF (RPM IS M) AND (T IS M) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS EA)")
        RULES.append("IF (RPM IS M) AND (T IS M) AND ((ET IS NN) OR (ET IS PN)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS MA)")
        RULES.append("IF (RPM IS M) AND (T IS M) AND ((ET IS NN) OR (ET IS PN)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS A)")
        RULES.append("IF (RPM IS M) AND (T IS M) AND ((ET IS PMB) OR (ET IS PB) OR (ET IS PM) OR (ET IS PA) OR (ET IS PMA)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS MB)")
        RULES.append("IF (RPM IS M) AND (T IS M) AND ((ET IS PMB) OR (ET IS PB) OR (ET IS PM) OR (ET IS PA) OR (ET IS PMA)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS M)")
        RULES.append("IF (RPM IS M) AND (T IS A) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS MA)")
        RULES.append("IF (RPM IS M) AND (T IS A) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS EA)")
        RULES.append("IF (RPM IS M) AND (T IS A) AND ((ET IS NN) OR (ET IS PN)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS EA)")
        RULES.append("IF (RPM IS M) AND (T IS A) AND ((ET IS NN) OR (ET IS PN)) AND (CET IS N) THEN (V IS MA)")
        RULES.append("IF (RPM IS M) AND (T IS A) AND ((ET IS NN) OR (ET IS PN)) AND ((CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS A)")
        RULES.append("IF (RPM IS M) AND (T IS A) AND ((ET IS PMB) OR (ET IS PB) OR (ET IS PM) OR (ET IS PA) OR (ET IS PMA)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS MB)")
        RULES.append("IF (RPM IS M) AND (T IS A) AND ((ET IS PMB) OR (ET IS PB) OR (ET IS PM) OR (ET IS PA) OR (ET IS PMA)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS M)")
        RULES.append("IF (RPM IS M) AND (T IS MA) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA) OR (CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS EA)")
        RULES.append("IF (RPM IS M) AND (T IS MA) AND ((ET IS NN) OR (ET IS PN)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA) OR (CET IS N)) THEN (V IS EA)")
        RULES.append("IF (RPM IS M) AND (T IS MA) AND ((ET IS NN) OR (ET IS PN)) AND ((CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS MA)")
        RULES.append("IF (RPM IS M) AND (T IS MA) AND ((ET IS PMB) OR (ET IS PB) OR (ET IS PM) OR (ET IS PA) OR (ET IS PMA)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS MB)")
        RULES.append("IF (RPM IS M) AND (T IS MA) AND ((ET IS PMB) OR (ET IS PB) OR (ET IS PM) OR (ET IS PA) OR (ET IS PMA)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS M)")

        RULES.append("IF (RPM IS A) AND (T IS N) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS A)")
        RULES.append("IF (RPM IS A) AND (T IS N) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS N) OR (CET IS PMB)) THEN (V IS MA)")
        RULES.append("IF (RPM IS A) AND (T IS N) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS EA)")
        RULES.append("IF (RPM IS A) AND (T IS N) AND ((ET IS NN) OR (ET IS PN)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS MB)")
        RULES.append("IF (RPM IS A) AND (T IS N) AND ((ET IS NN) OR (ET IS PN)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS N)")
        RULES.append("IF (RPM IS A) AND (T IS N) AND ((ET IS PMB) OR (ET IS PB) OR (ET IS PM) OR (ET IS PA) OR (ET IS PMA)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS B)")
        RULES.append("IF (RPM IS A) AND (T IS N) AND ((ET IS PMB) OR (ET IS PB) OR (ET IS PM) OR (ET IS PA) OR (ET IS PMA)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS MB)")
        RULES.append("IF (RPM IS A) AND (T IS MB) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS MA)")
        RULES.append("IF (RPM IS A) AND (T IS MB) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS N) OR (CET IS PMB)) THEN (V IS EA)")
        RULES.append("IF (RPM IS A) AND (T IS MB) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS L)")
        RULES.append("IF (RPM IS A) AND (T IS MB) AND ((ET IS NN) OR (ET IS PN)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS A)")
        RULES.append("IF (RPM IS A) AND (T IS MB) AND ((ET IS NN) OR (ET IS PN)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS M)")
        RULES.append("IF (RPM IS A) AND (T IS MB) AND ((ET IS PMB) OR (ET IS PB) OR (ET IS PM) OR (ET IS PA) OR (ET IS PMA)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS MB)")
        RULES.append("IF (RPM IS A) AND (T IS MB) AND ((ET IS PMB) OR (ET IS PB) OR (ET IS PM) OR (ET IS PA) OR (ET IS PMA)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS M)")
        RULES.append("IF (RPM IS A) AND (T IS B) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS EA)")
        RULES.append("IF (RPM IS A) AND (T IS B) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS L)")
        RULES.append("IF (RPM IS A) AND (T IS B) AND ((ET IS NN) OR (ET IS PN)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS MA)")
        RULES.append("IF (RPM IS A) AND (T IS B) AND ((ET IS NN) OR (ET IS PN)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS A)")
        RULES.append("IF (RPM IS A) AND (T IS B) AND ((ET IS PMB) OR (ET IS PB) OR (ET IS PM) OR (ET IS PA) OR (ET IS PMA)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS B)")
        RULES.append("IF (RPM IS A) AND (T IS B) AND ((ET IS PMB) OR (ET IS PB) OR (ET IS PM) OR (ET IS PA) OR (ET IS PMA)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS M)")
        RULES.append("IF (RPM IS A) AND (T IS M) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS EA)")
        RULES.append("IF (RPM IS A) AND (T IS M) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS L)")
        RULES.append("IF (RPM IS A) AND (T IS M) AND ((ET IS NN) OR (ET IS PN)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS EA)")
        RULES.append("IF (RPM IS A) AND (T IS M) AND ((ET IS NN) OR (ET IS PN)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS MA)")
        RULES.append("IF (RPM IS A) AND (T IS M) AND ((ET IS PMB) OR (ET IS PB) OR (ET IS PM) OR (ET IS PA) OR (ET IS PMA)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS B)")
        RULES.append("IF (RPM IS A) AND (T IS M) AND ((ET IS PMB) OR (ET IS PB) OR (ET IS PM) OR (ET IS PA) OR (ET IS PMA)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS A)")
        RULES.append("IF (RPM IS A) AND (T IS A) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS EA)")
        RULES.append("IF (RPM IS A) AND (T IS A) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS L)")
        RULES.append("IF (RPM IS A) AND (T IS A) AND ((ET IS NN) OR (ET IS PN)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS L)")
        RULES.append("IF (RPM IS A) AND (T IS A) AND ((ET IS NN) OR (ET IS PN)) AND (CET IS N) THEN (V IS EA)")
        RULES.append("IF (RPM IS A) AND (T IS A) AND ((ET IS NN) OR (ET IS PN)) AND ((CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS MA)")
        RULES.append("IF (RPM IS A) AND (T IS A) AND ((ET IS PMB) OR (ET IS PB) OR (ET IS PM) OR (ET IS PA) OR (ET IS PMA)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS B)")
        RULES.append("IF (RPM IS A) AND (T IS A) AND ((ET IS PMB) OR (ET IS PB) OR (ET IS PM) OR (ET IS PA) OR (ET IS PMA)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS A)")
        RULES.append("IF (RPM IS A) AND (T IS MA) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA) OR (CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS L)")
        RULES.append("IF (RPM IS A) AND (T IS MA) AND ((ET IS NN) OR (ET IS PN)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA) OR (CET IS N)) THEN (V IS L)")
        RULES.append("IF (RPM IS A) AND (T IS MA) AND ((ET IS NN) OR (ET IS PN)) AND ((CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS EA)")
        RULES.append("IF (RPM IS A) AND (T IS MA) AND ((ET IS PMB) OR (ET IS PB) OR (ET IS PM) OR (ET IS PA) OR (ET IS PMA)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS B)")
        RULES.append("IF (RPM IS A) AND (T IS MA) AND ((ET IS PMB) OR (ET IS PB) OR (ET IS PM) OR (ET IS PA) OR (ET IS PMA)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS A)")

        FS.add_rules(RULES)
        return FS

    def sistema_sugeno():
        FS = FuzzySystem()

        T_1 = FuzzySet(function=Triangular_MF(a=0, b=37, c=94), term="N")
        T_2 = FuzzySet(function=Triangular_MF(a=37, b=94, c=175), term="MB")
        T_3 = FuzzySet(function=Triangular_MF(a=94, b=175, c=270), term="B")
        T_4 = FuzzySet(function=Triangular_MF(a=175, b=270, c=388), term="M")
        T_5 = FuzzySet(function=Triangular_MF(a=270, b=388, c=520), term="A")
        T_6 = FuzzySet(function=Triangular_MF(a=388, b=520, c=520), term="MA")
        LV1 = LinguisticVariable([T_1, T_2, T_3, T_4, T_5, T_6], concept="Torque Medido", universe_of_discourse=[0,500])
        FS.add_linguistic_variable("T", LV1)

        RPM_1 = FuzzySet(function=Triangular_MF(a=0, b=0, c=50), term="N")
        RPM_2 = FuzzySet(function=Triangular_MF(a=0, b=50, c=100), term="B")
        RPM_3 = FuzzySet(function=Trapezoidal_MF(a=80, b=150, c=400, d=550), term="M")
        RPM_4 = FuzzySet(function=Triangular_MF(a=450, b=550, c=550), term="A")
        LV2 = LinguisticVariable([RPM_1, RPM_2, RPM_3, RPM_4], concept="RPM Medido", universe_of_discourse=[0,550])
        FS.add_linguistic_variable("RPM", LV2)

        ET_1 = FuzzySet(function=Triangular_MF(a=-500, b=-500, c=-400), term="NMA")
        ET_2 = FuzzySet(function=Triangular_MF(a=-500, b=-400, c=-300), term="NA")
        ET_3 = FuzzySet(function=Triangular_MF(a=-400, b=-300, c=-200), term="NM")
        ET_4 = FuzzySet(function=Triangular_MF(a=-300, b=-200, c=-100), term="NB")
        ET_5 = FuzzySet(function=Triangular_MF(a=-200, b=-100, c=0), term="NMB")
        ET_6 = FuzzySet(function=Triangular_MF(a=-100, b=-2, c=0), term="NN")
        ET_7 = FuzzySet(function=Triangular_MF(a=0, b=2, c=100), term="PN")
        ET_8 = FuzzySet(function=Triangular_MF(a=0, b=100, c=200), term="PMB")
        ET_9 = FuzzySet(function=Triangular_MF(a=100, b=200, c=300), term="PB")
        ET_10 = FuzzySet(function=Triangular_MF(a=200, b=300, c=400), term="PM")
        ET_11 = FuzzySet(function=Triangular_MF(a=300, b=400, c=500), term="PA")
        ET_12 = FuzzySet(function=Triangular_MF(a=400, b=500, c=500), term="PMA")
        LV3 = LinguisticVariable([ET_1, ET_2, ET_3, ET_4, ET_5, ET_6, ET_7, ET_8, ET_9, ET_10, ET_11, ET_12], concept="Error de Torque", universe_of_discourse=[-500,500])
        FS.add_linguistic_variable("ET", LV3)

        CET_1 = FuzzySet(function=Triangular_MF(a=-100, b=-100, c=-80), term="NMA")
        CET_2 = FuzzySet(function=Triangular_MF(a=-100, b=-80, c=-60), term="NA")
        CET_3 = FuzzySet(function=Triangular_MF(a=-80, b=-60, c=-40), term="NM")
        CET_4 = FuzzySet(function=Triangular_MF(a=-60, b=-40, c=-20), term="NB")
        CET_5 = FuzzySet(function=Triangular_MF(a=-40, b=-20, c=0), term="NMB")
        CET_6 = FuzzySet(function=Triangular_MF(a=-20, b=0, c=20), term="N")
        CET_7 = FuzzySet(function=Triangular_MF(a=0, b=20, c=40), term="PMB")
        CET_8 = FuzzySet(function=Triangular_MF(a=20, b=40, c=60), term="PB")
        CET_9 = FuzzySet(function=Triangular_MF(a=40, b=60, c=80), term="PM")
        CET_10 = FuzzySet(function=Triangular_MF(a=60, b=80, c=100), term="PA")
        CET_11 = FuzzySet(function=Triangular_MF(a=80, b=100, c=100), term="PMA")
        LV4 = LinguisticVariable([CET_1, CET_2, CET_3, CET_4, CET_5, CET_6, CET_7, CET_8, CET_9, CET_10, CET_11], concept="Cambio en Error de Torque", universe_of_discourse=[-100,100])
        FS.add_linguistic_variable("CET", LV4)

        FS.set_crisp_output_value("N", 0.0)
        FS.set_crisp_output_value("MB", 0.2)
        FS.set_crisp_output_value("B", 0.4)
        FS.set_crisp_output_value("M", 0.6)
        FS.set_crisp_output_value("A", 0.8)
        FS.set_crisp_output_value("MA", 1.0)
        FS.set_crisp_output_value("EA", 1.2)
        FS.set_crisp_output_value("L", 1.4)

        RULES = []
        RULES.append("IF ((RPM IS N) OR (RPM IS B)) AND (T IS N) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS M)")
        RULES.append("IF ((RPM IS N) OR (RPM IS B)) AND (T IS N) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS N) OR (CET IS PMB)) THEN (V IS A)")
        RULES.append("IF ((RPM IS N) OR (RPM IS B)) AND (T IS N) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS MA)")
        RULES.append("IF ((RPM IS N) OR (RPM IS B)) AND (T IS N) AND ((ET IS NN) OR (ET IS PN)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS MB)")
        RULES.append("IF ((RPM IS N) OR (RPM IS B)) AND (T IS N) AND ((ET IS NN) OR (ET IS PN)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS N)")
        RULES.append("IF ((RPM IS N) OR (RPM IS B)) AND (T IS N) AND ((ET IS PMB) OR (ET IS PB) OR (ET IS PM) OR (ET IS PA) OR (ET IS PMA)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS B)")
        RULES.append("IF ((RPM IS N) OR (RPM IS B)) AND (T IS N) AND ((ET IS PMB) OR (ET IS PB) OR (ET IS PM) OR (ET IS PA) OR (ET IS PMA)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS MB)")
        RULES.append("IF ((RPM IS N) OR (RPM IS B)) AND (T IS MB) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS M)")
        RULES.append("IF ((RPM IS N) OR (RPM IS B)) AND (T IS MB) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS N) OR (CET IS PMB)) THEN (V IS A)")
        RULES.append("IF ((RPM IS N) OR (RPM IS B)) AND (T IS MB) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS MA)")
        RULES.append("IF ((RPM IS N) OR (RPM IS B)) AND (T IS MB) AND ((ET IS NN) OR (ET IS PN)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS M)")
        RULES.append("IF ((RPM IS N) OR (RPM IS B)) AND (T IS MB) AND ((ET IS NN) OR (ET IS PN)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS B)")
        RULES.append("IF ((RPM IS N) OR (RPM IS B)) AND (T IS MB) AND ((ET IS PMB) OR (ET IS PB) OR (ET IS PM) OR (ET IS PA) OR (ET IS PMA)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS N)")
        RULES.append("IF ((RPM IS N) OR (RPM IS B)) AND (T IS MB) AND ((ET IS PMB) OR (ET IS PB) OR (ET IS PM) OR (ET IS PA) OR (ET IS PMA)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS B)")
        RULES.append("IF ((RPM IS N) OR (RPM IS B)) AND (T IS B) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS A)")
        RULES.append("IF ((RPM IS N) OR (RPM IS B)) AND (T IS B) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS MA)")
        RULES.append("IF ((RPM IS N) OR (RPM IS B)) AND (T IS B) AND ((ET IS NN) OR (ET IS PN)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS A)")
        RULES.append("IF ((RPM IS N) OR (RPM IS B)) AND (T IS B) AND ((ET IS NN) OR (ET IS PN)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS M)")
        RULES.append("IF ((RPM IS N) OR (RPM IS B)) AND (T IS B) AND ((ET IS PMB) OR (ET IS PB) OR (ET IS PM) OR (ET IS PA) OR (ET IS PMA)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS MB)")
        RULES.append("IF ((RPM IS N) OR (RPM IS B)) AND (T IS B) AND ((ET IS PMB) OR (ET IS PB) OR (ET IS PM) OR (ET IS PA) OR (ET IS PMA)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS B)")
        RULES.append("IF ((RPM IS N) OR (RPM IS B)) AND (T IS M) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS A)")
        RULES.append("IF ((RPM IS N) OR (RPM IS B)) AND (T IS M) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS MA)")
        RULES.append("IF ((RPM IS N) OR (RPM IS B)) AND (T IS M) AND ((ET IS NN) OR (ET IS PN)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS MA)")
        RULES.append("IF ((RPM IS N) OR (RPM IS B)) AND (T IS M) AND ((ET IS NN) OR (ET IS PN)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS A)")
        RULES.append("IF ((RPM IS N) OR (RPM IS B)) AND (T IS M) AND ((ET IS PMB) OR (ET IS PB) OR (ET IS PM) OR (ET IS PA) OR (ET IS PMA)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS MB)")
        RULES.append("IF ((RPM IS N) OR (RPM IS B)) AND (T IS M) AND ((ET IS PMB) OR (ET IS PB) OR (ET IS PM) OR (ET IS PA) OR (ET IS PMA)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS M)")
        RULES.append("IF ((RPM IS N) OR (RPM IS B)) AND (T IS A) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS A)")
        RULES.append("IF ((RPM IS N) OR (RPM IS B)) AND (T IS A) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS MA)")
        RULES.append("IF ((RPM IS N) OR (RPM IS B)) AND (T IS A) AND ((ET IS NN) OR (ET IS PN)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA) OR (CET IS N)) THEN (V IS MA)")
        RULES.append("IF ((RPM IS N) OR (RPM IS B)) AND (T IS A) AND ((ET IS NN) OR (ET IS PN)) AND ((CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS A)")
        RULES.append("IF ((RPM IS N) OR (RPM IS B)) AND (T IS A) AND ((ET IS PMB) OR (ET IS PB) OR (ET IS PM) OR (ET IS PA) OR (ET IS PMA)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS MB)")
        RULES.append("IF ((RPM IS N) OR (RPM IS B)) AND (T IS A) AND ((ET IS PMB) OR (ET IS PB) OR (ET IS PM) OR (ET IS PA) OR (ET IS PMA)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS M)")
        RULES.append("IF ((RPM IS N) OR (RPM IS B)) AND (T IS MA) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA) OR (CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS MA)")
        RULES.append("IF ((RPM IS N) OR (RPM IS B)) AND (T IS MA) AND ((ET IS NN) OR (ET IS PN)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA) OR (CET IS N)) THEN (V IS MA)")
        RULES.append("IF ((RPM IS N) OR (RPM IS B)) AND (T IS MA) AND ((ET IS NN) OR (ET IS PN)) AND ((CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS MA)")
        RULES.append("IF ((RPM IS N) OR (RPM IS B)) AND (T IS MA) AND ((ET IS PMB) OR (ET IS PB) OR (ET IS PM) OR (ET IS PA) OR (ET IS PMA)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS MB)")
        RULES.append("IF ((RPM IS N) OR (RPM IS B)) AND (T IS MA) AND ((ET IS PMB) OR (ET IS PB) OR (ET IS PM) OR (ET IS PA) OR (ET IS PMA)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS M)")

        RULES.append("IF (RPM IS M) AND (T IS N) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS A)")
        RULES.append("IF (RPM IS M) AND (T IS N) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS N) OR (CET IS PMB)) THEN (V IS MA)")
        RULES.append("IF (RPM IS M) AND (T IS N) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS EA)")
        RULES.append("IF (RPM IS M) AND (T IS N) AND ((ET IS NN) OR (ET IS PN)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS MB)")
        RULES.append("IF (RPM IS M) AND (T IS N) AND ((ET IS NN) OR (ET IS PN)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS N)")
        RULES.append("IF (RPM IS M) AND (T IS N) AND ((ET IS PMB) OR (ET IS PB) OR (ET IS PM) OR (ET IS PA) OR (ET IS PMA)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS B)")
        RULES.append("IF (RPM IS M) AND (T IS N) AND ((ET IS PMB) OR (ET IS PB) OR (ET IS PM) OR (ET IS PA) OR (ET IS PMA)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS MB)")
        RULES.append("IF (RPM IS M) AND (T IS MB) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS A)")
        RULES.append("IF (RPM IS M) AND (T IS MB) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS N) OR (CET IS PMB)) THEN (V IS MA)")
        RULES.append("IF (RPM IS M) AND (T IS MB) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS EA)")
        RULES.append("IF (RPM IS M) AND (T IS MB) AND ((ET IS NN) OR (ET IS PN)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS M)")
        RULES.append("IF (RPM IS M) AND (T IS MB) AND ((ET IS NN) OR (ET IS PN)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS B)")
        RULES.append("IF (RPM IS M) AND (T IS MB) AND ((ET IS PMB) OR (ET IS PB) OR (ET IS PM) OR (ET IS PA) OR (ET IS PMA)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS N)")
        RULES.append("IF (RPM IS M) AND (T IS MB) AND ((ET IS PMB) OR (ET IS PB) OR (ET IS PM) OR (ET IS PA) OR (ET IS PMA)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS B)")
        RULES.append("IF (RPM IS M) AND (T IS B) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS MA)")
        RULES.append("IF (RPM IS M) AND (T IS B) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS EA)")
        RULES.append("IF (RPM IS M) AND (T IS B) AND ((ET IS NN) OR (ET IS PN)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS A)")
        RULES.append("IF (RPM IS M) AND (T IS B) AND ((ET IS NN) OR (ET IS PN)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS M)")
        RULES.append("IF (RPM IS M) AND (T IS B) AND ((ET IS PMB) OR (ET IS PB) OR (ET IS PM) OR (ET IS PA) OR (ET IS PMA)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS MB)")
        RULES.append("IF (RPM IS M) AND (T IS B) AND ((ET IS PMB) OR (ET IS PB) OR (ET IS PM) OR (ET IS PA) OR (ET IS PMA)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS B)")
        RULES.append("IF (RPM IS M) AND (T IS M) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS MA)")
        RULES.append("IF (RPM IS M) AND (T IS M) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS EA)")
        RULES.append("IF (RPM IS M) AND (T IS M) AND ((ET IS NN) OR (ET IS PN)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS MA)")
        RULES.append("IF (RPM IS M) AND (T IS M) AND ((ET IS NN) OR (ET IS PN)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS A)")
        RULES.append("IF (RPM IS M) AND (T IS M) AND ((ET IS PMB) OR (ET IS PB) OR (ET IS PM) OR (ET IS PA) OR (ET IS PMA)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS MB)")
        RULES.append("IF (RPM IS M) AND (T IS M) AND ((ET IS PMB) OR (ET IS PB) OR (ET IS PM) OR (ET IS PA) OR (ET IS PMA)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS M)")
        RULES.append("IF (RPM IS M) AND (T IS A) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS MA)")
        RULES.append("IF (RPM IS M) AND (T IS A) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS EA)")
        RULES.append("IF (RPM IS M) AND (T IS A) AND ((ET IS NN) OR (ET IS PN)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS EA)")
        RULES.append("IF (RPM IS M) AND (T IS A) AND ((ET IS NN) OR (ET IS PN)) AND (CET IS N) THEN (V IS MA)")
        RULES.append("IF (RPM IS M) AND (T IS A) AND ((ET IS NN) OR (ET IS PN)) AND ((CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS A)")
        RULES.append("IF (RPM IS M) AND (T IS A) AND ((ET IS PMB) OR (ET IS PB) OR (ET IS PM) OR (ET IS PA) OR (ET IS PMA)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS MB)")
        RULES.append("IF (RPM IS M) AND (T IS A) AND ((ET IS PMB) OR (ET IS PB) OR (ET IS PM) OR (ET IS PA) OR (ET IS PMA)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS M)")
        RULES.append("IF (RPM IS M) AND (T IS MA) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA) OR (CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS EA)")
        RULES.append("IF (RPM IS M) AND (T IS MA) AND ((ET IS NN) OR (ET IS PN)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA) OR (CET IS N)) THEN (V IS EA)")
        RULES.append("IF (RPM IS M) AND (T IS MA) AND ((ET IS NN) OR (ET IS PN)) AND ((CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS MA)")
        RULES.append("IF (RPM IS M) AND (T IS MA) AND ((ET IS PMB) OR (ET IS PB) OR (ET IS PM) OR (ET IS PA) OR (ET IS PMA)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS MB)")
        RULES.append("IF (RPM IS M) AND (T IS MA) AND ((ET IS PMB) OR (ET IS PB) OR (ET IS PM) OR (ET IS PA) OR (ET IS PMA)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS M)")

        RULES.append("IF (RPM IS A) AND (T IS N) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS A)")
        RULES.append("IF (RPM IS A) AND (T IS N) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS N) OR (CET IS PMB)) THEN (V IS MA)")
        RULES.append("IF (RPM IS A) AND (T IS N) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS EA)")
        RULES.append("IF (RPM IS A) AND (T IS N) AND ((ET IS NN) OR (ET IS PN)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS MB)")
        RULES.append("IF (RPM IS A) AND (T IS N) AND ((ET IS NN) OR (ET IS PN)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS N)")
        RULES.append("IF (RPM IS A) AND (T IS N) AND ((ET IS PMB) OR (ET IS PB) OR (ET IS PM) OR (ET IS PA) OR (ET IS PMA)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS B)")
        RULES.append("IF (RPM IS A) AND (T IS N) AND ((ET IS PMB) OR (ET IS PB) OR (ET IS PM) OR (ET IS PA) OR (ET IS PMA)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS MB)")
        RULES.append("IF (RPM IS A) AND (T IS MB) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS MA)")
        RULES.append("IF (RPM IS A) AND (T IS MB) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS N) OR (CET IS PMB)) THEN (V IS EA)")
        RULES.append("IF (RPM IS A) AND (T IS MB) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS L)")
        RULES.append("IF (RPM IS A) AND (T IS MB) AND ((ET IS NN) OR (ET IS PN)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS A)")
        RULES.append("IF (RPM IS A) AND (T IS MB) AND ((ET IS NN) OR (ET IS PN)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS M)")
        RULES.append("IF (RPM IS A) AND (T IS MB) AND ((ET IS PMB) OR (ET IS PB) OR (ET IS PM) OR (ET IS PA) OR (ET IS PMA)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS MB)")
        RULES.append("IF (RPM IS A) AND (T IS MB) AND ((ET IS PMB) OR (ET IS PB) OR (ET IS PM) OR (ET IS PA) OR (ET IS PMA)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS M)")
        RULES.append("IF (RPM IS A) AND (T IS B) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS EA)")
        RULES.append("IF (RPM IS A) AND (T IS B) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS L)")
        RULES.append("IF (RPM IS A) AND (T IS B) AND ((ET IS NN) OR (ET IS PN)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS MA)")
        RULES.append("IF (RPM IS A) AND (T IS B) AND ((ET IS NN) OR (ET IS PN)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS A)")
        RULES.append("IF (RPM IS A) AND (T IS B) AND ((ET IS PMB) OR (ET IS PB) OR (ET IS PM) OR (ET IS PA) OR (ET IS PMA)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS B)")
        RULES.append("IF (RPM IS A) AND (T IS B) AND ((ET IS PMB) OR (ET IS PB) OR (ET IS PM) OR (ET IS PA) OR (ET IS PMA)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS M)")
        RULES.append("IF (RPM IS A) AND (T IS M) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS EA)")
        RULES.append("IF (RPM IS A) AND (T IS M) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS L)")
        RULES.append("IF (RPM IS A) AND (T IS M) AND ((ET IS NN) OR (ET IS PN)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS EA)")
        RULES.append("IF (RPM IS A) AND (T IS M) AND ((ET IS NN) OR (ET IS PN)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS MA)")
        RULES.append("IF (RPM IS A) AND (T IS M) AND ((ET IS PMB) OR (ET IS PB) OR (ET IS PM) OR (ET IS PA) OR (ET IS PMA)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS B)")
        RULES.append("IF (RPM IS A) AND (T IS M) AND ((ET IS PMB) OR (ET IS PB) OR (ET IS PM) OR (ET IS PA) OR (ET IS PMA)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS A)")
        RULES.append("IF (RPM IS A) AND (T IS A) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS EA)")
        RULES.append("IF (RPM IS A) AND (T IS A) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS L)")
        RULES.append("IF (RPM IS A) AND (T IS A) AND ((ET IS NN) OR (ET IS PN)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS L)")
        RULES.append("IF (RPM IS A) AND (T IS A) AND ((ET IS NN) OR (ET IS PN)) AND (CET IS N) THEN (V IS EA)")
        RULES.append("IF (RPM IS A) AND (T IS A) AND ((ET IS NN) OR (ET IS PN)) AND ((CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS MA)")
        RULES.append("IF (RPM IS A) AND (T IS A) AND ((ET IS PMB) OR (ET IS PB) OR (ET IS PM) OR (ET IS PA) OR (ET IS PMA)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS B)")
        RULES.append("IF (RPM IS A) AND (T IS A) AND ((ET IS PMB) OR (ET IS PB) OR (ET IS PM) OR (ET IS PA) OR (ET IS PMA)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS A)")
        RULES.append("IF (RPM IS A) AND (T IS MA) AND ((ET IS NMB) OR (ET IS NB) OR (ET IS NM) OR (ET IS NA) OR (ET IS NMA)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA) OR (CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS L)")
        RULES.append("IF (RPM IS A) AND (T IS MA) AND ((ET IS NN) OR (ET IS PN)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA) OR (CET IS N)) THEN (V IS L)")
        RULES.append("IF (RPM IS A) AND (T IS MA) AND ((ET IS NN) OR (ET IS PN)) AND ((CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS EA)")
        RULES.append("IF (RPM IS A) AND (T IS MA) AND ((ET IS PMB) OR (ET IS PB) OR (ET IS PM) OR (ET IS PA) OR (ET IS PMA)) AND ((CET IS NMB) OR (CET IS NB) OR (CET IS NM) OR (CET IS NA) OR (CET IS NMA)) THEN (V IS B)")
        RULES.append("IF (RPM IS A) AND (T IS MA) AND ((ET IS PMB) OR (ET IS PB) OR (ET IS PM) OR (ET IS PA) OR (ET IS PMA)) AND ((CET IS N) OR (CET IS PMB) OR (CET IS PB) OR (CET IS PM) OR (CET IS PA) OR (CET IS PMA)) THEN (V IS A)")

        FS.add_rules(RULES)
        return FS

    opciones = OptionFlags.DEFAULT
    canal_salida_analoga = 0                            # Canal a usar para generar voltaje.
    canales_lectura = [0, 4, 1, 5]                      # Canales a usar para leer voltaje.
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

    factor_atenuacion_pau = 20.1
    divisor_voltaje = 3
    offset_pau = 0.00682
    sensibilidad_celdas = 0.003         # Sensibilidad de las celdas de carga.
    capacidad_celdas = 2000             # Capacidad de las celdas de carga en libras.
    factor_amplificacion = 100          # Factor de amplificación del voltaje diferencial de las celdas de carga.
    factor_libras_kilos = 2.205         # Factor de conversión de libras a kilogramos.
    factor_kilos_newton = 9.80665

    diametro_rodillo = 19.75            # Diametro del rodillo del dinamómetro en pulgadas.
    factor_pulgadas_metros = 0.0254     # Factor de conversión de pulgadas a metros.
    pulsos_vuelta = 60                  # Cantidad de pulsos que entrega el rodillo por vuelta.
    factor_velocidad = 3.6              # Factor de conversión de velocidad(m/s) a velocidad (km/h).
    MinimaFrecuencia = (0.05*pulsos_vuelta)/(diametro_rodillo*factor_pulgadas_metros*math.pi)

    cantidad_muestras = 100
    muestras_calibración = 1000

    PWM_GPIO = 17
    pi = pigpio.pi()
    p = read_PWM.reader(pi, PWM_GPIO, MinimaFrecuencia)

    lista_tiempo = []
    lista_celda_01 = []
    lista_celda_02 = []
    lista_PAU = []
    lista_excitacion = []
    lista_frecuencia = []
    lista_torque_deseado = []
    lista_torque_actual = []
    lista_error_torque = []
    lista_cambio_error_torque = []
    lista_RPM = []
    lista_voltaje_control = []

    modulo_mcc152.a_out_write(canal_salida_analoga, 0, opciones)
    FS = sistema_mamdani()
    
    hilo_2 = Thread(target = hilo_cambio_torque, args = (12,))

    print('Eliminando offset de celdas de carga, espere por favor.')
    
    muestras = 0
    voltaje_inicial_celda_01 = 0
    voltaje_inicial_celda_02 = 0
    error_torque_anterior = 0
    
    while muestras < muestras_calibración:
        muestras += 1
        for chan in canales_lectura:
            if chan == 0:
                voltaje_inicial_celda_01 += modulo_mcc128.a_in_read(chan, opciones)
                
            elif chan == 4:
                voltaje_inicial_celda_02 += modulo_mcc128.a_in_read(chan, opciones)
                
    voltaje_inicial_celda_01 = voltaje_inicial_celda_01/muestras_calibración
    voltaje_inicial_celda_02 = voltaje_inicial_celda_02/muestras_calibración
    
    print('Offset Celda 01: {:.6f}'.format(voltaje_inicial_celda_01, ' V  '))
    print('Offset Celda 02: {:.6f}'.format(voltaje_inicial_celda_02, ' V  '))
    
    print('Captura de datos iniciada.')
    
    hilo_2.start()
    
    tiempo_inicio = time.time()
    
    hilo_1 = threading.currentThread()
    while getattr(hilo_1, "do_run", True):
        
        muestras = 0
        voltaje_celda_01 = 0
        voltaje_celda_02 = 0
        voltaje_PAU = 0
        voltaje_excitacion = 0
        
        while muestras < cantidad_muestras:
            
            muestras += 1
            for chan in canales_lectura:
                if chan == 0:
                    voltaje_dummy = modulo_mcc128.a_in_read(chan, opciones)
                    voltaje_celda_01 += voltaje_dummy - voltaje_inicial_celda_01
                    
                elif chan == 4:
                    voltaje_dummy = modulo_mcc128.a_in_read(chan, opciones)
                    voltaje_celda_02 += voltaje_dummy - voltaje_inicial_celda_02
                
                elif chan == 1:
                     voltaje_dummy = modulo_mcc128.a_in_read(chan, opciones)
                     voltaje_PAU += voltaje_dummy - offset_pau
                
                elif chan == 5:
                    voltaje_excitacion += modulo_mcc128.a_in_read(chan, opciones)
        
        voltaje_celda_01 = voltaje_celda_01/(cantidad_muestras*factor_amplificacion)
        voltaje_celda_02 = voltaje_celda_02/(cantidad_muestras*factor_amplificacion)
        voltaje_PAU = (voltaje_PAU/cantidad_muestras)*divisor_voltaje*factor_atenuacion_pau
        voltaje_excitacion = (voltaje_excitacion/cantidad_muestras)*divisor_voltaje
        frecuencia = p.frequency()
        
        lista_celda_01.append('{:.8f}'.format(voltaje_celda_01))
        lista_celda_02.append('{:.8f}'.format(voltaje_celda_02))
        lista_PAU.append('{:.6f}'.format(voltaje_PAU))
        lista_excitacion.append('{:.4f}'.format(voltaje_excitacion))
        lista_frecuencia.append('{:.4f}'.format(frecuencia))
        
        masa_celda_01 = (voltaje_celda_01*capacidad_celdas)/(sensibilidad_celdas*factor_libras_kilos*voltaje_excitacion)
        torque_celda_01 = masa_celda_01*factor_kilos_newton*((diametro_rodillo*factor_pulgadas_metros)/2)
        masa_celda_02 = (voltaje_celda_02*capacidad_celdas)/(sensibilidad_celdas*factor_libras_kilos*voltaje_excitacion)
        torque_celda_02 = masa_celda_02*factor_kilos_newton*((diametro_rodillo*factor_pulgadas_metros)/2)
        
        torque_actual = torque_celda_01 + torque_celda_02
        error_torque = torque_actual - torque_deseado
        cambio_error_torque = error_torque - error_torque_anterior
        RPM = (frecuencia/pulsos_vuelta)*60
        
        FS.set_variable("T", torque_actual)
        FS.set_variable("ET", error_torque)
        FS.set_variable("CET", cambio_error_torque)
        FS.set_variable("RPM", RPM)
        
        voltaje_control_difuso = FS.Mamdani_inference(["V"], ignore_warnings = True)
        
        
        lista_torque_deseado.append('{:.4f}'.format(torque_deseado))
        lista_torque_actual.append('{:.4f}'.format(torque_actual))
        lista_error_torque.append('{:.4f}'.format(error_torque))
        lista_cambio_error_torque.append('{:.4f}'.format(cambio_error_torque))
        lista_RPM.append('{:.4f}'.format(RPM))
        lista_voltaje_control.append('{:.4f}'.format(voltaje_control_difuso['V']))
        
        if voltaje_control_difuso['V'] > 0:
            modulo_mcc152.a_out_write(canal_salida_analoga, voltaje_control_difuso['V'], opciones)
        
        error_torque_anterior = error_torque
        
        tiempo_final = time.time()
        lista_tiempo.append('{:.6f}'.format(tiempo_final-tiempo_inicio))
        
    datos = {'Tiempo':lista_tiempo, 
             'Voltaje Excitación':lista_excitacion, 
             'Voltaje Celda 01':lista_celda_01, 
             'Voltaje Celda 02':lista_celda_02,
             'Voltaje PAU':lista_PAU,
             'Frecuencia':lista_frecuencia,
             'Torque Deseado':lista_torque_deseado,
             'Torque Actual':lista_torque_actual,
             'Error Torque':lista_error_torque,
             'Cambio Error Torque':lista_cambio_error_torque,
             'RPM':lista_RPM,
             'Voltaje Control':lista_voltaje_control}
    
    dataframe_datos = pd.DataFrame(datos)
    fecha_hora = datetime.now().strftime("%d/%m/%Y %H/%M/%S")
    fecha_hora = fecha_hora.replace('/', '_').replace(' ', '-')
    dataframe_datos.to_csv(fecha_hora+'.csv', index=False)

if __name__ == "__main__":
    hilo_1 = Thread(target = hilo_lectura, args = (12,))
    hilo_1.start()