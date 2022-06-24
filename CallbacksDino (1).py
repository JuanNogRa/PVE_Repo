from provisional_gui import *
from ThreadsDino import *
import math
import config
from PyQt5 import QtCore
from datetime import datetime
import pandas as pd
import time
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
#from matplotlib.figure import Figure
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


ygraph=None
"""class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=2, dpi=20):
        #fig = Figure(figsize=(width, height), dpi=dpi)
        fig, axes = plt.subplots()
        #self.axes = fig.add_subplot(111)
        super(MplCanvas,self).__init__(fig, axes)"""

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
        #self.ReadFrecuency.FrecuencyUpdate.connect(self.FrecuencySlotUpdate)
            #f(*args)
        
        self.value=''
        self.VTorque = 'Voltage (V)'
        self.torque_celda_01 = 0
        self.torque_celda_02 = 0
        self.fecha_prueba = ''
        self.fecha_hora_inicio = ''
        self.fecha_hora_finalizacion = ''
        self.dataforDataFrame=[]
        self.potencia_acumulada=0
        self.Tasa_Muestreo=4
        self.muestreo_time=0.0
        self.ygraph=0.0
        
        self.SendVoltage = SendVoltage()
        self.ReadVoltage = ReadVoltage(self.MinimaFrecuencia)
        self.Do_every = Do_every(1/self.Tasa_Muestreo)
        self.pushButton.setEnabled(False)
        self.Aplicar.clicked.connect(lambda: self.DACVoltageDC())
        self.button_parametro.clicked.connect(lambda: self.ParamsInput())
        self.pushButton_2.clicked.connect(lambda: self.startTest())
        self.pushButton.clicked.connect(lambda: self.stopTest())
        #self.ReadFrecuency = ReadFrecuency()
        self.ReadVoltage.start()
        #self.ReadFrecuency.start()
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
        
        self.canvas = MyFigureCanvas(x_len=(100), y_range=[-5, 5], interval=1)
        #toolbar = NavigationToolbar(self.canvas, self)
        #self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        # Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second.
        toolbar = NavigationToolbar(self.canvas, self)
        self.Senales.addWidget(toolbar)
        self.Senales.addWidget(self.canvas)
        self.show
        #self.Graph = Graph(1/self.Tasa_Muestreo)
        #self._plot_ref = None
        

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
        #if self.SendVoltage.isFinished:
        self.value=self.InputVoltage.text()
        self.SendVoltage.main_sendVoltage(self.value)
        #print('Voltaje '+str(config.value))

    def listVelocidad(self):
        self.select_item=self.listWidget.currentItem()

    def listDistance(self):
        self.select_item_dis=self.listWidget_2.currentItem()
    
    def onClicked(self):
        radioBtn = self.sender()
        if radioBtn.isChecked():
            self.VTorque=radioBtn.text()
    
    def startTest(self):
        #self.start=time.time()
        config.startTest_activacte = True
        self.Tasa_Muestreo = float(self.Frecuencia_value.text())
        self.fecha_prueba = datetime.now().strftime("%d/%m/%Y")
        self.fecha_prueba = self.fecha_prueba.replace('/', '_').replace(' ', '-')
        self.fecha_hora_inicio = datetime.now().strftime("%H/%M/%S")
        self.fecha_hora_inicio = self.fecha_hora_inicio.replace('/', '_').replace(' ', '-')
        self.pushButton_2.setEnabled(False)
        self.button_parametro.setEnabled(False)
        self.pushButton.setEnabled(True)
        x_len=int(self.Tasa_Muestreo)
        self.canvas = MyFigureCanvas(x_len=(x_len), y_range=[-5, 5], interval=1/self.Tasa_Muestreo)
        self.show
        #toolbar = NavigationToolbar(self.canvas, self)
        #n_data=int((self.Tasa_Muestreo)*2)
        #self.xdata = [x*(1/(self.Tasa_Muestreo)) for x in list(range(n_data))]
        #self.ydata = [x*0 for x in list(range(n_data))]
        #self._plot_ref = None
        #self.ygraph=0.0
        #self.canvas.axes.cla()  # Clear the canvas.
        
        if self.Do_every.isFinished:
            self.Do_every = Do_every(1/self.Tasa_Muestreo)
            self.Do_every.start()
            self.Do_every.Muestreo_Time.connect(self.Time_MuestreoSlotUpdate)
            #self.Do_every.graph.connect(self.GraphSlotUpdate)
        
        #if self.Graph.isFinished:
         #   self.Graph = Graph(1/self.Tasa_Muestreo)
          #  self.Graph.start()
            
    
    def stopTest(self):
        config.startTest_activacte = False
        self.fecha_hora_finalizacion = datetime.now().strftime("%H/%M/%S")
        self.fecha_hora_finalizacion = self.fecha_hora_finalizacion.replace('/', '_').replace(' ', '-')
        Observaciones=str(self.plainTextEdit.toPlainText())
        dataframe_header = pd.DataFrame([['Fecha',self.fecha_prueba],['Hora de inicio',self.fecha_hora_inicio],
                                        ['Hora de finalización',self.fecha_hora_finalizacion],
                                        ['Voltage de salida analoga',self.value],['Observaciones'+Observaciones]])
        dataframe_datos = pd.DataFrame(self.dataforDataFrame,
                columns=['Muestreo (s)','Cuentas de vueltas','Voltaje celda #1 (V)', 'Voltaje celda #2 (V)',
                         'Velocidad medida (m/s)','Voltaje PAU (V)', 'Voltaje de excitacion (V)'])
        dataframe = pd.concat([dataframe_header, dataframe_datos], ignore_index=True)
        dataframe.to_csv('/home/usuario/PVE_Repo/Pruebas/'+self.fecha_prueba+'_'+self.fecha_hora_inicio+'.csv', index=False)
        self.dataforDataFrame=[]
        self.muestreo=0
        self.pushButton_2.setEnabled(True)
        self.button_parametro.setEnabled(True)
        self.pushButton.setEnabled(False)
        self.Do_every.stop()
        ygraph = None
        #self.Graph.stop()
        
    def VoltageSlotUpdate(self, Voltage):
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
 
    def FrecuencySlotUpdate(self, datos_frecuencia):
        global ygraph
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
        self.potencia_acumulada += potencia
        self.Fuerza_value.setText('{:.5f}'.format(fuerza)+' N')
        self.Potencia_value.setText('{:.5f}'.format(potencia)+' N '+'m/s')
        self.PotenciaAcu_value.setText('{:.5f}'.format(self.potencia_acumulada)+' N '+'m/s')
        
        if(config.startTest_activacte==True):
            if config.f:
                velocidad = revoluciones*((self.diametro_rodillo*math.pi))
                #self.muestreo += time.time()-self.start
                #self.start=time.time()
                self.muestreo += self.muestreo_time
                self.dataforDataFrame.append([self.muestreo, self.cuentas_distancia ,self.Voltage[0]/self.Factor_Amplificacion, self.Voltage[2]/self.Factor_Amplificacion, velocidad, 
                    (self.Voltage[1]-self.offset_pau)*(self.divisor_Voltaje*self.Facto_Atenuacion), self.Voltage[3]*self.divisor_Voltaje])
                ygraph=self.Voltage[0]/self.Factor_Amplificacion
                #print(str(self.xdata)+' '+str(self.ydata))
                
                config.f=False
                #self.Save=False
        
    def Time_MuestreoSlotUpdate(self, MuestreoTime):
        self.muestreo_time=MuestreoTime
        #if config.f:
            #self.update_plot()
            #self.show()
        #if self._plot_ref is None:
            # First time we have no plot reference, so do a normal plot.
            # .plot returns a list of line <reference>s, as we're
            # only getting one we can take the first element.
        #    plot_refs = self.canvas.axes.plot(self.xdata, self.ydata, 'r')
        #    self._plot_ref = plot_refs[0]
        #else:
            # We have a reference, we can use it to update the data for that line.
        #    self._plot_ref.set_ydata(self.ydata)
        
        # Trigger the canvas to update and redraw.
        #self.canvas.draw()
    def update_plot(self):
         # Note: we no longer need to clear the axis.
        # Drop off the first y element, append a new one.
        self.ydata = self.ydata[1:] + [self.ygraph]
        if self._plot_ref is None:
            # First time we have no plot reference, so do a normal plot.
            # .plot returns a list of line <reference>s, as we're
            # only getting one we can take the first element.
            plot_refs = self.canvas.axes.plot(self.xdata, self.ydata, 'r')
            self._plot_ref = plot_refs[0]
        else:
            # We have a reference, we can use it to update the data for that line.
            self._plot_ref.set_ydata(self.ydata)
        self.canvas.flush_events()
        # Trigger the canvas to update and redraw.
        self.canvas.draw()
        #self.axes.draw_artist(self.canvas.patch)
        #self.axes.draw_artist(self._plot_ref)
        #self.canvas.update()
        #self.canvas.flush_events()
        
            
            #if(time.time()-self.start>0.250):
                #self.start=time.time()
