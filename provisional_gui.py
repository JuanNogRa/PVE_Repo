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
        MainWindow.resize(435, 229)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Aplicar = QtWidgets.QPushButton(self.centralwidget)
        self.Aplicar.setGeometry(QtCore.QRect(180, 150, 61, 31))
        self.Aplicar.setObjectName("Aplicar")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setGeometry(QtCore.QRect(40, 150, 121, 31))
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.Ch1 = QtWidgets.QLabel(self.centralwidget)
        self.Ch1.setGeometry(QtCore.QRect(50, 50, 47, 13))
        self.Ch1.setObjectName("Ch1")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(50, 70, 47, 13))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(50, 90, 47, 13))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(50, 110, 47, 13))
        self.label_3.setObjectName("label_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Aplicar.setText(_translate("MainWindow", "Aplicar\n"
"Voltaje"))
        self.Ch1.setText(_translate("MainWindow", "Ch1"))
        self.label.setText(_translate("MainWindow", "Ch2"))
        self.label_2.setText(_translate("MainWindow", "Ch3"))
        self.label_3.setText(_translate("MainWindow", "Ch4"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
