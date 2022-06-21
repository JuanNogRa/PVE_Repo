from provisional_gui import *
from ThreadsDino import *
import math
import config
import matplotlib
matplotlib.use('Qt5Agg')
from datetime import datetime
import pandas as pd
import time
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=2, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

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
        self.start = time.time()
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
        self.start=time.time()
        self.Tasa_Muestreo=4
        self.xdata=[]
        self.ydata=[]
        
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
        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.Senales.addWidget(self.canvas)        

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
        self.start=time.time()
        config.startTest_activacte = True
        self.Tasa_Muestreo = float(self.Frecuencia_value.text())
        self.fecha_prueba = datetime.now().strftime("%d/%m/%Y")
        self.fecha_prueba = self.fecha_prueba.replace('/', '_').replace(' ', '-')
        self.fecha_hora_inicio = datetime.now().strftime("%H/%M/%S")
        self.fecha_hora_inicio = self.fecha_hora_inicio.replace('/', '_').replace(' ', '-')
        self.pushButton_2.setEnabled(False)
        self.button_parametro.setEnabled(False)
        self.pushButton.setEnabled(True)
        if self.Do_every.isFinished:
            self.Do_every = Do_every(1/self.Tasa_Muestreo)
            self.Do_every.start()
    
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
                         'Velocidad medida (m/s)','Voltaje PAU (V)', 'Voltaje de excitación (V)'])
        dataframe = pd.concat([dataframe_header, dataframe_datos], ignore_index=True)
        dataframe.to_csv('/home/usuario/PVE_Repo/Pruebas/'+self.fecha_prueba+'_'+self.fecha_hora_inicio+'.csv', index=False)
        self.dataforDataFrame=[]
        self.muestreo=0
        self.pushButton_2.setEnabled(True)
        self.button_parametro.setEnabled(True)
        self.pushButton.setEnabled(False)
        self.Do_every.stop()
        
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
                self.muestreo += time.time()-self.start
                self.dataforDataFrame.append([self.muestreo, self.cuentas_distancia ,self.Voltage[0]/self.Factor_Amplificacion, self.Voltage[2]/self.Factor_Amplificacion, velocidad, 
                    (self.Voltage[1]-self.offset_pau)*(self.divisor_Voltaje*self.Facto_Atenuacion), self.Voltage[3]*self.divisor_Voltaje])
                self.xdata.append(self.muestreo)
                self.ydata.append(self.Voltage[0]/self.Factor_Amplificacion)
                #print(str(self.xdata)+' '+str(self.ydata))
                self.update_plot()
                self.show()
                self.start=time.time()
                config.f=False
                #self.Save=False
        
            
            #if(time.time()-self.start>0.250):
                #self.start=time.time()

    def update_plot(self):
        self.canvas.axes.cla()  # Clear the canvas.
        self.canvas.axes.plot(self.xdata, self.ydata, 'r')
        # Trigger the canvas to update and redraw.
        self.canvas.draw()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