class MyFigureCanvas(FigureCanvas):
    '''
    This is the FigureCanvas in which the live plot is drawn.

    '''
    def __init__(self, x_len:int, y_range:list, interval:int) -> None:
        '''
        :param x_len:       The nr of data points shown in one plot.
        :param y_range:     Range on y-axis.
        :param interval:    Get a new datapoint every .. milliseconds.

        '''
        super().__init__(mpl.figure.Figure())
        if ygraph is not None:
            # Range settings
            self._x_len_ = x_len
            self._y_range_ = y_range

            # Store two lists _x_ and _y_
            self._x_ = list(range(0, x_len))
            self._y_ = [0] * x_len

            # Store a figure ax
            self._ax_ = self.figure.subplots()
            self._ax_.set_ylim(ymin=self._y_range_[0], ymax=self._y_range_[1]) # added
            self._line_, = self._ax_.plot(self._x_, self._y_)                  # added
        
            self.draw()                                                        # added

            # Initiate the timer
            self._timer_ = self.new_timer(interval, [(self._update_canvas_, (), {})])
            self._timer_.start()
        return

    def _update_canvas_(self) -> None:
        global ygraph
        '''
        This function gets called regularly by the timer.

        '''
        self._y_.append(ygraph)     # Add new datapoint
        self._y_ = self._y_[-self._x_len_:]                 # Truncate list y

        # Previous code
        # --------------
        # self._ax_.clear()                                   # Clear ax
        # self._ax_.plot(self._x_, self._y_)                  # Plot y(x)
        # self._ax_.set_ylim(ymin=self._y_range_[0], ymax=self._y_range_[1])
        # self.draw()

        # New code
        # ---------
        self._line_.set_ydata(self._y_)
        self._ax_.draw_artist(self._ax_.patch)
        self._ax_.draw_artist(self._line_)
        self.update()
        self.flush_events()
        return
    
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
