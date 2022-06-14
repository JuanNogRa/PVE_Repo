from provisional_gui import *
from ThreadsDino import *
import math
import config
from datetime import datetime
import pandas as pd
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.SendVoltage = SendVoltage()
        self.ReadVoltage = ReadVoltage()
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
        self.listWidget.clicked.connect(self.listVelocidad)
        self.listWidget_2.clicked.connect(self.listDistance)
        self.select_item=self.listWidget.currentItem()
        self.select_item_dis=self.listWidget_2.currentItem()
        self.Celda0.toggled.connect(self.onClicked)
        self.Celda1.toggled.connect(self.onClicked)
        self.Celda2.toggled.connect(self.onClicked)
       
        self.value=''
        self.VTorque = 'Voltage (V)'
        self.torque_celda_01 = 0
        self.torque_celda_02 = 0
        self.fecha_prueba = ''
        self.fecha_hora_inicio = ''
        self.fecha_hora_finalizacion = ''
        self.dataforDataFrame=[]

        self.Factor_Amplificacion=100
        self.Facto_Atenuacion=20.1
        self.divisor_Voltaje=3
        self.pulsos_vuelta=60
        self.offset_pau=0.00682
        self.diametro_rodillo=19.75*0.0254
        self.sensibilidad_celdas=3
        self.frecuencia=0
        self.capacidad_celdas = 2000             # Capacidad de las celdas de carga en libras.
        self.factor_libras_kilos = 2.205         # Factor de conversión de libras a kilogramos.
        self.factor_kilos_newton = 9.80665
        self.start=time.time()
        #self.ReadFrecuency.FrecuencyUpdate.connect(self.FrecuencySlotUpdate)
    
    def ParamsInput(self):
        self.pulsos_vuelta=float(self.Pulsos_value.text())
        self.diametro_rodillo=float(self.DiametroTambor_value.text())
        self.sensibilidad_celdas=float(self.SencibilidadCelda_value.text())/100
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
        config.startTest_activacte = True
        self.fecha_prueba = datetime.now().strftime("%d/%m/%Y")
        self.fecha_prueba = self.fecha_prueba.replace('/', '_').replace(' ', '-')
        self.fecha_hora_inicio = datetime.now().strftime("%H/%M/%S")
        self.fecha_hora_inicio = self.fecha_hora_inicio.replace('/', '_').replace(' ', '-')
        self.pushButton_2.setEnabled(False)
        self.button_parametro.setEnabled(False)
        self.pushButton.setEnabled(True)
    
    def stopTest(self):
        config.startTest_activacte = False
        self.fecha_hora_finalizacion = datetime.now().strftime("%H/%M/%S")
        self.fecha_hora_finalizacion = self.fecha_hora_finalizacion.replace('/', '_').replace(' ', '-')
        Observaciones=str(self.plainTextEdit.toPlainText())
        dataframe_header = pd.DataFrame([['Fecha',self.fecha_prueba],['Hora de inicio',self.fecha_hora_inicio],
                                        ['Hora de finalización',self.fecha_hora_finalizacion],
                                        ['Voltage de salida analoga',self.value],['Observaciones'+Observaciones]])
        dataframe_datos = pd.DataFrame(self.dataforDataFrame,
                columns=['Muestreo (s)','Voltaje celda #1 (V)', 'Voltaje celda #2 (V)', 'Velocidad medida (m/s)','Voltaje PAU (V)', 'Voltaje de excitación (V)'])
        dataframe = pd.concat([dataframe_header, dataframe_datos], ignore_index=True)
        dataframe.to_csv('/home/usuario/PVE_Repo/Pruebas/'+self.fecha_prueba+'_'+self.fecha_hora_inicio+'.csv', index=False)
        self.dataforDataFrame=[]
        self.pushButton_2.setEnabled(True)
        self.button_parametro.setEnabled(True)
        self.pushButton.setEnabled(False)
        
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

        self.Chan3.setText('{:.5f}'.format((Voltage[1]-self.offset_pau)*self.divisor_Voltaje*self.Facto_Atenuacion)+' V')
        self.Chan4.setText('{:.5f}'.format(Voltage[3]*self.divisor_Voltaje)+' V')
 
    def FrecuencySlotUpdate(self, datos_frecuencia):
        frecuencia=datos_frecuencia[0]
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
            distancia = distancia
            unidad_distancia=str(self.select_item_dis.text())
        elif str(self.select_item_dis.text())=='km':
            distancia/=1000
            unidad_distancia=str(self.select_item_dis.text())
        elif str(self.select_item_dis.text())=='rev':
            distancia=datos_frecuencia[1]/self.pulsos_vuelta
            unidad_distancia=str(self.select_item_dis.text())
        self.Distancia_value.setText('{:.5f}'.format(distancia)+ ' '+unidad_distancia)
        velocidad = revoluciones*((self.diametro_rodillo*math.pi))
        fuerza = (self.torque_celda_01+self.torque_celda_02)/((self.diametro_rodillo)/2)
        potencia = fuerza*velocidad
        potencia_acumulada += potencia
        self.Fuerza_value.setText('{:.5f}'.format(fuerza)+' N')
        self.Potencia_value.setText('{:.5f}'.format(potencia)+' N '+'m/s')
        self.PotenciaAcu_value.setText('{:.5f}'.format(potencia_acumulada)+' N '+unidad)
        
        if(config.startTest_activacte==True):
            time_total = time.time()-self.start
            if(time_total>0.250):
                time_total += time_total
                velocidad = revoluciones*((self.diametro_rodillo*math.pi))
                self.dataforDataFrame.append([time_total, self.Voltage[0]/self.Factor_Amplificacion, self.Voltage[2]/self.Factor_Amplificacion, velocidad, 
                (self.Voltage[1]-self.offset_pau)*(self.divisor_Voltaje*self.Facto_Atenuacion), self.Voltage[3]*self.divisor_Voltaje])
                self.start=time.time()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
