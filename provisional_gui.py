# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'provisional_gui.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(823, 632)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBox_3 = QtWidgets.QGroupBox(self.tab)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.formLayout_6 = QtWidgets.QFormLayout()
        self.formLayout_6.setObjectName("formLayout_6")
        self.Pulsos = QtWidgets.QLabel(self.groupBox_3)
        self.Pulsos.setObjectName("Pulsos")
        self.formLayout_6.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.Pulsos)
        self.Pulsos_value = QtWidgets.QLineEdit(self.groupBox_3)
        self.Pulsos_value.setObjectName("Pulsos_value")
        self.formLayout_6.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.Pulsos_value)
        self.DiametroTambor = QtWidgets.QLabel(self.groupBox_3)
        self.DiametroTambor.setObjectName("DiametroTambor")
        self.formLayout_6.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.DiametroTambor)
        self.DiametroTambor_value = QtWidgets.QLineEdit(self.groupBox_3)
        self.DiametroTambor_value.setObjectName("DiametroTambor_value")
        self.formLayout_6.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.DiametroTambor_value)
        self.SencibilidadCelda_value = QtWidgets.QLineEdit(self.groupBox_3)
        self.SencibilidadCelda_value.setObjectName("SencibilidadCelda_value")
        self.formLayout_6.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.SencibilidadCelda_value)
        self.SensibilidaCeldad = QtWidgets.QLabel(self.groupBox_3)
        self.SensibilidaCeldad.setObjectName("SensibilidaCeldad")
        self.formLayout_6.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.SensibilidaCeldad)
        self.button_parametro = QtWidgets.QPushButton(self.groupBox_3)
        self.button_parametro.setObjectName("button_parametro")
        self.formLayout_6.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.button_parametro)
        self.verticalLayout_7.addLayout(self.formLayout_6)
        self.gridLayout_2.addWidget(self.groupBox_3, 0, 0, 1, 1)
        self.groupBox_4 = QtWidgets.QGroupBox(self.tab)
        self.groupBox_4.setTitle("")
        self.groupBox_4.setObjectName("groupBox_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.groupBox_4)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.groupBox_2 = QtWidgets.QGroupBox(self.groupBox_4)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setObjectName("formLayout_2")
        self.Frecuency_2 = QtWidgets.QLabel(self.groupBox_2)
        self.Frecuency_2.setObjectName("Frecuency_2")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.Frecuency_2)
        self.Frecuency = QtWidgets.QLabel(self.groupBox_2)
        self.Frecuency.setObjectName("Frecuency")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.Frecuency)
        self.Velocidad = QtWidgets.QLabel(self.groupBox_2)
        self.Velocidad.setObjectName("Velocidad")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.Velocidad)
        self.Velocida_value = QtWidgets.QLabel(self.groupBox_2)
        self.Velocida_value.setObjectName("Velocida_value")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.Velocida_value)
        self.Distancia = QtWidgets.QLabel(self.groupBox_2)
        self.Distancia.setObjectName("Distancia")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.Distancia)
        self.Distancia_value = QtWidgets.QLabel(self.groupBox_2)
        self.Distancia_value.setObjectName("Distancia_value")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.Distancia_value)
        self.verticalLayout_4.addLayout(self.formLayout_2)
        self.horizontalLayout_3.addWidget(self.groupBox_2)
        self.groupBox_5 = QtWidgets.QGroupBox(self.groupBox_4)
        self.groupBox_5.setObjectName("groupBox_5")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_5)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.groupBox_5)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.listWidget = QtWidgets.QListWidget(self.groupBox_5)
        self.listWidget.setObjectName("listWidget")
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        self.verticalLayout_2.addWidget(self.listWidget)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_2 = QtWidgets.QLabel(self.groupBox_5)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_5.addWidget(self.label_2)
        self.listWidget_2 = QtWidgets.QListWidget(self.groupBox_5)
        self.listWidget_2.setObjectName("listWidget_2")
        item = QtWidgets.QListWidgetItem()
        self.listWidget_2.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_2.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_2.addItem(item)
        self.verticalLayout_5.addWidget(self.listWidget_2)
        self.verticalLayout_3.addLayout(self.verticalLayout_5)
        self.horizontalLayout_3.addWidget(self.groupBox_5)
        self.gridLayout_2.addWidget(self.groupBox_4, 1, 0, 1, 1)
        self.groupBox_6 = QtWidgets.QGroupBox(self.tab)
        self.groupBox_6.setTitle("")
        self.groupBox_6.setObjectName("groupBox_6")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.groupBox_6)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.groupBox_8 = QtWidgets.QGroupBox(self.groupBox_6)
        self.groupBox_8.setTitle("")
        self.groupBox_8.setObjectName("groupBox_8")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox_8)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(self.groupBox_8)
        self.groupBox.setObjectName("groupBox")
        self.formLayout_3 = QtWidgets.QFormLayout(self.groupBox)
        self.formLayout_3.setObjectName("formLayout_3")
        self.Ch1_ = QtWidgets.QLabel(self.groupBox)
        self.Ch1_.setObjectName("Ch1_")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.Ch1_)
        self.Chan1 = QtWidgets.QLabel(self.groupBox)
        self.Chan1.setObjectName("Chan1")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.Chan1)
        self.Ch2_ = QtWidgets.QLabel(self.groupBox)
        self.Ch2_.setObjectName("Ch2_")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.Ch2_)
        self.Chan2 = QtWidgets.QLabel(self.groupBox)
        self.Chan2.setObjectName("Chan2")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.Chan2)
        self.Ch3_ = QtWidgets.QLabel(self.groupBox)
        self.Ch3_.setObjectName("Ch3_")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.Ch3_)
        self.Chan3 = QtWidgets.QLabel(self.groupBox)
        self.Chan3.setObjectName("Chan3")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.Chan3)
        self.Ch4_ = QtWidgets.QLabel(self.groupBox)
        self.Ch4_.setObjectName("Ch4_")
        self.formLayout_3.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.Ch4_)
        self.Chan4 = QtWidgets.QLabel(self.groupBox)
        self.Chan4.setObjectName("Chan4")
        self.formLayout_3.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.Chan4)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_11 = QtWidgets.QGroupBox(self.groupBox_8)
        self.groupBox_11.setObjectName("groupBox_11")
        self.verticalLayout_15 = QtWidgets.QVBoxLayout(self.groupBox_11)
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.formLayout_9 = QtWidgets.QFormLayout()
        self.formLayout_9.setObjectName("formLayout_9")
        self.Fuerza = QtWidgets.QLabel(self.groupBox_11)
        self.Fuerza.setObjectName("Fuerza")
        self.formLayout_9.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.Fuerza)
        self.Fuerza_value = QtWidgets.QLabel(self.groupBox_11)
        self.Fuerza_value.setObjectName("Fuerza_value")
        self.formLayout_9.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.Fuerza_value)
        self.Potencia = QtWidgets.QLabel(self.groupBox_11)
        self.Potencia.setObjectName("Potencia")
        self.formLayout_9.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.Potencia)
        self.Potencia_value = QtWidgets.QLabel(self.groupBox_11)
        self.Potencia_value.setObjectName("Potencia_value")
        self.formLayout_9.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.Potencia_value)
        self.PotenciaAcu = QtWidgets.QLabel(self.groupBox_11)
        self.PotenciaAcu.setObjectName("PotenciaAcu")
        self.formLayout_9.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.PotenciaAcu)
        self.PotenciaAcu_value = QtWidgets.QLabel(self.groupBox_11)
        self.PotenciaAcu_value.setObjectName("PotenciaAcu_value")
        self.formLayout_9.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.PotenciaAcu_value)
        self.verticalLayout_15.addLayout(self.formLayout_9)
        self.verticalLayout.addWidget(self.groupBox_11)
        self.horizontalLayout_6.addWidget(self.groupBox_8)
        self.groupBox_7 = QtWidgets.QGroupBox(self.groupBox_6)
        self.groupBox_7.setObjectName("groupBox_7")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.groupBox_7)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.label_3 = QtWidgets.QLabel(self.groupBox_7)
        self.label_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_8.addWidget(self.label_3)
        self.Celda0 = QtWidgets.QRadioButton(self.groupBox_7)
        self.Celda0.setChecked(True)
        self.Celda0.setObjectName("Celda0")
        self.verticalLayout_8.addWidget(self.Celda0)
        self.Celda1 = QtWidgets.QRadioButton(self.groupBox_7)
        self.Celda1.setObjectName("Celda1")
        self.verticalLayout_8.addWidget(self.Celda1)
        self.Celda2 = QtWidgets.QRadioButton(self.groupBox_7)
        self.Celda2.setObjectName("Celda2")
        self.verticalLayout_8.addWidget(self.Celda2)
        self.label_4 = QtWidgets.QLabel(self.groupBox_7)
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        self.verticalLayout_8.addWidget(self.label_4)
        self.label_5 = QtWidgets.QLabel(self.groupBox_7)
        self.label_5.setText("")
        self.label_5.setObjectName("label_5")
        self.verticalLayout_8.addWidget(self.label_5)
        self.label_6 = QtWidgets.QLabel(self.groupBox_7)
        self.label_6.setText("")
        self.label_6.setObjectName("label_6")
        self.verticalLayout_8.addWidget(self.label_6)
        self.label_7 = QtWidgets.QLabel(self.groupBox_7)
        self.label_7.setText("")
        self.label_7.setObjectName("label_7")
        self.verticalLayout_8.addWidget(self.label_7)
        self.verticalLayout_9.addLayout(self.verticalLayout_8)
        self.horizontalLayout_6.addWidget(self.groupBox_7)
        self.gridLayout_2.addWidget(self.groupBox_6, 1, 1, 1, 1)
        self.groupBox_10 = QtWidgets.QGroupBox(self.tab)
        self.groupBox_10.setObjectName("groupBox_10")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.groupBox_10)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.groupBox_10)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.verticalLayout_10.addWidget(self.plainTextEdit)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Frecuencia = QtWidgets.QLabel(self.groupBox_10)
        self.Frecuencia.setObjectName("Frecuencia")
        self.horizontalLayout.addWidget(self.Frecuencia)
        self.Frecuencia_value = QtWidgets.QLineEdit(self.groupBox_10)
        self.Frecuencia_value.setObjectName("Frecuencia_value")
        self.horizontalLayout.addWidget(self.Frecuencia_value)
        self.verticalLayout_10.addLayout(self.horizontalLayout)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox_10)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_9.addWidget(self.pushButton_2)
        self.pushButton = QtWidgets.QPushButton(self.groupBox_10)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_9.addWidget(self.pushButton)
        self.verticalLayout_10.addLayout(self.horizontalLayout_9)
        self.gridLayout_2.addWidget(self.groupBox_10, 2, 1, 1, 1)
        self.groupBox_9 = QtWidgets.QGroupBox(self.tab)
        self.groupBox_9.setObjectName("groupBox_9")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.groupBox_9)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.Modo_control = QtWidgets.QVBoxLayout()
        self.Modo_control.setObjectName("Modo_control")
        self.Lazo_abierto = QtWidgets.QRadioButton(self.groupBox_9)
        self.Lazo_abierto.setChecked(True)
        self.Lazo_abierto.setObjectName("Lazo_abierto")
        self.Modo_control.addWidget(self.Lazo_abierto)
        self.Lazo_cerrado = QtWidgets.QRadioButton(self.groupBox_9)
        self.Lazo_cerrado.setObjectName("Lazo_cerrado")
        self.Modo_control.addWidget(self.Lazo_cerrado)
        self.horizontalLayout_5.addLayout(self.Modo_control)
        self.OutputText = QtWidgets.QGroupBox(self.groupBox_9)
        self.OutputText.setEnabled(True)
        self.OutputText.setCheckable(False)
        self.OutputText.setChecked(False)
        self.OutputText.setObjectName("OutputText")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.OutputText)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.InputVoltage = QtWidgets.QLineEdit(self.OutputText)
        self.InputVoltage.setObjectName("InputVoltage")
        self.horizontalLayout_2.addWidget(self.InputVoltage)
        self.Aplicar = QtWidgets.QPushButton(self.OutputText)
        self.Aplicar.setObjectName("Aplicar")
        self.horizontalLayout_2.addWidget(self.Aplicar)
        self.horizontalLayout_8.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_5.addWidget(self.OutputText)
        self.gridLayout_2.addWidget(self.groupBox_9, 0, 1, 1, 1)
        self.groupBox_12 = QtWidgets.QGroupBox(self.tab)
        self.groupBox_12.setCheckable(True)
        self.groupBox_12.setChecked(False)
        self.groupBox_12.setObjectName("groupBox_12")
        self.verticalLayout_14 = QtWidgets.QVBoxLayout(self.groupBox_12)
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.Path = QtWidgets.QLineEdit(self.groupBox_12)
        self.Path.setObjectName("Path")
        self.horizontalLayout_7.addWidget(self.Path)
        self.Load_file = QtWidgets.QPushButton(self.groupBox_12)
        self.Load_file.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Images/Load.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Load_file.setIcon(icon)
        self.Load_file.setObjectName("Load_file")
        self.horizontalLayout_7.addWidget(self.Load_file)
        self.Accept = QtWidgets.QPushButton(self.groupBox_12)
        self.Accept.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("Images/Accept.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Accept.setIcon(icon1)
        self.Accept.setObjectName("Accept")
        self.horizontalLayout_7.addWidget(self.Accept)
        self.verticalLayout_14.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.LabelIP = QtWidgets.QLabel(self.groupBox_12)
        self.LabelIP.setObjectName("LabelIP")
        self.horizontalLayout_4.addWidget(self.LabelIP)
        self.DataIP = QtWidgets.QLabel(self.groupBox_12)
        self.DataIP.setText("")
        self.DataIP.setObjectName("DataIP")
        self.horizontalLayout_4.addWidget(self.DataIP)
        self.verticalLayout_14.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.LabelIPC = QtWidgets.QLabel(self.groupBox_12)
        self.LabelIPC.setObjectName("LabelIPC")
        self.horizontalLayout_10.addWidget(self.LabelIPC)
        self.DataIPC = QtWidgets.QLabel(self.groupBox_12)
        self.DataIPC.setText("")
        self.DataIPC.setObjectName("DataIPC")
        self.horizontalLayout_10.addWidget(self.DataIPC)
        self.verticalLayout_14.addLayout(self.horizontalLayout_10)
        self.gridLayout_2.addWidget(self.groupBox_12, 2, 0, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.tab_2)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout()
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.Senales = QtWidgets.QVBoxLayout()
        self.Senales.setObjectName("Senales")
        self.verticalLayout_11.addLayout(self.Senales)
        self.line = QtWidgets.QFrame(self.tab_2)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_11.addWidget(self.line)
        self.Senales1 = QtWidgets.QVBoxLayout()
        self.Senales1.setObjectName("Senales1")
        self.verticalLayout_11.addLayout(self.Senales1)
        self.verticalLayout_12.addLayout(self.verticalLayout_11)
        self.tabWidget.addTab(self.tab_2, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Interfaz de Gestión de Dinamometro"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Parámetros del sistema"))
        self.Pulsos.setText(_translate("MainWindow", "Pulsos por revolución:"))
        self.Pulsos_value.setText(_translate("MainWindow", "60"))
        self.DiametroTambor.setText(_translate("MainWindow", "Diámetro del tambor o rodillo (m):"))
        self.DiametroTambor_value.setText(_translate("MainWindow", "0.50165"))
        self.SencibilidadCelda_value.setText(_translate("MainWindow", "3"))
        self.SensibilidaCeldad.setText(_translate("MainWindow", "Sensibilidad de cada celda de carga (mV/V):"))
        self.button_parametro.setText(_translate("MainWindow", "Aplicar\n"
"Parámetros"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Lectura de tacometro"))
        self.Frecuency_2.setText(_translate("MainWindow", "Frecuencia:"))
        self.Frecuency.setText(_translate("MainWindow", "0 Hz"))
        self.Velocidad.setText(_translate("MainWindow", "Velocidad:"))
        self.Velocida_value.setText(_translate("MainWindow", "0 Km/h"))
        self.Distancia.setText(_translate("MainWindow", "Distancia\n"
"recorrida:"))
        self.Distancia_value.setText(_translate("MainWindow", "0 m"))
        self.groupBox_5.setTitle(_translate("MainWindow", "Unidades de medida tacometro"))
        self.label.setText(_translate("MainWindow", "Velocidad"))
        self.listWidget.setSortingEnabled(False)
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        item = self.listWidget.item(0)
        item.setText(_translate("MainWindow", "km/h"))
        item = self.listWidget.item(1)
        item.setText(_translate("MainWindow", "km/s"))
        item = self.listWidget.item(2)
        item.setText(_translate("MainWindow", "m/s"))
        item = self.listWidget.item(3)
        item.setText(_translate("MainWindow", "rev/s"))
        item = self.listWidget.item(4)
        item.setText(_translate("MainWindow", "rpm"))
        item = self.listWidget.item(5)
        item.setText(_translate("MainWindow", "pulsos/min"))
        self.listWidget.setSortingEnabled(__sortingEnabled)
        self.label_2.setText(_translate("MainWindow", "Distancia recorrida"))
        __sortingEnabled = self.listWidget_2.isSortingEnabled()
        self.listWidget_2.setSortingEnabled(False)
        item = self.listWidget_2.item(0)
        item.setText(_translate("MainWindow", "m"))
        item = self.listWidget_2.item(1)
        item.setText(_translate("MainWindow", "km"))
        item = self.listWidget_2.item(2)
        item.setText(_translate("MainWindow", "rev"))
        self.listWidget_2.setSortingEnabled(__sortingEnabled)
        self.groupBox.setTitle(_translate("MainWindow", "Lectura de celdas de carga, PAU y excitación de sensores "))
        self.Ch1_.setText(_translate("MainWindow", "Celda de carga 01:"))
        self.Chan1.setText(_translate("MainWindow", "0V"))
        self.Ch2_.setText(_translate("MainWindow", "Celda de carga 02:"))
        self.Chan2.setText(_translate("MainWindow", "0V"))
        self.Ch3_.setText(_translate("MainWindow", "PAU:"))
        self.Chan3.setText(_translate("MainWindow", "0V"))
        self.Ch4_.setText(_translate("MainWindow", "Excitación sensores:"))
        self.Chan4.setText(_translate("MainWindow", "0V"))
        self.groupBox_11.setTitle(_translate("MainWindow", "Fuerza y potencia"))
        self.Fuerza.setText(_translate("MainWindow", "Fuerza (torque/radio):"))
        self.Fuerza_value.setText(_translate("MainWindow", "0 N"))
        self.Potencia.setText(_translate("MainWindow", "Potencia (fuerza*velocidad):"))
        self.Potencia_value.setText(_translate("MainWindow", "0 W"))
        self.PotenciaAcu.setText(_translate("MainWindow", "Potencia acumulada:"))
        self.PotenciaAcu_value.setText(_translate("MainWindow", "0 W"))
        self.groupBox_7.setTitle(_translate("MainWindow", "Unidades de medida"))
        self.label_3.setText(_translate("MainWindow", "Celdas de carga"))
        self.Celda0.setText(_translate("MainWindow", "Voltage (V)"))
        self.Celda1.setText(_translate("MainWindow", "Torque (N-m)"))
        self.Celda2.setText(_translate("MainWindow", "Peso (kg)"))
        self.groupBox_10.setTitle(_translate("MainWindow", "Menú para generar archivo de prueba"))
        self.plainTextEdit.setPlainText(_translate("MainWindow", "Escriba sus observaciones antes de presionar \"Terminar\" o borre este campo si no tiene..."))
        self.Frecuencia.setText(_translate("MainWindow", "Frecuencia de muestreo (Hz)"))
        self.Frecuencia_value.setText(_translate("MainWindow", "4"))
        self.pushButton_2.setText(_translate("MainWindow", "Empezar"))
        self.pushButton.setText(_translate("MainWindow", "Terminar"))
        self.groupBox_9.setTitle(_translate("MainWindow", "Menú de control"))
        self.Lazo_abierto.setText(_translate("MainWindow", "Lazo abierto"))
        self.Lazo_cerrado.setText(_translate("MainWindow", "Lazo cerrado"))
        self.OutputText.setTitle(_translate("MainWindow", "Salida de voltaje análogo en lazo abierto (V)"))
        self.Aplicar.setText(_translate("MainWindow", "Aplicar"))
        self.groupBox_12.setTitle(_translate("MainWindow", "Ciclo de manejo"))
        self.LabelIP.setText(_translate("MainWindow", "Dirección IP Servidor:"))
        self.LabelIPC.setText(_translate("MainWindow", "Dirección IP Cliente:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Configuración"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Gráficas de señales "))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
