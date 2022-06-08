from provisional_gui import *
from ThreadsDino import *
import math
import config
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.SendVoltage = SendVoltage()
        self.ReadVoltage = ReadVoltage()
        self.Aplicar.clicked.connect(lambda: self.DACVoltageDC())
        self.button_parametro.clicked.connect(lambda: self.ParamsInput())
        self.pushButton_2.clicked.connect(lambda: self.startTest())
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
        self.VTorque = 'Voltage (V)'

        self.Factor_Amplificacion=100
        self.divisor_Voltaje=3
        self.pulsos_vuelta=60
        self.diametro_rodillo=19.75*0.0254
        self.sensibilidad_celdas=3
        self.frecuencia=0
        self.capacidad_celdas = 2000             # Capacidad de las celdas de carga en libras.
        self.factor_libras_kilos = 2.205         # Factor de conversión de libras a kilogramos.
        self.factor_kilos_newton = 9.80665
        #self.ReadFrecuency.FrecuencyUpdate.connect(self.FrecuencySlotUpdate)
    
    def ParamsInput(self):
        self.pulsos_vuelta=float(self.Pulsos_value.text())
        self.diametro_rodillo=float(self.DiametroTambor_value.text())
        self.sensibilidad_celdas=float(self.SencibilidadCelda_value.text())/100
        print("Parametros actualizados")

    def DACVoltageDC(self):
        #if self.SendVoltage.isFinished:
        value=self.InputVoltage.text()
        self.SendVoltage.main_sendVoltage(value)
        #print('Voltaje '+str(config.value))

    def listVelocidad(self):
        self.select_item=self.listWidget.currentItem()

    def listDistance(self):
        self.select_item_dis=self.listWidget_2.currentItem()
    
    def onClicked(self):
        radioBtn = self.sender()
        if radioBtn.isChecked():
            self.VTorque=radioBtn.text()
        
    def VoltageSlotUpdate(self, Voltage):
        masa_celda_01 = (Voltage[0]*self.capacidad_celdas)/(self.Factor_Amplificacion*self.sensibilidad_celdas*self.factor_libras_kilos*Voltage[0])
        masa_celda_02 = (Voltage[2]*self.capacidad_celdas)/(self.Factor_Amplificacion*self.sensibilidad_celdas*self.factor_libras_kilos*Voltage[2])
        
        if(self.VTorque=='Voltage (V)'):
            self.Chan1.setText('{:.5f}'.format(Voltage[0]/self.Factor_Amplificacion)+' V')
            self.Chan2.setText('{:.5f}'.format(Voltage[2]/self.Factor_Amplificacion)+' V')
        
        if(self.VTorque=='Torque (N-m)'):
            torque_celda_01 = masa_celda_01*self.factor_kilos_newton*((self.diametro_rodillo)/2)
            torque_celda_02 = masa_celda_02*self.factor_kilos_newton*((self.diametro_rodillo)/2)
            self.Chan1.setText('{:.5f}'.format(torque_celda_01)+' N-m')
            self.Chan2.setText('{:.5f}'.format(torque_celda_02)+' N-m')

        if(self.VTorque=='Peso (kg)'):
            self.Chan1.setText('{:.5f}'.format(masa_celda_01)+' kg')
            self.Chan2.setText('{:.5f}'.format(masa_celda_02)+' kg')

        self.Chan3.setText('{:.5f}'.format(Voltage[1]*self.divisor_Voltaje)+' V')
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
    
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
