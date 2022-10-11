from gui_driver import *
from PyQt5.QtCore import pyqtSignal,QThread
import pyqtgraph as pg
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
import socket

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    Velocidad_actual=0.0
    Velocidad_perfil=0.0

    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.Conectar_2.clicked.connect(lambda: self.Socket_connection())
        self.Desconectar_2.clicked.connect(lambda: self.Socket_desconnection())
        n_data=60
        self.xdata = [x for x in list(range(n_data))]
        self.ydata = [x*0 for x in list(range(n_data))]
        self.ydata1 = [x*0 for x in list(range(n_data))]
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
        
        self.timer = QTimer()
        self.timer.setInterval(250)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()
    
    def update_plot(self):
        self.ydata = self.ydata[1:] + [self.Velocidad_actual]  # Remove the first
        self.ydata1 = self.ydata1[1:] + [self.Velocidad_perfil]  # Remove the first
        self.data_line1.setData(self.xdata, self.ydata)  # Update the data.
        self.data_line2.setData(self.xdata, self.ydata1)  # Update the data.
        
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
        if(self.Velocidad_actual-self.Velocidad_perfil<-5):
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
        elif(self.Velocidad_actual-self.Velocidad_perfil>5):
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
        elif(self.Velocidad_actual-self.Velocidad_perfil>-5 and self.Velocidad_actual-self.Velocidad_perfil<5):
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
    
    def ActualizarVelocidadPerfil(self, Velocidad):
        self.Velocidad_perfil=Velocidad
        #self.Source_Gauge.setValue(int(Velocidad))

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
