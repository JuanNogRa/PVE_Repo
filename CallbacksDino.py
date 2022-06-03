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
        self.ReadFrecuency = ReadFrecuency()
        #self.ReadVoltage.start()
        self.ReadFrecuency.start()
        #self.ReadVoltage.VoltageUpdate.connect(self.VoltageSlotUpdate)
        self.ReadFrecuency.FrecuencyUpdate.connect(self.FrecuencySlotUpdate)
    
    def DACVoltageDC(self):
        #if self.SendVoltage.isFinished:
        self.SendVoltage.main_sendVoltage(value)
        value=self.InputVoltage.text()
        print('Voltaje '+str(config.value))

    def VoltageSlotUpdate(self, Voltage):
        self.Ch1.setText('{:.5f}'.format(Voltage[0], 'V'))
        self.Ch2.setText('{:.5f}'.format(Voltage[1], 'V'))
        self.Ch3.setText('{:.5f}'.format(Voltage[2], 'V'))
        self.Ch4.setText('{:.5f}'.format(Voltage[3], 'V'))
 
    def FrecuencyUpdate(self, frecuencia):
        self.Frecuency.setText('{:.2f}'.format(frecuencia, 'Hz  '))
    
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
