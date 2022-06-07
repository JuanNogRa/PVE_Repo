from provisional_gui import *
from ThreadsDino import *
import config
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.SendVoltage = SendVoltage()
        self.ReadVoltage = ReadVoltage()
        self.Aplicar.clicked.connect(lambda: self.DACVoltageDC())
        #self.ReadFrecuency = ReadFrecuency()
        self.ReadVoltage.start()
        #self.ReadFrecuency.start()
        self.ReadVoltage.VoltageUpdate.connect(self.VoltageSlotUpdate)
        self.ReadVoltage.FrecuencyUpdate.connect(self.FrecuencySlotUpdate)
        self.Factor_Amplificacion=100
        self.divisor_Voltaje=3
        #self.ReadFrecuency.FrecuencyUpdate.connect(self.FrecuencySlotUpdate)
    
    def DACVoltageDC(self):
        #if self.SendVoltage.isFinished:
        value=self.InputVoltage.text()
        self.SendVoltage.main_sendVoltage(value)
        #print('Voltaje '+str(config.value))

    def VoltageSlotUpdate(self, Voltage):
        self.Chan1.setText('{:.5f}'.format(Voltage[0]/self.Factor_Amplificacion, 'V'))
        self.Chan2.setText('{:.5f}'.format(Voltage[1]/self.Factor_Amplificacion, 'V'))
        self.Chan3.setText('{:.5f}'.format(Voltage[2]*self.divisor_Voltaje, 'V'))
        self.Chan4.setText('{:.5f}'.format(Voltage[3]*self.divisor_Voltaje, 'V'))
 
    def FrecuencySlotUpdate(self, frecuencia):
        self.Frecuency.setText('{:.2f}'.format(frecuencia, 'Hz  '))
    
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
