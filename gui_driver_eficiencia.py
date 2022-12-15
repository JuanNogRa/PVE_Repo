# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_driver_eficiencia.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(826, 544)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_6.setContentsMargins(-1, -1, 0, -1)
        self.horizontalLayout_6.setSpacing(100)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.Measure_Gauge_velocidad = QtWidgets.QProgressBar(self.tab)
        self.Measure_Gauge_velocidad.setStyleSheet("QProgressBar {\n"
"border: 2px solid rgba(33, 37, 43, 180);\n"
"border-radius: 5px;\n"
"text-align: center;\n"
"font: 75 14pt \"MS Shell Dlg 2\";\n"
"background-color:transparent;\n"
"color: black;\n"
"width: 80;\n"
"\n"
"}\n"
"QProgressBar::chunk {\n"
"    background-color: rgb(0, 170, 0);\n"
"}")
        self.Measure_Gauge_velocidad.setMaximum(200)
        self.Measure_Gauge_velocidad.setProperty("value", 0)
        self.Measure_Gauge_velocidad.setTextVisible(True)
        self.Measure_Gauge_velocidad.setOrientation(QtCore.Qt.Vertical)
        self.Measure_Gauge_velocidad.setInvertedAppearance(False)
        self.Measure_Gauge_velocidad.setObjectName("Measure_Gauge_velocidad")
        self.horizontalLayout_6.addWidget(self.Measure_Gauge_velocidad)
        self.Senales_velocidad_coast = QtWidgets.QVBoxLayout()
        self.Senales_velocidad_coast.setObjectName("Senales_velocidad_coast")
        self.horizontalLayout_6.addLayout(self.Senales_velocidad_coast)
        self.verticalLayout_5.addLayout(self.horizontalLayout_6)
        self.label_12 = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_12.setFont(font)
        self.label_12.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_12.setObjectName("label_12")
        self.verticalLayout_5.addWidget(self.label_12)
        self.horizontalLayout_18 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_18.setObjectName("horizontalLayout_18")
        self.label_16 = QtWidgets.QLabel(self.tab)
        self.label_16.setObjectName("label_16")
        self.horizontalLayout_18.addWidget(self.label_16)
        self.Velo_max_coast = QtWidgets.QLineEdit(self.tab)
        self.Velo_max_coast.setObjectName("Velo_max_coast")
        self.horizontalLayout_18.addWidget(self.Velo_max_coast)
        self.Accept_velocidad_coast = QtWidgets.QPushButton(self.tab)
        self.Accept_velocidad_coast.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Images/Accept.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Accept_velocidad_coast.setIcon(icon)
        self.Accept_velocidad_coast.setObjectName("Accept_velocidad_coast")
        self.horizontalLayout_18.addWidget(self.Accept_velocidad_coast)
        self.Start_coast = QtWidgets.QPushButton(self.tab)
        self.Start_coast.setObjectName("Start_coast")
        self.horizontalLayout_18.addWidget(self.Start_coast)
        self.verticalLayout_5.addLayout(self.horizontalLayout_18)
        self.tabWidget.addTab(self.tab, "")
        self.Consumo = QtWidgets.QWidget()
        self.Consumo.setObjectName("Consumo")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.Consumo)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_3.setContentsMargins(-1, -1, 0, -1)
        self.horizontalLayout_3.setSpacing(100)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.Measure_Gauge = QtWidgets.QProgressBar(self.Consumo)
        self.Measure_Gauge.setStyleSheet("QProgressBar {\n"
"border: 2px solid rgba(33, 37, 43, 180);\n"
"border-radius: 5px;\n"
"text-align: center;\n"
"font: 75 14pt \"MS Shell Dlg 2\";\n"
"background-color:transparent;\n"
"color: black;\n"
"width: 80;\n"
"\n"
"}\n"
"QProgressBar::chunk {\n"
"    background-color: rgb(0, 170, 0);\n"
"}")
        self.Measure_Gauge.setMaximum(200)
        self.Measure_Gauge.setProperty("value", 0)
        self.Measure_Gauge.setTextVisible(True)
        self.Measure_Gauge.setOrientation(QtCore.Qt.Vertical)
        self.Measure_Gauge.setInvertedAppearance(False)
        self.Measure_Gauge.setObjectName("Measure_Gauge")
        self.horizontalLayout_3.addWidget(self.Measure_Gauge)
        self.Senales = QtWidgets.QVBoxLayout()
        self.Senales.setObjectName("Senales")
        self.horizontalLayout_3.addLayout(self.Senales)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.label_2 = QtWidgets.QLabel(self.Consumo)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.label_9 = QtWidgets.QLabel(self.Consumo)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_15.addWidget(self.label_9)
        self.Velo_max = QtWidgets.QLineEdit(self.Consumo)
        self.Velo_max.setObjectName("Velo_max")
        self.horizontalLayout_15.addWidget(self.Velo_max)
        self.Accept_velocidad = QtWidgets.QPushButton(self.Consumo)
        self.Accept_velocidad.setText("")
        self.Accept_velocidad.setIcon(icon)
        self.Accept_velocidad.setObjectName("Accept_velocidad")
        self.horizontalLayout_15.addWidget(self.Accept_velocidad)
        self.horizontalLayout_5.addLayout(self.horizontalLayout_15)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.Consumo)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.Time_hold = QtWidgets.QLineEdit(self.Consumo)
        self.Time_hold.setObjectName("Time_hold")
        self.horizontalLayout_2.addWidget(self.Time_hold)
        self.Accept_tiempo = QtWidgets.QPushButton(self.Consumo)
        self.Accept_tiempo.setText("")
        self.Accept_tiempo.setIcon(icon)
        self.Accept_tiempo.setObjectName("Accept_tiempo")
        self.horizontalLayout_2.addWidget(self.Accept_tiempo)
        self.horizontalLayout_5.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_4 = QtWidgets.QLabel(self.Consumo)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.Path = QtWidgets.QLineEdit(self.Consumo)
        self.Path.setObjectName("Path")
        self.horizontalLayout_4.addWidget(self.Path)
        self.Accept = QtWidgets.QPushButton(self.Consumo)
        self.Accept.setText("")
        self.Accept.setIcon(icon)
        self.Accept.setObjectName("Accept")
        self.horizontalLayout_4.addWidget(self.Accept)
        self.Load_file = QtWidgets.QPushButton(self.Consumo)
        self.Load_file.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("Images/Load.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Load_file.setIcon(icon1)
        self.Load_file.setObjectName("Load_file")
        self.horizontalLayout_4.addWidget(self.Load_file)
        self.Start = QtWidgets.QPushButton(self.Consumo)
        self.Start.setObjectName("Start")
        self.horizontalLayout_4.addWidget(self.Start)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.tabWidget.addTab(self.Consumo, "")
        self.Rango = QtWidgets.QWidget()
        self.Rango.setObjectName("Rango")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.Rango)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_10.setContentsMargins(-1, -1, 0, -1)
        self.horizontalLayout_10.setSpacing(100)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.Measure_Gauge_3 = QtWidgets.QProgressBar(self.Rango)
        self.Measure_Gauge_3.setStyleSheet("QProgressBar {\n"
"border: 2px solid rgba(33, 37, 43, 180);\n"
"border-radius: 5px;\n"
"text-align: center;\n"
"font: 75 14pt \"MS Shell Dlg 2\";\n"
"background-color:transparent;\n"
"color: black;\n"
"width: 80;\n"
"\n"
"}\n"
"QProgressBar::chunk {\n"
"    background-color: rgb(0, 170, 0);\n"
"}")
        self.Measure_Gauge_3.setMaximum(200)
        self.Measure_Gauge_3.setProperty("value", 0)
        self.Measure_Gauge_3.setTextVisible(True)
        self.Measure_Gauge_3.setOrientation(QtCore.Qt.Vertical)
        self.Measure_Gauge_3.setInvertedAppearance(False)
        self.Measure_Gauge_3.setObjectName("Measure_Gauge_3")
        self.horizontalLayout_10.addWidget(self.Measure_Gauge_3)
        self.Senales_3 = QtWidgets.QVBoxLayout()
        self.Senales_3.setObjectName("Senales_3")
        self.horizontalLayout_10.addLayout(self.Senales_3)
        self.verticalLayout_3.addLayout(self.horizontalLayout_10)
        self.label_8 = QtWidgets.QLabel(self.Rango)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_3.addWidget(self.label_8)
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.label_10 = QtWidgets.QLabel(self.Rango)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_16.addWidget(self.label_10)
        self.Velo_max_rango = QtWidgets.QLineEdit(self.Rango)
        self.Velo_max_rango.setObjectName("Velo_max_rango")
        self.horizontalLayout_16.addWidget(self.Velo_max_rango)
        self.Accept_velocidad_rango = QtWidgets.QPushButton(self.Rango)
        self.Accept_velocidad_rango.setText("")
        self.Accept_velocidad_rango.setIcon(icon)
        self.Accept_velocidad_rango.setObjectName("Accept_velocidad_rango")
        self.horizontalLayout_16.addWidget(self.Accept_velocidad_rango)
        self.horizontalLayout_13.addLayout(self.horizontalLayout_16)
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.label_7 = QtWidgets.QLabel(self.Rango)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_12.addWidget(self.label_7)
        self.Time_hold_rango = QtWidgets.QLineEdit(self.Rango)
        self.Time_hold_rango.setObjectName("Time_hold_rango")
        self.horizontalLayout_12.addWidget(self.Time_hold_rango)
        self.Accept_tiempo_rango = QtWidgets.QPushButton(self.Rango)
        self.Accept_tiempo_rango.setText("")
        self.Accept_tiempo_rango.setIcon(icon)
        self.Accept_tiempo_rango.setObjectName("Accept_tiempo_rango")
        self.horizontalLayout_12.addWidget(self.Accept_tiempo_rango)
        self.horizontalLayout_13.addLayout(self.horizontalLayout_12)
        self.verticalLayout_3.addLayout(self.horizontalLayout_13)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.label_6 = QtWidgets.QLabel(self.Rango)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_11.addWidget(self.label_6)
        self.Path_rango = QtWidgets.QLineEdit(self.Rango)
        self.Path_rango.setObjectName("Path_rango")
        self.horizontalLayout_11.addWidget(self.Path_rango)
        self.Accept_rango1 = QtWidgets.QPushButton(self.Rango)
        self.Accept_rango1.setText("")
        self.Accept_rango1.setIcon(icon)
        self.Accept_rango1.setObjectName("Accept_rango1")
        self.horizontalLayout_11.addWidget(self.Accept_rango1)
        self.Load_file_rango = QtWidgets.QPushButton(self.Rango)
        self.Load_file_rango.setText("")
        self.Load_file_rango.setIcon(icon1)
        self.Load_file_rango.setObjectName("Load_file_rango")
        self.horizontalLayout_11.addWidget(self.Load_file_rango)
        self.Start_rango = QtWidgets.QPushButton(self.Rango)
        self.Start_rango.setObjectName("Start_rango")
        self.horizontalLayout_11.addWidget(self.Start_rango)
        self.Stop = QtWidgets.QPushButton(self.Rango)
        self.Stop.setObjectName("Stop")
        self.horizontalLayout_11.addWidget(self.Stop)
        self.verticalLayout_3.addLayout(self.horizontalLayout_11)
        self.tabWidget.addTab(self.Rango, "")
        self.Calcular = QtWidgets.QWidget()
        self.Calcular.setObjectName("Calcular")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.Calcular)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.groupBox = QtWidgets.QGroupBox(self.Calcular)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.Accept_consumo = QtWidgets.QPushButton(self.groupBox)
        self.Accept_consumo.setText("")
        self.Accept_consumo.setIcon(icon)
        self.Accept_consumo.setObjectName("Accept_consumo")
        self.gridLayout.addWidget(self.Accept_consumo, 1, 3, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.groupBox)
        self.label_13.setObjectName("label_13")
        self.gridLayout.addWidget(self.label_13, 0, 0, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.groupBox)
        self.label_11.setText("")
        self.label_11.setObjectName("label_11")
        self.gridLayout.addWidget(self.label_11, 0, 4, 1, 1)
        self.Load_power = QtWidgets.QPushButton(self.groupBox)
        self.Load_power.setText("")
        self.Load_power.setIcon(icon1)
        self.Load_power.setObjectName("Load_power")
        self.gridLayout.addWidget(self.Load_power, 0, 2, 1, 1)
        self.file_path_power = QtWidgets.QLineEdit(self.groupBox)
        self.file_path_power.setObjectName("file_path_power")
        self.gridLayout.addWidget(self.file_path_power, 0, 1, 1, 1)
        self.Load_consumo = QtWidgets.QPushButton(self.groupBox)
        self.Load_consumo.setText("")
        self.Load_consumo.setIcon(icon1)
        self.Load_consumo.setObjectName("Load_consumo")
        self.gridLayout.addWidget(self.Load_consumo, 1, 2, 1, 1)
        self.file_path_consumo = QtWidgets.QLineEdit(self.groupBox)
        self.file_path_consumo.setObjectName("file_path_consumo")
        self.gridLayout.addWidget(self.file_path_consumo, 1, 1, 1, 1)
        self.label_14 = QtWidgets.QLabel(self.groupBox)
        self.label_14.setObjectName("label_14")
        self.gridLayout.addWidget(self.label_14, 1, 0, 1, 1)
        self.Accept_power = QtWidgets.QPushButton(self.groupBox)
        self.Accept_power.setText("")
        self.Accept_power.setIcon(icon)
        self.Accept_power.setObjectName("Accept_power")
        self.gridLayout.addWidget(self.Accept_power, 0, 3, 1, 1)
        self.label_15 = QtWidgets.QLabel(self.groupBox)
        self.label_15.setObjectName("label_15")
        self.gridLayout.addWidget(self.label_15, 2, 0, 1, 1)
        self.file_path_rango = QtWidgets.QLineEdit(self.groupBox)
        self.file_path_rango.setObjectName("file_path_rango")
        self.gridLayout.addWidget(self.file_path_rango, 2, 1, 1, 1)
        self.Load_rango = QtWidgets.QPushButton(self.groupBox)
        self.Load_rango.setText("")
        self.Load_rango.setIcon(icon1)
        self.Load_rango.setObjectName("Load_rango")
        self.gridLayout.addWidget(self.Load_rango, 2, 2, 1, 1)
        self.Accept_rango = QtWidgets.QPushButton(self.groupBox)
        self.Accept_rango.setText("")
        self.Accept_rango.setIcon(icon)
        self.Accept_rango.setObjectName("Accept_rango")
        self.gridLayout.addWidget(self.Accept_rango, 2, 3, 1, 1)
        self.verticalLayout_10.addLayout(self.gridLayout)
        self.horizontalLayout_17 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_17.setObjectName("horizontalLayout_17")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_17.addItem(spacerItem)
        self.Calcular_eficiencia = QtWidgets.QPushButton(self.groupBox)
        self.Calcular_eficiencia.setObjectName("Calcular_eficiencia")
        self.horizontalLayout_17.addWidget(self.Calcular_eficiencia)
        self.verticalLayout_10.addLayout(self.horizontalLayout_17)
        self.verticalLayout_9.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(self.Calcular)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.Valor_consumo = QtWidgets.QLabel(self.groupBox_2)
        self.Valor_consumo.setText("")
        self.Valor_consumo.setObjectName("Valor_consumo")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.Valor_consumo)
        self.label_5 = QtWidgets.QLabel(self.groupBox_2)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.Valor_rango = QtWidgets.QLabel(self.groupBox_2)
        self.Valor_rango.setText("")
        self.Valor_rango.setObjectName("Valor_rango")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.Valor_rango)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.Reporte_generado = QtWidgets.QPushButton(self.groupBox_2)
        self.Reporte_generado.setObjectName("Reporte_generado")
        self.horizontalLayout.addWidget(self.Reporte_generado)
        self.formLayout.setLayout(2, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout)
        self.verticalLayout_4.addLayout(self.formLayout)
        self.verticalLayout_9.addWidget(self.groupBox_2)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_9.addItem(spacerItem2)
        self.tabWidget.addTab(self.Calcular, "")
        self.verticalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Interfaz para prueba con perfil de velocidad"))
        self.Measure_Gauge_velocidad.setFormat(_translate("MainWindow", "%v km/h"))
        self.label_12.setText(_translate("MainWindow", "Velocidad\n"
"actual"))
        self.label_16.setText(_translate("MainWindow", "Velocidad\n"
"Máxima (km/h)"))
        self.Start_coast.setText(_translate("MainWindow", "Empezar"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Coast-down"))
        self.Measure_Gauge.setFormat(_translate("MainWindow", "%v km/h"))
        self.label_2.setText(_translate("MainWindow", "Velocidad\n"
"actual"))
        self.label_9.setText(_translate("MainWindow", "Velocidad\n"
"Máxima (km/h)"))
        self.label.setText(_translate("MainWindow", "Tiempo\n"
"Zero Hold (s):"))
        self.label_4.setText(_translate("MainWindow", "Carga de archivo\n"
"perfil de velocidad"))
        self.Start.setText(_translate("MainWindow", "Empezar"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Consumo), _translate("MainWindow", "Consumo"))
        self.Measure_Gauge_3.setFormat(_translate("MainWindow", "%v km/h"))
        self.label_8.setText(_translate("MainWindow", "Velocidad\n"
"actual"))
        self.label_10.setText(_translate("MainWindow", "Velocidad\n"
"Máxima(km/h)"))
        self.label_7.setText(_translate("MainWindow", "Tiempo\n"
"Zero Hold (s):"))
        self.label_6.setText(_translate("MainWindow", "Carga de archivo\n"
"perfil de velocidad"))
        self.Start_rango.setText(_translate("MainWindow", "Empezar"))
        self.Stop.setText(_translate("MainWindow", "Detener"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Rango), _translate("MainWindow", "Rango"))
        self.groupBox.setTitle(_translate("MainWindow", "Carga de archivos para calcular"))
        self.label_13.setText(_translate("MainWindow", "Archivo .csv de potencia eléctrica:"))
        self.label_14.setText(_translate("MainWindow", "Archivo .csv de prueba de consumo:"))
        self.label_15.setText(_translate("MainWindow", "Archivo .csv de prueba de rango:"))
        self.Calcular_eficiencia.setText(_translate("MainWindow", "Calcular"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Calculos y generación de reporte"))
        self.label_3.setText(_translate("MainWindow", "Consumo de energía (kW.h/km):"))
        self.label_5.setText(_translate("MainWindow", "Rango consumo de total de energía (km):"))
        self.Reporte_generado.setText(_translate("MainWindow", "Generar\n"
"reporte"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Calcular), _translate("MainWindow", "Calculo y reporte"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())