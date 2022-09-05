from gui_driver import *
from PyQt5.QtCore import pyqtSignal,QThread
import socket

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    Velocidad_actual=0.0
    Velocidad_perfil=0.0

    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.Conectar_2.clicked.connect(lambda: self.Socket_connection())
        self.Desconectar_2.clicked.connect(lambda: self.Socket_desconnection())

    def Socket_connection(self):
        HOST=self.IP_address_2.text()
        self.SocketComunication = SocketComunication(HOST)
        self.SocketComunication.start()
        self.SocketComunication.Velocidad_actual.connect(self.ActualizarVelocidadActual)
        self.SocketComunication.Velocidad_perfil.connect(self.ActualizarVelocidadPerfil)
        self.Conectar_2.setEnabled(False)
        self.Desconectar_2.setEnabled(True)
    
    def Socket_desconnection(self):
        self.SocketComunication.stop()
        self.Conectar_2.setEnabled(True)
        self.Desconectar_2.setEnabled(False)
    
    def ActualizarVelocidadActual(self, Velocidad):
        self.Velocidad_actual=Velocidad
        self.Measure_Gauge.setValue(int(Velocidad))
        if(self.Velocidad_actual-self.Velocidad_perfil<5):
            self.Indicaciones.setStyleSheet("color: green")
            self.Measure_Gauge.setStyleSheet("QProgressBar::chunk "
                          "{"
                          "background-color: green;"
                          "}")
            self.Indicaciones.setText("Acelere")
        elif(self.Velocidad_actual-self.Velocidad_perfil<5):
            self.Indicaciones.setStyleSheet("color: red")
            self.Measure_Gauge.setStyleSheet("QProgressBar::chunk "
                          "{"
                          "background-color: red;"
                          "}")
            self.Indicaciones.setText("Desacelere")
        else:
            self.Indicaciones.setStyleSheet("color: yellow")
            self.Measure_Gauge.setStyleSheet("QProgressBar::chunk "
                          "{"
                          "background-color: yellow;"
                          "}")
            self.Indicaciones.setText("Mantener")
    
    def ActualizarVelocidadPerfil(self, Velocidad):
        self.Velocidad_perfil=Velocidad
        self.Source_Gauge.setValue(int(Velocidad))

class SocketComunication(QThread):
    Velocidad_actual = pyqtSignal(float)
    Velocidad_perfil = pyqtSignal(float)

    def __init__(self, HOST):
        QThread.__init__(self)
        self.HOST=HOST
        
    def run(self):
        self.ThreadActive=True
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.HOST, 1338))
            while self.ThreadActive:
                #s.sendall(b"Hello, world")
                s.sendall(b"Recibiendo velocidad actual")
                data = s.recv(1024)
                strings = data.decode('utf8')
                #print(strings)
                #get the num
                num = float(strings)
                self.Velocidad_actual.emit(num)      
                s.sendall(b"Recibiendo velocidad de perfil")
                data = s.recv(1024)
                strings = data.decode('utf8')
                #print(strings)
                #get the num
                num = float(strings)
                self.Velocidad_perfil.emit(num)      

    def stop(self):
        self.ThreadActive = False
        self.quit()
        
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
