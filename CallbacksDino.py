from provisional_gui import *
from ThreadsDino import *
import config
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.Aplicar.clicked.connect(lambda: self.DACVoltageDC())

    def DACVoltageDC(self):
        self.SendVoltage = SendVoltage()
        if self.SendVoltage.isFinished:
            self.SendVoltage.start()
        config.value=self.plainTextEdit.getText()

    
