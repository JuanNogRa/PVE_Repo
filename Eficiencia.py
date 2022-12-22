from gui_driver_eficiencia import *
from ThreadGINS import *
from PDFTemplate import *
import pyqtgraph as pg
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import *
import pandas as pd
from math import sqrt
from datetime import datetime
import numpy as np
from scipy import integrate
from scipy.signal import savgol_filter

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    Velocidad_actual=0.0                #Variable para graficar la magnitud de velocidad GINS200
    Velocidad_perfil=0.0                #Variable para graficar la magnitud de velocidad del perfil de velocidad
    Velocidad_perfil_actual=0           #Variable para graficar la magnitud de velocidad del perfil de velocidad instanea para comparar y determinar (acelerar, desacelerar, mantener)
    i=0                                 #Variable de control para graficar la velocidad tanto del perfil de condución como de la magnitud del GINS200
    numeral_velocidad=0                 #Variable de control para prueba de coast-down para velocidades especificas.
    Value_hold=0                        #Variable para llevar la cuenta de tiempo para el retenedor de velocidad.
    Time_hold_value=0.250                   #Variable para guardar el tiempo del retenedor que el usuario digita para la prueba de consumo
    velocidad_max=30                    #Variable para guardar la velocidad maxima a la cual se va a realizar la prueba de consumo
    Time_hold_rango_value=0.250           #Variable para guardar el tiempo del retenedor que el usuario digita para la prueba de rango
    velocidad_max_rango=30              #Variable para guardar la velocidad maxima a la cual se va a realizar la prueba de rango
    velocidad_max_coast=40              #Variable para guardar la velocidad maxima a la cual se va a realizar la prueba de coast-down
    Continuar_potencia=False            #Variable de control para validar que el usuario accepto que se carge en memoria el archivo .csv de potencia
    Continuar_consumo=False             #Variable de control para validar que el usuario accepto que se carge en memoria el archivo .csv del archivo obtenido para el calculo del consumo energetico.
    Continuar_rango=False               #Variable de control para validar que el usuario accepto que se carge en memoria el archivo .csv del archivo obtenido para el calculo del rango.
    start_time=0
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        n_data=20
        self.path=''                            #Declaración de la variable donde se guardar la dirección del archivo .csv donde esta el perfil de velocidad
        self.path_rango=''
        self.thread={}
        """Declaración de las listas para graficar las velocidades siendo n_data=400 para visualizar en pantalla 400 datos"""
        self.xdata = [x for x in list(range(n_data))]
        self.ydata = [x*0 for x in list(range(n_data))]
        self.ydata1 = [x*0 for x in list(range(n_data))]
        """Se declara el numpy en el cual se guardaran los valores de velocidad"""
        self.data_gins = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
        """Se declaran las variables necesarias para graficar las señales con PyQtGraph:
        -Se conecta el Widget Senales (añadido en Qt Designer) con el objeto PyQtGraph graphWidget1
        -Se añade legendas para diferenciar el par de graficas.
        -Se añade titulo para el tipo de prueba.
        -Se dejan establecidos las lineas con la grafica de tal manera que cuando se actualicen los valores la linea también."""
        self.graphWidget1 = pg.PlotWidget()
        self.Senales.addWidget(self.graphWidget1)
        self.pos_indicador = pg.TextItem(text="", color=(0,0,0))
        #self.pos_indicador.hide()
        self.pos_indicador.setZValue(2)
        self.pos_indicador.setFont(QFont('Arial', 20))
        self.graphWidget1.addItem(self.pos_indicador)
        self.pos_indicador.setPos(15,5)
        self.graphWidget1.setBackground('w')
        self.graphWidget1.addLegend(labelTextColor='black',labelTextSize='13pt')
        pen = pg.mkPen(color=(255, 0, 255), width=5)
        pen1 = pg.mkPen(color=(0, 180, 100), width=5, style=QtCore.Qt.DashLine)
        self.graphWidget1.setTitle("Señal de velocidad para prueba de consumo", color="black", size="20pt")
        self.data_line1 =  self.graphWidget1.plot(self.xdata, self.ydata, name = "Velocidad actual", pen=pen)# added
        self.data_line2 =  self.graphWidget1.plot(self.xdata, self.ydata1, name = "Velocidad objetivo", pen=pen1)# added
        
        """Se declaran las variables necesarias para graficar las señales con PyQtGraph:
        -Se conecta el Widget Senales (añadido en Qt Designer) con el objeto PyQtGraph graphWidget1
        -Se añade legendas para diferenciar el par de graficas.
        -Se añade titulo para el tipo de prueba.
        -Se dejan establecidos las lineas con la grafica de tal manera que cuando se actualicen los valores la linea también."""
        self.graphWidget = pg.PlotWidget()
        self.Senales_3.addWidget(self.graphWidget)
        self.pos_indicador1 = pg.TextItem(text="", color=(0,0,0))
        #self.pos_indicador.hide()
        self.pos_indicador1.setZValue(2)
        self.pos_indicador1.setFont(QFont('Arial', 20))
        self.graphWidget.addItem(self.pos_indicador1)
        self.pos_indicador1.setPos(15,5)
        self.graphWidget.setBackground('w')
        self.graphWidget.addLegend(labelTextColor='black',labelTextSize='13pt')
        pen2 = pg.mkPen(color=(255, 0, 255), width=5)
        pen3 = pg.mkPen(color=(0, 180, 100), width=5, style=QtCore.Qt.DashLine)
        self.graphWidget.setTitle("Señal de velocidad para prueba de rango", color="black", size="20pt")
        self.data_line3 =  self.graphWidget.plot(self.xdata, self.ydata, name = "Velocidad actual", pen=pen2)# added
        self.data_line4 =  self.graphWidget.plot(self.xdata, self.ydata1, name = "Velocidad objetivo", pen=pen3)# added

        """Se declaran las variables necesarias para graficar las señales con PyQtGraph:
        -Se conecta el Widget Senales (añadido en Qt Designer) con el objeto PyQtGraph graphWidget2
        -Se añade legendas para diferenciar el par de graficas.
        -Se añade titulo para el tipo de prueba.
        -Se dejan establecidos las lineas con la grafica de tal manera que cuando se actualicen los valores la linea también."""
        self.graphWidget2 = pg.PlotWidget()
        self.Senales_velocidad_coast.addWidget(self.graphWidget2)
        self.pos_indicador2 = pg.TextItem(text="", color=(0,0,0))
        self.pos_indicador2.setZValue(2)
        self.pos_indicador2.setFont(QFont('Arial', 20))
        self.graphWidget2.addItem(self.pos_indicador2)
        self.pos_indicador2.setPos(15,5)
        self.graphWidget2.setBackground('w')
        self.graphWidget2.addLegend(labelTextColor='black',labelTextSize='13pt')
        pen4 = pg.mkPen(color=(255, 0, 255), width=5)
        pen5 = pg.mkPen(color=(0, 180, 100), width=5, style=QtCore.Qt.DashLine)
        self.graphWidget2.setTitle("Señal de velocidad para prueba de coast-down", color="black", size="20pt")
        self.data_line5 =  self.graphWidget2.plot(self.xdata, self.ydata, name = "Velocidad actual", pen=pen4)# added
        self.data_line6 =  self.graphWidget2.plot(self.xdata, self.ydata1, name = "Velocidad objetivo", pen=pen5)# added

        """Se conectan los botones de la prueba de consumo de la interfaz grafica con las funciones."""
        self.Load_file.clicked.connect(lambda: self.CicloManejoPath())                          #Conexión con el botón para cargar el archivo .csv con el perfil de conducción
        self.Accept.clicked.connect(lambda: self.CicloManejoAccept())                           #Conexión con el botón para guardar en memoria el perfil de conducción en numpy
        self.Accept_tiempo.clicked.connect(lambda: self.CicloTime())                            #Conexión con el botón para guardar en memoria el tiempo del retenedor.
        self.Accept_velocidad.clicked.connect(lambda: self.CicloVelocidad())                    #Conexión con el botón para guardar en memoria la velocidad maxima del ciclo de conducción.

        """Se conectan los botones de la prueba de rango de la interfaz grafica con las funciones."""
        self.Load_file_rango.clicked.connect(lambda: self.CicloManejoPath_rango())              #Conexión con el botón para cargar el archivo .csv con el perfil de conducción
        self.Accept_rango1.clicked.connect(lambda: self.CicloManejoAccept_rango())              #Conexión con el botón para guardar en memoria el perfil de conducción en numpy
        self.Accept_tiempo_rango.clicked.connect(lambda: self.CicloTime_rango())                #Conexión con el botón para guardar en memoria el tiempo del retenedor.
        self.Accept_velocidad_rango.clicked.connect(lambda: self.CicloVelocidad_rango())        #Conexión con el botón para guardar en memoria la velocidad maxima del ciclo de conducción.
        self.Accept_velocidad_coast.clicked.connect(lambda: self.Velocidad_coast())

        """Se conectan los botones para abrir la ventana de navegación para obtener el path el calculo de la eficiencia."""
        self.Load_power.clicked.connect(lambda: self.Potencia_path())                           #Conexión con el botón para cargar el archivo .csv con los datos para el cálculo de la potencia electrica
        self.Load_consumo.clicked.connect(lambda: self.Consumo_path())                          #Conexión con el botón para cargar el archivo .csv con los datos para el cálculo del consumo
        self.Load_rango.clicked.connect(lambda: self.Rango_path())                              #Conexión con el botón para cargar el archivo .csv con los datos para el cálculo del rango

        """Se conectan los botones para guardar en memoria los valores de las pruebas para el calculo de la eficiencia."""
        self.Accept_power.clicked.connect(lambda: self.Power_Accept())                           #Conexión con el botón para cargar el archivo .csv con los datos para el cálculo de la potencia electrica
        self.Accept_consumo.clicked.connect(lambda: self.Consumo_Accept())                       #Conexión con el botón para cargar el archivo .csv con los datos para el cálculo del consumo
        self.Accept_rango.clicked.connect(lambda: self.Rango_Accept())                           #Conexión con el botón para cargar el archivo .csv con los datos para el cálculo del rango
        
        """Se conectan los botones de empezar y detenerse con el programa principal"""
        self.Start.clicked.connect(lambda: self.EmpezarCiclo())                                 
        self.Start_rango.clicked.connect(lambda: self.EmpezarCicloRango())
        self.Start_coast.clicked.connect(lambda: self.EmpezarCoastDown())    
        self.Stop.clicked.connect(lambda: self.DetenerCiclo_rango())
        self.Calcular_eficiencia.clicked.connect(lambda: self.Calcular_eficiencia_function())
        self.Reporte_generado.clicked.connect(lambda: self.Generar_reporte())

        """Se desactivan los botones hasta que se cumplan con las condiciones"""
        self.Start.setEnabled(False)
        self.Start_rango.setEnabled(False)
        self.Start_coast.setEnabled(False)
        self.Stop.setEnabled(False)
        self.Calcular_eficiencia.setEnabled(False)
        self.Reporte_generado.setEnabled(False)

        """Se declaran las variables que se obtienen del sensor GINS 200"""
        self.gins_data = {}
        self.gins_data["gyro_x"] = 0
        self.gins_data["gyro_y"] = 0
        self.gins_data["gyro_z"] = 0
        self.gins_data["acc_x"] = 0
        self.gins_data["acc_y"] = 0
        self.gins_data["acc_z"] = 0
        self.gins_data["magn_x"] = 0
        self.gins_data["magn_y"] = 0
        self.gins_data["magn_z"] = 0
        self.gins_data["h_bar"] = 0
        self.gins_data["gps_vel_E"] = 0
        self.gins_data["gps_vel_N"] = 0
        self.gins_data["gps_vel_U"] = 0
        self.gins_data["gps_Lon"] = 0
        self.gins_data["gps_Lat"] = 0
        self.gins_data["gps_alt"] = 0
        self.gins_data["gps_yaw"] = 0
        self.gins_data["nav_pitch"] = 0
        self.gins_data["nav_roll"] = 0
        self.gins_data["nav_yaw"] = 0
        self.gins_data["nav_vel_E"] = 0
        self.gins_data["nav_vel_N"] = 0
        self.gins_data["nav_vel_U"] = 0
        self.gins_data["nav_Lon"] = 0
        self.gins_data["nav_Lat"] = 0
        self.gins_data["nav_alt"] = 0
        self.gins_data["Temp"] = 0

        """Se declara una ventana para informar al usuario de las condiciones del programa."""
        self.msg = QMessageBox()
        self.msg.setWindowTitle("Panel de información")

    """Metodo que permite graficar el perfil de velocidad y la velocidad longitudinal del GINS200 para la prueba de consumo.
    También se muestra graficamente el nivel de velocidad y si hay que acelerar, desacelerar o mantener la velocidad."""
    def update_plot(self):
        if self.i<len(self.Velocidad_perfil)-1:
            #self.i+=1
            if self.Value_hold>=self.Time_hold_value:
                self.i+=1
                self.Value_hold=0
        else:
            self.i=0
            self.thread[1].stop()
            self.Start.setEnabled(True)
            self.DetenerCiclo()

        self.Velocidad_perfil_actual=self.Velocidad_perfil[self.i,1]
        self.ydata = self.ydata[1:] + [self.Velocidad_actual]  # Remove the first
        self.ydata1 = self.ydata1[1:] + [self.Velocidad_perfil_actual]  # Remove the first
        self.data_line1.setData(self.xdata, self.ydata)  # Update the data.
        self.data_line2.setData(self.xdata, self.ydata1)  # Update the data.
        self.data_gins=np.concatenate((self.data_gins, np.array([[self.gins_data["nav_vel_E"], self.gins_data["nav_vel_N"], self.gins_data["nav_vel_U"],
                        self.gins_data["acc_x"], self.gins_data["acc_y"], self.gins_data["acc_z"],
                        self.gins_data["nav_pitch"], self.gins_data["nav_roll"], self.gins_data["nav_yaw"],
                        self.gins_data["nav_Lon"], self.gins_data["nav_Lat"], self.gins_data["nav_alt"]]])), axis=0)

        self.Measure_Gauge.setValue(int(self.Velocidad_actual))
        if(self.Velocidad_actual-self.Velocidad_perfil_actual<-5):
            #self.Indicaciones.setStyleSheet("color: green")
            self.pos_indicador.setColor((0,128,0))
            self.pos_indicador.setText('Acelere hasta '+str(int(self.Velocidad_perfil_actual))+' km/h')
            self.Measure_Gauge.setStyleSheet(
                """QProgressBar {
                    border: 2px solid rgba(33, 37, 43, 180);
                    border-radius: 5px;
                    text-align: center;
                    font: 75 14pt "MS Shell Dlg 2";
                    background-color:transparent;
                    color: black;
                    width: 80;
                    }"""
                "QProgressBar::chunk "
                          "{"
                          "background-color: green;"
                          "}")
            #self.Indicaciones.setText("Acelere")
        elif(self.Velocidad_actual-self.Velocidad_perfil_actual>5):
            #self.Indicaciones.setStyleSheet("color: red")
            self.pos_indicador.setColor((136, 8, 8))
            self.pos_indicador.setText('Desacelere hasta '+str(int(self.Velocidad_perfil_actual))+' km/h')
            self.Measure_Gauge.setStyleSheet(
                """QProgressBar {
                    border: 2px solid rgba(33, 37, 43, 180);
                    border-radius: 5px;
                    text-align: center;
                    font: 75 14pt "MS Shell Dlg 2";
                    background-color:transparent;
                    color: black;
                    width: 80;
                    }"""
                "QProgressBar::chunk "
                          "{"
                          "background-color: red;"
                          "}")
            #self.Indicaciones.setText("Desacelere")
        elif(self.Velocidad_actual-self.Velocidad_perfil_actual>-5 and self.Velocidad_actual-self.Velocidad_perfil_actual<5):
            #self.Indicaciones.setStyleSheet("color: yellow")
            self.pos_indicador.setColor((255,255,0))
            self.pos_indicador.setText('Mantener en '+str(int(self.Velocidad_perfil_actual))+' km/h')
            self.Measure_Gauge.setStyleSheet(
                """QProgressBar {
                    border: 2px solid rgba(33, 37, 43, 180);
                    border-radius: 5px;
                    text-align: center;
                    font: 75 14pt "MS Shell Dlg 2";
                    background-color:transparent;
                    color: black;
                    width: 80;
                    }"""
                "QProgressBar::chunk "
                          "{"
                          "background-color: yellow;"
                          "}")
            #self.Indicaciones.setText("Mantener")
    """Metodo que permite graficar el perfil de velocidad y la velocidad longitudinal del GINS200 para la prueba de rango.
    También se muestra graficamente el nivel de velocidad y si hay que acelerar, desacelerar o mantener la velocidad."""
    def update_plot_1(self):
        if self.i<len(self.Velocidad_perfil)-1:
            #self.i+=1
            if self.Value_hold>=self.Time_hold_rango_value:
                self.i+=1
                self.Value_hold=0
        else:
            self.i=0

        self.Velocidad_perfil_actual=self.Velocidad_perfil[self.i,1]
        self.ydata = self.ydata[1:] + [self.Velocidad_actual]  # Remove the first
        self.ydata1 = self.ydata1[1:] + [self.Velocidad_perfil_actual]  # Remove the first
        self.data_line3.setData(self.xdata, self.ydata)  # Update the data.
        self.data_line4.setData(self.xdata, self.ydata1)  # Update the data.
        self.data_gins=np.concatenate((self.data_gins, np.array([[self.gins_data["nav_vel_E"], self.gins_data["nav_vel_N"], self.gins_data["nav_vel_U"],
                        self.gins_data["acc_x"], self.gins_data["acc_y"], self.gins_data["acc_z"],
                        self.gins_data["gyro_x"], self.gins_data["gyro_x"], self.gins_data["gyro_x"],
                        self.gins_data["nav_Lon"], self.gins_data["nav_Lat"], self.gins_data["nav_alt"]]])), axis=0)
        
        self.Measure_Gauge_3.setValue(int(self.Velocidad_actual))
        if(self.Velocidad_actual-self.Velocidad_perfil_actual<-5):
            #self.Indicaciones.setStyleSheet("color: green")
            self.pos_indicador1.setColor((0,128,0))
            self.pos_indicador1.setText('Acelere hasta '+str(int(self.Velocidad_perfil_actual))+' km/h')
            self.Measure_Gauge_3.setStyleSheet(
                """QProgressBar {
                    border: 2px solid rgba(33, 37, 43, 180);
                    border-radius: 5px;
                    text-align: center;
                    font: 75 14pt "MS Shell Dlg 2";
                    background-color:transparent;
                    color: black;
                    width: 80;
                    }"""
                "QProgressBar::chunk "
                          "{"
                          "background-color: green;"
                          "}")
            #self.Indicaciones.setText("Acelere")
        elif(self.Velocidad_actual-self.Velocidad_perfil_actual>5):
            #self.Indicaciones.setStyleSheet("color: red")
            self.pos_indicador1.setColor((136, 8, 8))
            self.pos_indicador1.setText('Desacelere hasta '+str(int(self.Velocidad_perfil_actual))+' km/h')
            self.Measure_Gauge_3.setStyleSheet(
                """QProgressBar {
                    border: 2px solid rgba(33, 37, 43, 180);
                    border-radius: 5px;
                    text-align: center;
                    font: 75 14pt "MS Shell Dlg 2";
                    background-color:transparent;
                    color: black;
                    width: 80;
                    }"""
                "QProgressBar::chunk "
                          "{"
                          "background-color: red;"
                          "}")
            #self.Indicaciones.setText("Desacelere")
        elif(self.Velocidad_actual-self.Velocidad_perfil_actual>-5 and self.Velocidad_actual-self.Velocidad_perfil_actual<5):
            #self.Indicaciones.setStyleSheet("color: yellow")
            self.pos_indicador1.setColor((255,255,0))
            self.pos_indicador1.setText('Mantener en '+str(int(self.Velocidad_perfil_actual))+' km/h')
            self.Measure_Gauge_3.setStyleSheet(
                """QProgressBar {
                    border: 2px solid rgba(33, 37, 43, 180);
                    border-radius: 5px;
                    text-align: center;
                    font: 75 14pt "MS Shell Dlg 2";
                    background-color:transparent;
                    color: black;
                    width: 80;
                    }"""
                "QProgressBar::chunk "
                          "{"
                          "background-color: yellow;"
                          "}")
            #self.Indicaciones.setText("Mantener")
    
    """Metodo que permite graficar el perfil de velocidad y la velocidad longitudinal del GINS200 para la prueba de rango.
    También se muestra graficamente el nivel de velocidad y si hay que acelerar, desacelerar o mantener la velocidad."""
    def update_plot_coastdown(self):
        self.Velocidad_perfil_actual = self.vel_especificas[self.numeral_velocidad]
        self.ydata = self.ydata[1:] + [self.Velocidad_actual]  # Remove the first
        self.ydata1 = self.ydata1[1:] + [self.Velocidad_perfil_actual]  # Remove the first
        self.data_line5.setData(self.xdata, self.ydata)  # Update the data.
        self.data_line6.setData(self.xdata, self.ydata1)  # Update the data.
        
        self.Measure_Gauge_velocidad.setValue(int(self.Velocidad_actual))
        if self.State_coastdown==0:
            if self.Velocidad_actual>=5:
                if(self.Velocidad_actual-self.Velocidad_perfil_actual-10<-3):    
                    self.pos_indicador2.setColor((0,128,0))
                    self.pos_indicador2.setText('Acelere hasta '+str(self.Velocidad_perfil_actual+10)+' km/h')
                    self.Measure_Gauge_velocidad.setStyleSheet(
                        """QProgressBar {
                            border: 2px solid rgba(33, 37, 43, 180);
                            border-radius: 5px;
                            text-align: center;
                            font: 75 14pt "MS Shell Dlg 2";
                            background-color:transparent;
                            color: black;
                            width: 80;
                            }"""
                        "QProgressBar::chunk "
                                "{"
                                "background-color: green;"
                                "}")
                elif(self.Velocidad_actual-self.Velocidad_perfil_actual-10>3):
                    self.pos_indicador2.setColor((136, 8, 8))
                    self.pos_indicador2.setText('Desacelere hasta '+str(self.Velocidad_perfil_actual+10)+' km/h')
                    self.Measure_Gauge_velocidad.setStyleSheet(
                        """QProgressBar {
                            border: 2px solid rgba(33, 37, 43, 180);
                            border-radius: 5px;
                            text-align: center;
                            font: 75 14pt "MS Shell Dlg 2";
                            background-color:transparent;
                            color: black;
                            width: 80;
                            }"""
                        "QProgressBar::chunk "
                                    "{"
                                    "background-color: red;"
                                    "}")
                else:
                    self.State_coastdown=1                  

        elif self.State_coastdown==1:
            if(self.Velocidad_actual-self.Velocidad_perfil_actual-10>-2 and self.Velocidad_actual-self.Velocidad_perfil_actual-10<2):
                if self.Time_coastdown.isRunning()==False:
                    self.Time_coastdown.start()

                self.pos_indicador2.setColor((255,255,0))
                self.pos_indicador2.setText('Mantener la velocidad '+ str(self.Velocidad_perfil_actual+10)+' km/h durante 5s')
                self.Measure_Gauge_velocidad.setStyleSheet(
                    """QProgressBar {
                        border: 2px solid rgba(33, 37, 43, 180);
                        border-radius: 5px;
                        text-align: center;
                        font: 75 14pt "MS Shell Dlg 2";
                        background-color:transparent;
                        color: black;
                        width: 80;
                        }"""
                    "QProgressBar::chunk "
                            "{"
                            "background-color: yellow;"
                            "}")
                #print(self.Value_hold)
                if self.Value_hold>=5:
                    self.State_coastdown=2
                    start = time.time()
            else:
                self.Value_hold=0                                
                self.State_coastdown=0
                self.Time_coastdown.stop()
                self.Time_coastdown = Do_every(5.0)
                self.Time_coastdown.Muestreo_Time.connect(self.Hold_sample)

        elif self.State_coastdown==2:
            if(self.Velocidad_actual-self.Velocidad_perfil_actual>5):
                
                self.pos_indicador2.setColor((136, 8, 8))
                self.pos_indicador2.setText('Suelte el acelerador y\nponga el vehículo en neutro.')
                self.Measure_Gauge_velocidad.setStyleSheet(
                    """QProgressBar {
                        border: 2px solid rgba(33, 37, 43, 180);
                        border-radius: 5px;
                        text-align: center;
                        font: 75 14pt "MS Shell Dlg 2";
                        background-color:transparent;
                        color: black;
                        width: 80;
                        }"""
                    "QProgressBar::chunk "
                                "{"
                                "background-color: red;"
                                "}")
            elif(self.Velocidad_actual-self.Velocidad_perfil_actual>-5 and self.Velocidad_actual-self.Velocidad_perfil_actual<5):
                self.data_gins=np.concatenate((self.data_gins, np.array([[self.vuelta,self.gins_data["nav_vel_E"], self.gins_data["nav_vel_N"], self.gins_data["nav_vel_U"],
                        self.gins_data["acc_x"], self.gins_data["acc_y"], self.gins_data["acc_z"],
                        self.gins_data["gyro_x"], self.gins_data["gyro_x"], self.gins_data["gyro_x"],
                        self.gins_data["nav_Lon"], self.gins_data["nav_Lat"], self.gins_data["nav_alt"]]])), axis=0)
                self.data_gins_temporal=np.concatenate((self.data_gins_temporal, np.array([[self.gins_data["nav_vel_E"], self.gins_data["nav_vel_N"], self.gins_data["nav_vel_U"],
                        self.gins_data["acc_x"], self.gins_data["acc_y"], self.gins_data["acc_z"]]])), axis=0)
            else:
                if self.vuelta==False:
                    time_ida = time.time()-start
                else:
                    time_vuelta = time.time()-start
                self.State_coastdown=3

        elif self.State_coastdown==3:
            if self.vuelta==False:
                velocidad = 3.6*np.sqrt((self.data_gins_temporal['Velocidad E (m/s)'])**2.0 + (self.data_gins_temporal['Velocidad N (m/s)'])**2.0 + (self.data_gins_temporal['Velocidad U (m/s)'])**2.0)         #Calculo de la velocidad longitudinal en km/s a partir de las velocidades en el eje global North, East y Up. (Prueba de consumo)
                #Aplicar filtro de suavizado a señal de aceleración
                ay_sm = savgol_filter(self.data_gins_temporal["acc_y"], 101, 1) # window size 101, polynomial order 1
                #Obtenemos los coeficientes del polinomio de segundo grado que mejor se ajusta a velocidad vs aceleración.
                p = np.polyfit(velocidad, ay_sm, 2)
                self.list_polinomy=np.concatenate(([self.list_polinomy],[p]), axis=0)
                self.vuelta=True
                self.State_coastdown=0
            else:
                velocidad = 3.6*np.sqrt((self.data_gins_temporal['Velocidad E (m/s)'])**2.0 + (self.data_gins_temporal['Velocidad N (m/s)'])**2.0 + (self.data_gins_temporal['Velocidad U (m/s)'])**2.0)         #Calculo de la velocidad longitudinal en km/s a partir de las velocidades en el eje global North, East y Up. (Prueba de consumo)
                #Aplicar filtro de suavizado a señal de aceleración
                ay_sm = savgol_filter(self.data_gins_temporal["acc_y"], 101, 1) # window size 101, polynomial order 1
                #Obtenemos los coeficientes del polinomio de segundo grado que mejor se ajusta a velocidad vs aceleración.
                p = np.polyfit(velocidad, ay_sm, 2)
                self.list_polinomy=np.concatenate(([self.list_polinomy],[p]), axis=0)
                self.vuelta=False
                promedio_tiempo_desacel = (time_ida+time_vuelta)/2
                self.numero_pruebas = self.numero_pruebas + 1
                self.suma_interna_promedio_tiempos += promedio_tiempo_desacel
                self.promedio_tiempos = (self.suma_interna_promedio_tiempos)/self.numero_pruebas
                self.lista_promedio_tiempo_desacel=np.concatenate(([self.lista_promedio_tiempo_desacel],[promedio_tiempo_desacel]), axis=0)

                if self.numero_pruebas>=4:
                    if self.numero_pruebas == 4:
                        coeficiente = 3.2
                    elif self.numero_pruebas == 5:
                        coeficiente = 2.8
                    elif self.numero_pruebas == 6:
                        coeficiente = 2.6
                    elif self.numero_pruebas == 7:
                        coeficiente = 2.5
                    elif self.numero_pruebas == 8:
                        coeficiente = 2.4
                    else:
                        coeficiente = 2.3
                else:
                    self.State_coastdown=0

            self.data_gins_temporal = np.array([[0,0,0,0]])
            polinomy_mean=np.sum(self.list_polinomy[1:,0])/len(self.list_polinomy[1:,0])
            suma_interna_desviacion_estandar = 0
            for j in self.lista_promedio_tiempo_desacel[1:]:
                sumatoria_desviacion_estandar = (j-self.promedio_tiempos)^(2)
                suma_interna_desviacion_estandar += sumatoria_desviacion_estandar
        
            desviacion_estandar = (suma_interna_desviacion_estandar/(self.numero_pruebas-1))^(1/2)
            self.precision_estadistica = ((coeficiente*desviacion_estandar)/((self.numero_pruebas)^(1/2)))*(100/self.promedio_tiempos)
            if self.precision_estadistica>=4:
                self.State_coastdown=0
                self.msg.setText('La precisión estadística es: '+str(self.precision_estadistica)+
                                '. Es necesario seguir calculando los polinomios con el perfil de velocidad de '+str(self.Velocidad_perfil_actual))
                self.msg.exec_()
            else:
                self.State_coastdown=4
                self.msg.setText('La precisión estadística es: '+str(self.precision_estadistica)+
                                '. El polinomio promedio cumple con la precisión deseada y se han guardado en memoria. El promedio de los coeficientes es: '+str(polinomy_mean))
                self.msg.exec_()

        elif self.State_coastdown==4:
            if self.numeral_velocidad==len(self.vel_especificas)-1:
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Prueba de coast-down")
                dlg.setText("¿Se quiere continuar con la siguiente velocidad especifica?")
                dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                dlg.setIcon(QMessageBox.Question)
                button = dlg.exec()

                if button == QMessageBox.Yes:
                    self.numero_pruebas=0
                    self.precision_estadistica=5
                    self.numeral_velocidad+=1
                    self.State_coastdown=0
                else:
                    self.DetenerCoastdown(polinomy_mean)
                    self.timer.stop()
                    self.thread[1].stop()
                    self.Time_coastdown.stop()
                    self.Time_coastdown = Do_every(5.0)
                    self.Time_coastdown.Muestreo_Time.connect(self.Hold_sample)
                    self.msg.setText('La precisión estadística es: '+str(self.precision_estadistica)+
                                '. El polinomio promedio y se ha guardado. El promedio de los coeficientes es: '+str(polinomy_mean))
                    self.msg.exec_()
            else:
                self.msg.setText('Prueba de coast-down termina.')
                self.msg.show()
                self.DetenerCoastdown(polinomy_mean)
                self.timer.stop()
                self.thread[1].stop()
                self.Time_coastdown.stop()
                self.Time_coastdown = Do_every(5.0)
                self.Time_coastdown.Muestreo_Time.connect(self.Hold_sample)

    def Hold_sample(self, time):
        self.Value_hold=time
        #print(self.Value_hold)

    def ActualizarVelocidadActual(self, gins):
        vx = 3.6*sqrt((self.gins_data["nav_vel_E"])**2 + (self.gins_data["nav_vel_N"])**2 + 
				(self.gins_data["nav_vel_U"])**2) #km/h
        self.gins_data=gins
        self.Velocidad_actual=vx
    
    def start_workers(self):
        try:
            serialPort = 'COM4' # Debe revisarse el puerto al que se conecta el GINS
            baudRate = 460800
            self.thread[1] = Gins(serialPort,baudRate,parent=None,index=1)  
            self.thread[1].data.connect(self.ActualizarVelocidadActual)
            self.thread[1].start()
        except:
            print('No se ha podido establecer conexión con el GINS200')

    def CicloManejoPath(self):
        filename = QFileDialog.getOpenFileName()
        self.path=filename[0]
        self.Path.setText(self.path)       
    
    def CicloManejoPath_rango(self):
        filename = QFileDialog.getOpenFileName()
        self.path_rango=filename[0]
        self.Path_rango.setText(self.path_rango)

    def CicloManejoAccept(self): 
        if self.path !='':
            #self.HOST = self.EditIPHost.text()  # Standard loopback interface address (localhost)        
            data = pd.read_csv(self.path)
            styles = {'color':'black', 'font-size':'15px'}
            self.graphWidget1.setLabel('bottom', 'Tiempo (s)', **styles)
            df = data.drop('tiempo', axis=1)
            df_norm = df*self.velocidad_max
            df_norm = pd.concat((data.tiempo, df_norm), axis = 1)
            self.Velocidad_perfil=df_norm.to_numpy()
            #print(len(self.cycle_temp))
            self.data_line2.setData(self.Velocidad_perfil[:,0],  self.Velocidad_perfil[:,1])  # Update the data.
            self.Start.setEnabled(True)
            self.msg.setText('Ciclo de manejo cargado en memoria para prueba de consumo.')
            self.msg.show()
    
    def CicloManejoAccept_rango(self): 
        if self.path_rango !='':
            #self.HOST = self.EditIPHost.text()  # Standard loopback interface address (localhost)        
            data = pd.read_csv(self.path_rango)
            styles = {'color':'black', 'font-size':'15px'}
            self.graphWidget.setLabel('bottom', 'Tiempo (s)', **styles)
            df = data.drop('tiempo', axis=1)
            df_norm = df*self.velocidad_max_rango
            df_norm = pd.concat((data.tiempo, df_norm), axis = 1)
            self.Velocidad_perfil=df_norm.to_numpy()
            #print(len(self.cycle_temp))
            self.data_line4.setData(self.Velocidad_perfil[:,0],  self.Velocidad_perfil[:,1])  # Update the data.
            self.Start_rango.setEnabled(True)
            self.msg.setText('Ciclo de manejo cargado en memoria para prueba de rango.')
            self.msg.show()
    
    def CicloTime(self): 
        if self.Time_hold.text() !='':        
            self.Time_hold_value=float(self.Time_hold.text())
            self.msg.setText('El retenedor de tiempo configurada es de '+str(self.Time_hold_value)+' s.')
            self.msg.show()        

    def CicloVelocidad(self): 
        if self.Velo_max.text() !='':        
            self.velocidad_max=float(self.Velo_max.text())
            self.msg.setText('La velocidad máxima configurada es de '+self.Velo_max.text()+' km/h.')
            self.msg.show()             

    def CicloTime_rango(self): 
        if self.Time_hold_rango.text() !='':        
            self.Time_hold_rango_value=float(self.Time_hold_rango.text())
            self.msg.setText('El retenedor de tiempo configurada es de '+str(self.Time_hold_rango_value)+' s.')
            self.msg.show()             

    def CicloVelocidad_rango(self): 
        if self.Velo_max_rango.text() !='':        
            self.velocidad_max_rango=float(self.Velo_max_rango.text())
            self.msg.setText('La velocidad máxima configurada es de '+self.Velo_max_rango.text()+' m/s.')
            self.msg.show()

    def Velocidad_coast(self): 
        if self.Velo_max_coast.text() !='':        
            self.velocidad_max_coast=int(self.Velo_max_coast.text())
            self.Start_coast.setEnabled(True)
            self.msg.setText('La velocidad máxima configurada es de '+self.Velo_max_coast.text()+' m/s.')
            self.msg.show()
                   
    """Metodo para empezar la prueba de consumo. Se definen las variables para guardar lo capturado en el GINS200. 
    Se definen los metodos que permiten graficar la velocidad del perfil de conducción y la velocidad del gins200.
    Se guarda en memoria la fecha y la hora de inicio de la prueba.
    Se habilita el retenedor de tiempo de la velocidad del perfil de conducción cargado."""
    def EmpezarCiclo(self):
        n_data=20
        self.xdata = [x for x in list(range(n_data))]
        self.ydata = [x*0 for x in list(range(n_data))]
        self.ydata1 = [x*0 for x in list(range(n_data))]
        self.data_gins = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
        self.start_time=time.time()
        self.start_workers()
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()
        self.Start.setEnabled(False)
        self.fecha_prueba = datetime.now().strftime("%d/%m/%Y")
        self.fecha_prueba = self.fecha_prueba.replace('/', '_').replace(' ', '-')
        self.fecha_hora_inicio = datetime.now().strftime("%H/%M/%S")
        self.fecha_hora_inicio = self.fecha_hora_inicio.replace('/', '_').replace(' ', '-')
        self.Hold_sample_period = Do_every(self.Time_hold_value)
        self.Hold_sample_period.Muestreo_Time.connect(self.Hold_sample)
        self.Hold_sample_period.start()
        self.msg.setText('Esta comenzando la prueba de consumo. Presione "Ok" para continuar.')
        self.msg.exec_()  

    """Metodo para empezar la prueba de rango. Se definen las variables para guardar lo capturado en el GINS200. 
    Se definen los metodos que permiten graficar la velocidad del perfil de conducción y la velocidad del gins200.
    Se guarda en memoria la fecha y la hora de inicio de la prueba.
    Se habilita el retenedor de tiempo de la velocidad del perfil de conducción cargado."""
    def EmpezarCicloRango(self):
        n_data=20
        self.xdata = [x for x in list(range(n_data))]
        self.ydata = [x*0 for x in list(range(n_data))]
        self.ydata1 = [x*0 for x in list(range(n_data))]
        self.data_gins = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
        self.start_workers()
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_plot_1)
        self.timer.start()
        self.Start_rango.setEnabled(False)
        self.Stop.setEnabled(True)
        #self.Pause.setEnabled(True)
        
        self.fecha_prueba = datetime.now().strftime("%d/%m/%Y")
        self.fecha_prueba = self.fecha_prueba.replace('/', '_').replace(' ', '-')
        self.fecha_hora_inicio = datetime.now().strftime("%H/%M/%S")
        self.fecha_hora_inicio = self.fecha_hora_inicio.replace('/', '_').replace(' ', '-')
        self.Hold_sample_period = Do_every(self.Time_hold_rango_value)
        self.Hold_sample_period.Muestreo_Time.connect(self.Hold_sample)
        self.Hold_sample_period.start()

        self.msg.setText('Esta comenzando la prueba de rango. Presione "Ok" para continuar.')
        self.msg.exec_()  
    
    """Metodo para empezar la prueba de coastdown. Se definen las variables para guardar lo capturado en el GINS200. 
    Se definen los metodos que permiten graficar la velocidad del gins200."""
    def EmpezarCoastDown(self):
        n_data=20
        self.xdata = [x for x in list(range(n_data))]
        self.ydata = [x*0 for x in list(range(n_data))]
        self.ydata1 = [x*0 for x in list(range(n_data))]
        self.data_gins = np.array([[False, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
        self.data_gins_temporal = np.array([[0,0,0,0]])
        self.list_polinomy=np.array([0,0,0])
        self.vuelta=False
        self.numero_pruebas = 0
        self.suma_interna_promedio_tiempos = 0
        self.promedio_tiempos = 0
        self.lista_promedio_tiempo_desacel = np.array([0])
        self.precision_estadistica = 5
        self.list_polinomy=np.array([0,0,0])
        if self.velocidad_max_coast > 130:
            self.vel_especificas = np.array([100, 80, 60, 40, 20])
        elif self.velocidad_max_coast <= 130 and self.velocidad_max_coast > 100:
            self.vel_especificas = np.array([90, 80, 60, 40, 20])
        elif self.velocidad_max_coast <= 100 and self.velocidad_max_coast > 70:
            self.vel_especificas = np.array([60, 50, 40, 30, 20])
        else:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Prueba de coast-down")
            dlg.setText("¿El vehículo puede alcanzar los 55 km/h?")
            dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            dlg.setIcon(QMessageBox.Question)
            button = dlg.exec()

            if button == QMessageBox.Yes:
                self.vel_especificas = np.array([50, 40, 30, 20])
            else:
                self.vel_especificas = np.array([40, 30, 20, 30])
        
        self.State_coastdown=0
        self.start_workers()
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_plot_coastdown)
        self.timer.start()
        self.Time_coastdown = Do_every(5.0)
        self.Time_coastdown.Muestreo_Time.connect(self.Hold_sample)
        self.msg.setText('Esta comenzando la prueba de coast-down. Presione "Ok" para continuar.')
        self.msg.exec_()

    """Metodo que se ejecuta al acabar la prueba de consumo. Aquí se guarda el archivo .csv con la hora y fecha de inicio de la prueba
    y la hora y fecha de finalización de la prueba. Se almacena la velocidades capturadas con el GINS en el marco global East, North y Up.
    Aceleración en el marco local. Angulo de inclinación. Y la posición en el marco global de longitud, latitud y altitud."""
    def DetenerCiclo(self):
        self.Start.setEnabled(True)
        #self.Pause.setEnabled(False)
        #self.Stop.setEnabled(False)
        self.fecha_hora_finalizacion = datetime.now().strftime("%H/%M/%S")
        self.fecha_hora_finalizacion = self.fecha_hora_finalizacion.replace('/', '_').replace(' ', '-')
        self.timer.stop()
        dataframe_header = pd.DataFrame([['Fecha',self.fecha_prueba],['Hora de inicio',self.fecha_hora_inicio],
                                        ['Hora de finalización',self.fecha_hora_finalizacion]])
                                        
        dataframe_datos = pd.DataFrame(self.data_gins,
                columns=['Velocidad E (m/s)','Velocidad N (m/s)', 'Velocidad U (m/s)',
                         'Aceleración X (g)','Aceleración Y (g)', 'Aceleración Z (g)',
                         'Pitch (°)','Roll Y (°)', 'Yaw (°)',
                         'Posición longitud (deg)','Posición latitud (deg)', 'Posición altitud (m)'])          
        dataframe = pd.concat([dataframe_header, dataframe_datos], ignore_index=True)
        dataframe.to_csv('Eficiencia/Consumo'+self.fecha_prueba+'_'+self.fecha_hora_inicio+'.csv', index=False)
        self.Hold_sample_period.stop()
        self.i=0
        self.msg.setText('Prueba terminada. Se han guardado los datos en el archivo '+'Eficiencia/Consumo'+self.fecha_prueba+'_'+self.fecha_hora_inicio+'.csv')
        self.msg.show()

    """Metodo que se ejecuta al presionar el botón de "Terminar" en la prueba de rango. Aquí se guarda el archivo .csv con la hora y fecha de inicio de la prueba
    y la hora y fecha de finalización de la prueba. Se almacena la velocidades capturadas con el GINS en el marco global East, North y Up.
    Aceleración en el marco local. Angulo de inclinación. Y la posición en el marco global de longitud, latitud y altitud."""
    def DetenerCiclo_rango(self):
        self.Start_rango.setEnabled(True)
        self.fecha_hora_finalizacion = datetime.now().strftime("%H/%M/%S")
        self.fecha_hora_finalizacion = self.fecha_hora_finalizacion.replace('/', '_').replace(' ', '-')
        self.timer.stop()
        dataframe_header = pd.DataFrame([['Fecha',self.fecha_prueba],['Hora de inicio',self.fecha_hora_inicio],
                                        ['Hora de finalización',self.fecha_hora_finalizacion]])
                                        
        dataframe_datos = pd.DataFrame(self.data_gins,
                columns=['Velocidad E (m/s)','Velocidad N (m/s)', 'Velocidad U (m/s)',
                         'Aceleración X (g)','Aceleración Y (g)', 'Aceleración Z (g)',
                         'Pitch (°)','Roll Y (°)', 'Yaw (°)',
                         'Posición longitud (deg)','Posición latitud (deg)', 'Posición altitud (m)'])          
        dataframe = pd.concat([dataframe_header, dataframe_datos], ignore_index=True)
        dataframe.to_csv('Eficiencia/Rango'+self.fecha_prueba+'_'+self.fecha_hora_inicio+'.csv', index=False)
        self.thread[1].stop()
        self.Hold_sample_period.stop()
        self.i=0
        self.msg.setText('Prueba terminada. Se han guardado los datos en el archivo '+'Eficiencia/Rango'+self.fecha_prueba+'_'+self.fecha_hora_inicio+'.csv')
        self.msg.show()
    
    def DetenerCoastdown(self, polinomy_mean):
        self.Start_coast.setEnabled(True)
        self.fecha_hora_finalizacion = datetime.now().strftime("%H/%M/%S")
        self.fecha_hora_finalizacion = self.fecha_hora_finalizacion.replace('/', '_').replace(' ', '-')

        dataframe_header = pd.DataFrame([['Fecha',self.fecha_prueba],['Hora de inicio',self.fecha_hora_inicio],
                                        ['Hora de finalización',self.fecha_hora_finalizacion],['Polinomio promedio prueba coast-down',polinomy_mean]])
                                        
        dataframe_datos = pd.DataFrame(self.data_gins,
                columns=['Vuelta (True/False)','Velocidad E (m/s)','Velocidad N (m/s)', 'Velocidad U (m/s)',
                         'Aceleración X (g)','Aceleración Y (g)', 'Aceleración Z (g)',
                         'Pitch (°)','Roll Y (°)', 'Yaw (°)',
                         'Posición longitud (deg)','Posición latitud (deg)', 'Posición altitud (m)'])
        dataframe_polinomios = pd.DataFrame(self.list_polinomy,
                columns=['Coeficiente a', 'Coeficiente b', 'Coeficiente c'])
                  
        dataframe = pd.concat([dataframe_header, dataframe_polinomios, dataframe_datos], ignore_index=True)
        dataframe.to_csv('Eficiencia/Coast_down'+self.fecha_prueba+'_'+self.fecha_hora_inicio+'.csv', index=False)
        self.msg.setText('Prueba terminada. Se han guardado los datos en el archivo '+'Eficiencia/Coast_down'+self.fecha_prueba+'_'+self.fecha_hora_inicio+'.csv')
        self.msg.show()
    
    """Abrir archivo csv con los datos para calcular potencia"""
    def Potencia_path(self):
        filename = QFileDialog.getOpenFileName()
        self.path_potencia=filename[0]
        self.file_path_power.setText(self.path_potencia)
    
    """Abrir archivo csv con los datos para calcular consumo"""
    def Consumo_path(self):
        filename = QFileDialog.getOpenFileName()
        self.path_consumo_calculo=filename[0]
        self.file_path_consumo.setText(self.path_consumo_calculo)

    """Abrir archivo csv con los datos para calcular rango"""
    def Rango_path(self):
        filename = QFileDialog.getOpenFileName()
        self.path_rango_calculo=filename[0]
        self.file_path_rango.setText(self.path_rango_calculo)
    
    """Guardar en memoria las variables numpy para calcular la potencia electrica."""
    def Power_Accept(self):
        if self.path_potencia !='':
            self.Continuar_potencia=True        
            self.Potencia_values = pd.read_csv(self.path_potencia)
            self.msg.setText('Archivo guardado en memoria con el voltaje y corriente en la batería.')
            self.msg.show()
            if self.Continuar_potencia and self.Continuar_consumo and self.Continuar_rango:
                self.Calcular_eficiencia.setEnabled(True)
    
    """Guardar en memoria las variables numpy para calcular el consumo."""
    def Consumo_Accept(self):
        if self.path_consumo_calculo !='':
            self.Continuar_consumo=True  
            self.Consumo_values = pd.read_csv(self.path_consumo_calculo)
            self.msg.setText('Archivo guardado en memoria con el valor de velocidad para el cálculo de consumo.')
            self.msg.show()
            if self.Continuar_potencia and self.Continuar_consumo and self.Continuar_rango:
                self.Calcular_eficiencia.setEnabled(True)
    
    """Guardar en memoria las variables numpy para calcular el rango."""
    def Rango_Accept(self):
        if self.path_rango_calculo !='':
            self.Continuar_rango=True     
            self.Rango_values = pd.read_csv(self.path_rango_calculo)
            self.msg.setText('Archivo guardado en memoria con el valor de velocidad para el cálculo de rango.')
            self.msg.show()
            if self.Continuar_potencia and self.Continuar_consumo and self.Continuar_rango:
                self.Calcular_eficiencia.setEnabled(True)

    """Se realizan los calculos de consumo de energía y rango en distancia."""
    def Calcular_eficiencia_function(self):
        self.Potencia_values = self.Potencia_values.dropna()                                                                                                                                                                            #Si existe en alguna de las columnas NaN borra la fila con este valor para evitar errores en el procesado de datos
        self.Energy = integrate.trapz(self.Potencia_values['voltaje']*self.Potencia_values['corriente']*1e-3, x=self.Potencia_values['tiempo']/3600)                                                                                         #Calculo de la energía toma los valores de corriente y voltaje se multiplica y se calcula el area bajo la curva vs el tiempo (h) con la regla trapezoidal.
        self.Consumo_values['Velocidad longitudinal (km/h)'] = 3.6*np.sqrt((self.Consumo_values['Velocidad E (m/s)'])**2.0 + (self.Consumo_values['Velocidad N (m/s)'])**2.0 + (self.Consumo_values['Velocidad U (m/s)'])**2.0)         #Calculo de la velocidad longitudinal en km/s a partir de las velocidades en el eje global North, East y Up. (Prueba de consumo)
        self.Energia_consumo = (self.Energy)/(integrate.trapz(self.Consumo_values['Velocidad longitudinal (km/h)'].dropna(), x=self.Consumo_values['Velocidad longitudinal (km/h)'].dropna().index*(0.1/3600)))                                  #Calculo de la posición por medio de la integral con la regla del trapezoide a partir de la velocidad longitudinal. (Prueba de consumo)
        self.Rango_values['Velocidad longitudinal (km/h)'] = 3.6*np.sqrt((self.Rango_values['Velocidad E (m/s)'])**2.0 + (self.Rango_values['Velocidad N (m/s)'])**2.0 + (self.Rango_values['Velocidad U (m/s)'])**2.0)                 #Calculo de la velocidad longitudinal en km/s a partir de las velocidades en el eje global North, East y Up. (Prueba de rango)
        self.Energia_rango = (integrate.trapz(self.Rango_values['Velocidad longitudinal (km/h)'].dropna(), x=self.Rango_values['Velocidad longitudinal (km/h)'].dropna().index*(0.1/3600)))                                                 #Calculo de la posición por medio de la integral con la regla del trapezoide a partir de la velocidad longitudinal. (Prueba de rango)
        self.Valor_consumo.setText(str(self.Energia_consumo))
        self.Valor_rango.setText(str(self.Energia_rango))
        self.path_potencia = ''
        self.path_consumo_calculo = ''
        self.path_rango_calculo = ''
        self.file_path_power.clear()
        self.file_path_consumo.clear()
        self.file_path_rango.clear()
        self.Calcular_eficiencia.setEnabled(False)
        self.Reporte_generado.setEnabled(True)
        self.msg.setText('Energía consumida y rango calculados.')
        self.msg.show()
    
    def Generar_reporte(self):
        report=Report_eficiencia()
        Encargado_prueba=["Juan Pablo Arias", "Esteban Velez", "Juan Carlos Noguera"]
        fecha_hora_finalizacion = datetime.now().strftime("%H/%M/%S").replace('/', '_').replace(' ', '-')
        fecha_consumo = str(self.Consumo_values['1'][0:2].replace('_', '/').replace(' ', '-'))
        fecha_rango = str(self.Rango_values['1'][0:2].replace('_', '/').replace(' ', '-'))
        fecha=[fecha_consumo,fecha_rango,fecha_hora_finalizacion,'20 septiembre de 2022 13:00']
        Datos_vehiculo=['JAC', 'E10X, 2022', 'Auto de pasajeros', '','','27 psi','27 psi']
        Nombre_archivo='Eficiencia/ReporteEficiencia_'+str(fecha_hora_finalizacion)+'.pdf'
        data_graph=[]
        data_graph_velocidad=[]
        data_graph_velocidad_r=[]
        potencia=self.Potencia_values['voltaje']*self.Potencia_values['corriente']*1e-3
        tiempo_hora=self.Potencia_values['tiempo']/3600
        data_graph.append(tuple(zip(tiempo_hora,potencia)))
        data_graph_velocidad.append(tuple(zip(self.Consumo_values['Velocidad longitudinal (km/h)'].dropna().index*(0.01/3600),self.Consumo_values['Velocidad longitudinal (km/h)'].dropna())))
        data_graph_velocidad_r.append(tuple(zip(self.Rango_values['Velocidad longitudinal (km/h)'].dropna().index*(0.01/3600),self.Rango_values['Velocidad longitudinal (km/h)'].dropna())))
        report.get_doc(Nombre_archivo, Encargado_prueba, fecha, Datos_vehiculo, data_graph, data_graph_velocidad, data_graph_velocidad_r, self.Energy, self.Energia_consumo, self.Energia_rango)
        self.msg.setText('Reporte guardado en el archivo pdf '+ Nombre_archivo +'.')
        self.msg.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
