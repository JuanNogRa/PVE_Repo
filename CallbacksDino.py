from provisional_gui import *
from ThreadsDino import *
import math
import config
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMessageBox
from datetime import datetime
import pandas as pd
import time
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
from simpful import *
import numpy as np

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
       
        self.Factor_Amplificacion = 100
        self.Facto_Atenuacion = 20.1
        self.divisor_Voltaje = 3
        self.pulsos_vuelta = 60
        self.offset_pau = 0.00682
        self.diametro_rodillo = 19.75*0.0254
        self.sensibilidad_celdas = 3
        self.frecuencia = 0
        self.capacidad_celdas = 2000             # Capacidad de las celdas de carga en libras.
        self.factor_libras_kilos = 2.205         # Factor de conversión de libras a kilogramos.
        self.factor_kilos_newton = 9.80665
        self.cuentas_distancia = 0
        self.muestreo = 0
        self.MinimaFrecuencia = (0.05*self.pulsos_vuelta)/(self.diametro_rodillo*math.pi)
        self.offsetCelda1 = 0.0
        self.offsetCelda2 = 0.0
        self.error_torque_anterior = 0.0
        #self.ReadFrecuency.FrecuencyUpdate.connect(self.FrecuencySlotUpdate)
            #f(*args)
        
        self.value=''
        self.VTorque = 'Voltage (V)'
        self.Lazo = 'Lazo abierto'
        self.torque_celda_01 = 0
        self.torque_celda_02 = 0
        self.fecha_prueba = ''
        self.fecha_hora_inicio = ''
        self.fecha_hora_finalizacion = ''
        self.dataforDataFrame = np.array([[0, 0, 0, 0, 0, 0, 0]])
        self.potencia_acumulada=0
        self.Tasa_Muestreo=4
        self.muestreo_time=0.0
        self.ygraph=0.0
        self.startCalibration=False
        self.counter_muestra=0
        
        self.SendVoltage = SendVoltage()
        self.ReadVoltage = ReadVoltage(self.MinimaFrecuencia)
        self.Do_every = Do_every(1/self.Tasa_Muestreo)
        self.pushButton.setEnabled(False)
        self.Aplicar.clicked.connect(lambda: self.DACVoltageDC())
        self.button_parametro.clicked.connect(lambda: self.ParamsInput())
        self.pushButton_2.clicked.connect(lambda: self.startTest())
        self.pushButton.clicked.connect(lambda: self.stopTest())
        self.ReadVoltage.start()
        self.ReadVoltage.VoltageUpdate.connect(self.VoltageSlotUpdate)
        self.ReadVoltage.FrecuencyUpdate.connect(self.FrecuencySlotUpdate)
        #
        self.listWidget.clicked.connect(self.listVelocidad)
        self.listWidget_2.clicked.connect(self.listDistance)
        self.select_item=self.listWidget.currentItem()
        self.select_item_dis=self.listWidget_2.currentItem()
        self.Celda0.toggled.connect(self.onClicked)
        self.Celda1.toggled.connect(self.onClicked)
        self.Celda2.toggled.connect(self.onClicked)
        self.Lazo_abierto.toggled.connect(self.ClickedLazo)
        self.Lazo_cerrado.toggled.connect(self.ClickedLazo)

        n_data=900
        self.xdata = [x for x in list(range(n_data))]
        self.ydata = [x*0 for x in list(range(n_data))]
        self.ydata1 = [x*0 for x in list(range(n_data))]
        self.ydata2 = [x*0 for x in list(range(n_data))]
        self.graphWidget = pg.PlotWidget()
        self.Senales.addWidget(self.graphWidget)
        self.graphWidget.setBackground('w')

        pen = pg.mkPen(color=(255, 0, 0), width=5)
        self.graphWidget.setTitle("Señal medida de velocidad", color="black", size="20pt")
        self.data_line =  self.graphWidget.plot(self.xdata, self.ydata, pen=pen)# added
        styles = {'color':'black', 'font-size':'15px'}
        self.graphWidget.setLabel('left', 'Velocidad (km/h)', **styles)
        self.graphWidget.setLabel('bottom', 'Tiempo (s)', **styles)

        self.graphWidget1 = pg.PlotWidget()
        self.Senales1.addWidget(self.graphWidget1)
        self.graphWidget1.setBackground('w')
        self.graphWidget1.addLegend(labelTextColor='black',labelTextSize='13pt')
        
        pen1 = pg.mkPen(color=(255, 0, 255), width=5)
        self.graphWidget1.setTitle("Señal medida de celdas de carga", color="black", size="20pt")
        self.data_line1 =  self.graphWidget1.plot(self.xdata, self.ydata1, name = "Celda de carga 1", pen=pen)# added
        self.data_line2 =  self.graphWidget1.plot(self.xdata, self.ydata2, name = "Celda de carga 2",pen=pen1)# added
        self.graphWidget1.setLabel('left', 'Torque (N-m)', **styles)
        self.graphWidget1.setLabel('bottom', 'Tiempo (s)', **styles)
        #Add legend
        self.msg = QMessageBox()
        self.msg.setWindowTitle("Calibración de celdas de carga")
        self.FS = self.sistema_mamdani()
        #self.graphWidget.showGrid(x=True, y=True)
        

    def ParamsInput(self):
        self.pulsos_vuelta=float(self.Pulsos_value.text())
        self.diametro_rodillo=float(self.DiametroTambor_value.text())
        self.sensibilidad_celdas=float(self.SencibilidadCelda_value.text())/100
        self.MinimaFrecuencia=(0.05*self.pulsos_vuelta)/(self.diametro_rodillo*math.pi)
        self.ReadVoltage.stop()
        self.ReadVoltage = ReadVoltage(self.MinimaFrecuencia)
        self.ReadVoltage.start()
        #self.ReadFrecuency.start()
        self.ReadVoltage.VoltageUpdate.connect(self.VoltageSlotUpdate)
        self.ReadVoltage.FrecuencyUpdate.connect(self.FrecuencySlotUpdate)
        print("Parametros actualizados")

    def DACVoltageDC(self):
        if self.Lazo=='Lazo abierto':
            self.value=float(self.InputVoltage.text())
            self.SendVoltage.main_sendVoltage(self.value)
        elif self.Lazo=='Lazo cerrado':
            self.value=float(self.InputVoltage.text())

    def listVelocidad(self):
        self.select_item=self.listWidget.currentItem()

    def listDistance(self):
        self.select_item_dis=self.listWidget_2.currentItem()
    
    def onClicked(self):
        radioBtn = self.sender()
        if radioBtn.isChecked():
            self.VTorque=radioBtn.text()
    
    def ClickedLazo(self):
        radioBtn = self.sender()
        if radioBtn.isChecked():
            self.Lazo=radioBtn.text()
        if self.Lazo=='Lazo abierto':
            self.OutputText.setTitle("Salida de voltaje análogo en lazo abierto (V)")
        elif self.Lazo=='Lazo cerrado':
            self.OutputText.setTitle("Torque de referencia en lazo cerrado (N-m)")
    
    def startTest(self):
        self.start=time.time()
        self.Tasa_Muestreo = float(self.Frecuencia_value.text())
        self.fecha_prueba = datetime.now().strftime("%d/%m/%Y")
        self.fecha_prueba = self.fecha_prueba.replace('/', '_').replace(' ', '-')
        self.fecha_hora_inicio = datetime.now().strftime("%H/%M/%S")
        self.fecha_hora_inicio = self.fecha_hora_inicio.replace('/', '_').replace(' ', '-')
        self.pushButton_2.setEnabled(False)
        self.button_parametro.setEnabled(False)
        self.Aplicar.setEnabled(False)
        self.pushButton.setEnabled(True)
        self.potencia_acumulada = 0.0
        self.cuentas_distancia = 0
        self.startCalibration = True
        self.offsetCelda1 = 0.0
        self.offsetCelda2 = 0.0
        self.counter_muestra = 0        
        self.msg.setText('Calibrando offset celdas de carga espere hasta completar 500 muestras.')
        self.msg.exec_()
        if self.Do_every.isFinished:
            self.Do_every = Do_every(1/self.Tasa_Muestreo)
            self.Do_every.start()
            self.Do_every.Muestreo_Time.connect(self.Time_MuestreoSlotUpdate)
            
    
    def stopTest(self):
        config.startTest_activacte = False
        self.fecha_hora_finalizacion = datetime.now().strftime("%H/%M/%S")
        self.fecha_hora_finalizacion = self.fecha_hora_finalizacion.replace('/', '_').replace(' ', '-')
        Observaciones=str(self.plainTextEdit.toPlainText())
        dataframe_header = pd.DataFrame([['Fecha',self.fecha_prueba],['Hora de inicio',self.fecha_hora_inicio],
                                        ['Hora de finalización',self.fecha_hora_finalizacion],
                                        ['Voltage de salida analoga',self.value],
                                        ['Voltaje offset celda 1', self.offsetCelda1],
                                        ['Voltaje offset celda 2', self.offsetCelda2],
                                        ['Observaciones'+Observaciones]])
        dataframe_datos = pd.DataFrame(self.dataforDataFrame,
                columns=['Muestreo (s)','Cuentas de vueltas','Voltaje celda #1 (V)', 'Voltaje celda #2 (V)',
                         'Velocidad medida (m/s)','Voltaje PAU (V)', 'Voltaje de excitacion (V)'])
        dataframe = pd.concat([dataframe_header, dataframe_datos], ignore_index=True)
        dataframe.to_csv('/home/usuario/PVE_Repo/Pruebas/'+self.fecha_prueba+'_'+self.fecha_hora_inicio+'.csv', index=False)
        self.dataforDataFrame=np.array([[0, 0, 0, 0, 0, 0, 0]])
        self.muestreo=0
        self.pushButton_2.setEnabled(True)
        self.button_parametro.setEnabled(True)
        self.Aplicar.setEnabled(True)
        self.pushButton.setEnabled(False)
        self.Do_every.stop()
        
    def VoltageSlotUpdate(self, Voltage):
        if self.counter_muestra > 500:
            Voltage[0]=Voltage[0]-self.offsetCelda1
            Voltage[2]=Voltage[2]-self.offsetCelda2
        masa_celda_01 = (Voltage[0]*self.capacidad_celdas)/(self.Factor_Amplificacion*self.sensibilidad_celdas*self.factor_libras_kilos*Voltage[3])
        masa_celda_02 = (Voltage[2]*self.capacidad_celdas)/(self.Factor_Amplificacion*self.sensibilidad_celdas*self.factor_libras_kilos*Voltage[3])
        self.torque_celda_01 = masa_celda_01*self.factor_kilos_newton*((self.diametro_rodillo)/2)
        self.torque_celda_02 = masa_celda_02*self.factor_kilos_newton*((self.diametro_rodillo)/2)
        self.Voltage = Voltage
        if(self.VTorque=='Voltage (V)'):
            self.Chan1.setText('{:.5f}'.format(Voltage[0]/self.Factor_Amplificacion)+' V')
            self.Chan2.setText('{:.5f}'.format(Voltage[2]/self.Factor_Amplificacion)+' V')
        
        if(self.VTorque=='Torque (N-m)'):
            self.Chan1.setText('{:.5f}'.format(self.torque_celda_01)+' N-m')
            self.Chan2.setText('{:.5f}'.format(self.torque_celda_02)+' N-m')

        if(self.VTorque=='Peso (kg)'):
            self.Chan1.setText('{:.5f}'.format(masa_celda_01)+' kg')
            self.Chan2.setText('{:.5f}'.format(masa_celda_02)+' kg')

        self.Chan3.setText('{:.5f}'.format(((Voltage[1]*self.divisor_Voltaje)-self.offset_pau)*self.Facto_Atenuacion)+' V')
        self.Chan4.setText('{:.5f}'.format(Voltage[3]*self.divisor_Voltaje)+' V')
        if self.startCalibration:
            self.offsetCelda1 += Voltage[0]
            self.offsetCelda2 += Voltage[2]
            self.counter_muestra += 1
            if self.counter_muestra > 500:
                self.offsetCelda1=self.offsetCelda1/self.counter_muestra
                self.offsetCelda2=self.offsetCelda2/self.counter_muestra
                config.startTest_activacte = True
                self.startCalibration = False
                self.msg.setText('Calibración del offset terminado.\nOffset Celda 1='+str(self.offsetCelda1)
              +'\nOffset Celda 2='+str(self.offsetCelda2))
                self.msg.exec_()
 
    def FrecuencySlotUpdate(self, datos_frecuencia):
        frecuencia=datos_frecuencia[0]
        self.cuentas_distancia=datos_frecuencia[1]
        distancia=datos_frecuencia[1]*(self.diametro_rodillo*math.pi)
        self.Frecuency.setText('{:.2f}'.format(frecuencia)+' Hz')
        revoluciones = (frecuencia/self.pulsos_vuelta)
        velocidad = revoluciones*((self.diametro_rodillo*math.pi))
        if not self.select_item:
            velocidad = 0
            unidad =''
        elif str(self.select_item.text())=='km/h':
            velocidad = velocidad*3.6
            unidad=str(self.select_item.text())
        elif str(self.select_item.text())=='km/s':
            velocidad = velocidad/1000
            unidad=str(self.select_item.text())
        elif str(self.select_item.text())=='m/s':
            velocidad = velocidad
            unidad=str(self.select_item.text())
        elif str(self.select_item.text())=='rev/s':
            velocidad = revoluciones
            unidad=str(self.select_item.text())
        elif str(self.select_item.text())=='rpm':
            velocidad = revoluciones*60
            unidad=str(self.select_item.text())
        elif str(self.select_item.text())=='pulsos/min':
            velocidad = frecuencia*60
            unidad=str(self.select_item.text())
        self.Velocida_value.setText('{:.5f}'.format(velocidad)+' '+unidad)

        if not self.select_item_dis:
            unidad_distancia =''
        elif str(self.select_item_dis.text())=='m':
            distancia = (datos_frecuencia[1]/self.pulsos_vuelta)*(self.diametro_rodillo*math.pi)
            unidad_distancia=str(self.select_item_dis.text())
        elif str(self.select_item_dis.text())=='km':
            distancia=((datos_frecuencia[1]/self.pulsos_vuelta)*(self.diametro_rodillo*math.pi))/1000
            unidad_distancia=str(self.select_item_dis.text())
        elif str(self.select_item_dis.text())=='rev':
            distancia=datos_frecuencia[1]/self.pulsos_vuelta
            unidad_distancia=str(self.select_item_dis.text())
        self.Distancia_value.setText('{:.5f}'.format(distancia)+ ' '+unidad_distancia)
        velocidad = revoluciones*((self.diametro_rodillo*math.pi))
        fuerza = (self.torque_celda_01+self.torque_celda_02)/((self.diametro_rodillo)/2)
        potencia = fuerza*velocidad
        
        self.Fuerza_value.setText('{:.5f}'.format(fuerza)+' N')
        self.Potencia_value.setText('{:.5f}'.format(potencia)+' N '+'m/s')
        
        
        if(config.startTest_activacte==True):
            if config.f:
                if self.Lazo=='Lazo cerrado':
                    
                    torque_actual = self.torque_celda_01 + self.torque_celda_02
                    error_torque = torque_actual - self.value
                    cambio_error_torque = error_torque - self.error_torque_anterior
                    
                    self.FS.set_variable("T", torque_actual)
                    self.FS.set_variable("ET", error_torque)
                    self.FS.set_variable("CET", cambio_error_torque)
                    self.FS.set_variable("RPM", revoluciones*60)
                    
                    #start=time.time()
                    voltaje_control_difuso = self.FS.Mamdani_inference(["V"], ignore_warnings = True)
                    #print(time.time()-start)
                    if voltaje_control_difuso['V'] > 0:
                        self.SendVoltage.main_sendVoltage(voltaje_control_difuso['V'])
                    self.error_torque_anterior = error_torque
                    
                    
                velocidad = revoluciones*((self.diametro_rodillo*math.pi))
                self.PotenciaAcu_value.setText('{:.5f}'.format(self.potencia_acumulada)+' N '+'m/s')
                self.potencia_acumulada += potencia
                self.muestreo += self.muestreo_time
                self.dataforDataFrame = np.concatenate((self.dataforDataFrame, np.array([[self.muestreo, self.cuentas_distancia ,self.Voltage[0]/self.Factor_Amplificacion, self.Voltage[2]/self.Factor_Amplificacion, velocidad, 
                    (self.Voltage[1]-self.offset_pau)*(self.divisor_Voltaje*self.Facto_Atenuacion), self.Voltage[3]*self.divisor_Voltaje]])), axis=0)
                self.ygraph=velocidad*3.6
                config.f=False
                    
                #self.Save=False
        
    def Time_MuestreoSlotUpdate(self, MuestreoTime):
        self.muestreo_time=MuestreoTime
        if config.f:
            self.ydata = self.ydata[1:] + [self.ygraph]  # Remove the first
            self.data_line.setData(self.xdata, self.ydata)  # Update the data.
            self.ydata1 = self.ydata1[1:] + [self.torque_celda_01]  # Remove the first
            self.data_line1.setData(self.xdata, self.ydata1)  # Update the data.
            self.ydata2 = self.ydata2[1:] + [self.torque_celda_02]  # Remove the first
            self.data_line2.setData(self.xdata, self.ydata2)  # Update the data.
            #print(sys.getsizeof(self.ydata))

    def sistema_mamdani(self):
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
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
