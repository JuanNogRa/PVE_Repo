from gui_driver_eficiencia import *
from ThreadGINS import *
import pyqtgraph as pg
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import *
import pandas as pd
from math import sqrt
from datetime import datetime
import numpy as np

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    Velocidad_actual=0.0
    Velocidad_perfil=0.0
    Velocidad_perfil_actual=0
    i=0
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        n_data=20
        self.path=''                            #Declaración de la variable donde se guardar la dirección del archivo .csv donde esta el perfil de velocidad
        self.thread={}
        self.xdata = [x for x in list(range(n_data))]
        self.ydata = [x*0 for x in list(range(n_data))]
        self.ydata1 = [x*0 for x in list(range(n_data))]
        self.data_gins = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0]])
        self.graphWidget1 = pg.PlotWidget()
        self.Senales.addWidget(self.graphWidget1)
        self.pos_indicador = pg.TextItem(text="", color=(0,0,0))
        #self.pos_indicador.hide()
        self.pos_indicador.setZValue(2)
        self.pos_indicador.setFont(QFont('Arial', 40))
        self.graphWidget1.addItem(self.pos_indicador)
        self.pos_indicador.setPos(15,5)
        self.graphWidget1.setBackground('w')
        self.graphWidget1.addLegend(labelTextColor='black',labelTextSize='13pt')
        pen = pg.mkPen(color=(255, 0, 255), width=5)
        pen1 = pg.mkPen(color=(0, 180, 100), width=5, style=QtCore.Qt.DashLine)
        self.graphWidget1.setTitle("Señal de velocidad para prueba con perfil", color="black", size="20pt")
        self.data_line1 =  self.graphWidget1.plot(self.xdata, self.ydata, name = "Velocidad actual", pen=pen)# added
        self.data_line2 =  self.graphWidget1.plot(self.xdata, self.ydata1, name = "Velocidad objetivo", pen=pen1)# added
        
        self.Load_file.clicked.connect(lambda: self.CicloManejoPath())
        self.Accept.clicked.connect(lambda: self.CicloManejoAccept())
        self.Start.clicked.connect(lambda: self.EmpezarCiclo())
        self.Stop.clicked.connect(lambda: self.DetenerCiclo())
        self.Pause.clicked.connect(lambda: self.PauseCiclo())

        self.Start.setEnabled(False)
        self.Stop.setEnabled(False)
        self.Pause.setEnabled(False)

        self.msg = QMessageBox()
        self.msg.setWindowTitle("Panel de información")

    def update_plot(self):
        if self.i<len(self.Velocidad_perfil)-1:
            self.i+=1
        else:
            self.i=0
            n_data=20
            self.xdata = [x for x in list(range(n_data))]
            self.ydata = [x*0 for x in list(range(n_data))]
            self.ydata1 = [x*0 for x in list(range(n_data))]
            self.thread[1].stop()
            self.Start.setEnabled(True)
            self.Pause.setEnabled(False)
            self.Stop.setEnabled(False)
            self.DetenerCiclo()

        self.Velocidad_perfil_actual=self.Velocidad_perfil[self.i,1]
        self.ydata = self.ydata[1:] + [self.Velocidad_actual]  # Remove the first
        self.ydata1 = self.ydata1[1:] + [self.Velocidad_perfil_actual]  # Remove the first
        self.data_line1.setData(self.xdata, self.ydata)  # Update the data.
        self.data_line2.setData(self.xdata, self.ydata1)  # Update the data.
        self.data_gins=np.concatenate((self.data_gins, np.array([[self.gins["nav_vel_E"], self.gins["nav_vel_N"], self.gins["nav_vel_U"],
                        self.gins["acc_x"], self.gins["acc_y"], self.gins["acc_z"],
                        self.gins["nav_Lon"], self.gins["nav_Lat"], self.gins["nav_alt"]]])), axis=0)
        
    def ActualizarVelocidadActual(self, gins):
        vx = 3.6*sqrt((gins["nav_vel_E"])**2 + (gins["nav_vel_N"])**2 + 
				(gins["nav_vel_U"])**2) #km/h
        #print(str(gins["nav_Lon"])+" "+str(gins["nav_Lat"]))
        self.gins=gins
        self.Velocidad_actual=vx
        self.Measure_Gauge.setValue(int(vx))
        if(self.Velocidad_actual-self.Velocidad_perfil_actual<-5):
            #self.Indicaciones.setStyleSheet("color: green")
            self.pos_indicador.setColor((0,128,0))
            self.pos_indicador.setText('Acelere')
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
            self.pos_indicador.setText('Desacelere')
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
            self.pos_indicador.setText('Mantener')
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

    def CicloManejoAccept(self): 
        if self.path !='':
            #self.HOST = self.EditIPHost.text()  # Standard loopback interface address (localhost)        
            df = pd.read_csv(self.path)
            styles = {'color':'black', 'font-size':'15px'}
            self.graphWidget1.setLabel('bottom', 'Tiempo (s)', **styles)
            self.Velocidad_perfil=df.to_numpy()
            #print(len(self.cycle_temp))
            self.data_line2.setData(self.Velocidad_perfil[:,0],  self.Velocidad_perfil[:,1])  # Update the data.
            self.Start.setEnabled(True)

    def EmpezarCiclo(self):
        self.start_workers()
        self.timer = QTimer()
        self.timer.setInterval(250)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()
        self.Start.setEnabled(False)
        self.Pause.setEnabled(True)
        self.Stop.setEnabled(True)
        self.fecha_prueba = datetime.now().strftime("%d/%m/%Y")
        self.fecha_prueba = self.fecha_prueba.replace('/', '_').replace(' ', '-')
        self.fecha_hora_inicio = datetime.now().strftime("%H/%M/%S")
        self.fecha_hora_inicio = self.fecha_hora_inicio.replace('/', '_').replace(' ', '-')
    
    def PauseCiclo(self):
        self.Start.setEnabled(True)
        self.Pause.setEnabled(False)
        self.Stop.setEnabled(True)
        self.timer.stop()

    def DetenerCiclo(self):
        self.Start.setEnabled(True)
        self.Pause.setEnabled(False)
        self.Stop.setEnabled(False)
        self.fecha_hora_finalizacion = datetime.now().strftime("%H/%M/%S")
        self.fecha_hora_finalizacion = self.fecha_hora_finalizacion.replace('/', '_').replace(' ', '-')
        self.timer.stop()
        self.msg.setText('Prueba terminada.')
        self.msg.show()
        dataframe_header = pd.DataFrame([['Fecha',self.fecha_prueba],['Hora de inicio',self.fecha_hora_inicio],
                                        ['Hora de finalización',self.fecha_hora_finalizacion]])
                                        
        dataframe_datos = pd.DataFrame(self.data_gins,
                columns=['Velocidad E (m/s)','Velocidad N (m/s)', 'Velocidad U (m/s)',
                         'Aceleración X (g)','Aceleración Y (g)', 'Aceleración Z (g)',
                         'Posición longitud (deg)','Posición latitud (deg)', 'Posición altitud (m)'])          
        dataframe = pd.concat([dataframe_header, dataframe_datos], ignore_index=True)
        dataframe.to_csv('Perfil_velocidad'+self.fecha_prueba+'_'+self.fecha_hora_inicio+'.csv', index=False)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
