# Prueba multithreading usando cDAQ-91-88 y GINS200
# Se tiene un objeto que hereda de QThread para cada conexión y un objeto 
#  para la adquisición con un tiempo de muestreo determinado
# Se agregan funcionalidades a los labels y gráficas por prueba
import numpy as np
from nidaqmx import constants
from ast import Continue
#import nidaqmx as daq
from math import sqrt
import time
#import numpy 
#import matplotlib.pyplot as plt
from datetime import datetime
import sqlite3
import threading
from nidaqmx import stream_readers
import serial
import nidaqmx
#from nidaqmx.constants import TerminalConfiguration
from bitstring import BitArray
from pyqtgraph import PlotWidget, plot, mkPen
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel,QComboBox,QTabWidget, QMessageBox, QAction
from PyQt5.QtCore import pyqtSlot,QTimer,Qt,QObject, QThread, pyqtSignal
from PyQt5 import uic

start=False

class UI(QMainWindow):
	def __init__(self):
		QMainWindow.__init__(self)
		self.tab_index = 0
		self.fase_frenado = 1
		self.fases_frenado = ['Eficiencia en frío','Calentamiento','Eficiencia en caliente',
			'Recuperación','Eficiencia de recuperación']
		self.setupUi()
		#icon = QtGui.QIcon()
		#icon.addPixmap(QtGui.QPixmap("PyShine.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		#self.setWindowIcon(icon)
		self.thread={}
		self.pause = False
		self.gins_data = {}
		self.cdaq_data = {}
		self.sensors_data = {}

		self.xdata = [x*0.1 for x in list(range(15))]
		self.ydata = [x*0 for x in list(range(15))]
		self.ydata = [self.ydata, self.ydata, self.ydata, self.ydata,self.ydata,self.ydata]
		self.line1 = None
		self.line2 = None
		self.line3 = None
		self.t = -0.1
		self.line1 = self.fre_widget_plot.plot(self.xdata,self.ydata[0],pen=self.red_pen,symbol='+', symbolSize=10, symbolBrush=('b'))
		self.line2 = self.est_widget_plot.plot(self.xdata,self.ydata[0],pen=self.red_pen,symbol='+', symbolSize=10, symbolBrush=('b'))
		self.line3 = self.vib_widget_plot.plot(self.xdata,self.ydata[0],pen=self.red_pen,symbol='+', symbolSize=10, symbolBrush=('b'))
		self.start_workers()
		
		self.timer = QTimer()

	def setupUi(self):
		uic.loadUi("PVE-Python\interfaz_app.ui",self)
				
		self.tabs_pruebas = self.findChild(QTabWidget,"tabs_pruebas")
		self.tabs_pruebas.currentChanged.connect(self.tab_change)
		self.tab_index = self.tabs_pruebas.currentIndex()
		print(f'Current tab: {self.tab_index}')

		self.button_start = self.findChild(QPushButton,"button_start")
		self.button_start.clicked.connect(self.start_acquisition)
		self.button_stop = self.findChild(QPushButton,"button_stop")
		self.button_stop.clicked.connect(self.stop_acquisition)
		self.button_stop.setEnabled(False)

		#Fase de frenado - Labels de salida
		self.label_f_1 = self.findChild(QLabel,"label_fre_1")
		self.label_f_2 = self.findChild(QLabel,"label_fre_2")
		self.label_f_3 = self.findChild(QLabel,"label_fre_3")
		self.label_f_4 = self.findChild(QLabel,"label_fre_4")
		self.label_f_5 = self.findChild(QLabel,"label_fre_5")
		self.label_f_6 = self.findChild(QLabel,"label_fre_6")
		#Fase de frenado - Labels de título
		self.label_f_fase = self.findChild(QLabel,"label_fre_fase")
		self.label_f_vx = self.findChild(QLabel,"label_fre_vx")
		self.label_f_ax = self.findChild(QLabel,"label_fre_ax")
		self.label_f_fp = self.findChild(QLabel,"label_fre_fp")
		self.label_f_df_Td = self.findChild(QLabel,"label_fre_df_Td")
		self.label_f_Ti = self.findChild(QLabel,"label_fre_Ti")
		self.label_f_t_dr = self.findChild(QLabel,"label_fre_t_dr")
		#Fase de frenado - Ocultar labels iniciales
		self.label_f_5.hide()
		self.label_f_6.hide()
		self.label_f_Ti.hide()
		self.label_f_t_dr.hide()
		self.button_f_fase = self.findChild(QPushButton,"button_fre_fase")
		self.button_f_fase.clicked.connect(self.cambiar_fase)
		self.button_f_rst = self.findChild(QPushButton,"button_fre_rst")
		self.button_f_rst.clicked.connect(self.reiniciar_fase)
		self.combo_f_plot = self.findChild(QComboBox,"combo_fre_plot")
		#self.combo_f_plot.activated.connect(self.cambiar_f_plot)

		#Prueba de estabilidad - Labels de salida
		self.label_e_vx = self.findChild(QLabel,"label_est_vx")
		self.label_e_ay = self.findChild(QLabel,"label_est_ay")
		self.label_e_delta = self.findChild(QLabel,"label_est_delta")
		self.label_e_beta = self.findChild(QLabel,"label_est_beta")
		self.label_e_phi = self.findChild(QLabel,"label_est_phi")
		self.combo_e_plot = self.findChild(QComboBox,"combo_est_plot")

		#Prueba de vibraciones - Labels de salida
		self.label_v_ax = self.findChild(QLabel,"label_vib_ax")
		self.label_v_ay = self.findChild(QLabel,"label_vib_ay")
		self.label_v_az = self.findChild(QLabel,"label_vib_az")
		self.combo_v_plot = self.findChild(QComboBox,"combo_vib_plot")


		##----------INSERTAR OTRAS PRUEBAS----------##

		#Modo de prueba - ComboBox
		self.combo_prueba = self.findChild(QComboBox,"combo_prueba")
		#self.combo_prueba.activated.connect(self.cambiar_disp_prueba)
		#Modo de prueba - Labels de título
		self.label_p_1 = self.findChild(QLabel,"label_prb_1")
		self.label_p_2 = self.findChild(QLabel,"label_prb_2")
		self.label_p_3 = self.findChild(QLabel,"label_prb_3")
		self.label_p_4 = self.findChild(QLabel,"label_prb_4")
		self.label_p_5 = self.findChild(QLabel,"label_prb_5")
		self.label_p_6 = self.findChild(QLabel,"label_prb_6")
		self.label_p_7 = self.findChild(QLabel,"label_prb_7")
		self.label_p_8 = self.findChild(QLabel,"label_prb_8")
		self.label_p_9 = self.findChild(QLabel,"label_prb_9")
		self.label_p_10 = self.findChild(QLabel,"label_prb_10")
		self.label_p_11 = self.findChild(QLabel,"label_prb_11")
		self.label_p_12 = self.findChild(QLabel,"label_prb_12")
		self.label_p_13 = self.findChild(QLabel,"label_prb_13")
		self.label_p_14 = self.findChild(QLabel,"label_prb_14")
		self.label_p_15 = self.findChild(QLabel,"label_prb_15")
		self.label_p_16 = self.findChild(QLabel,"label_prb_16")
		self.label_p_17 = self.findChild(QLabel,"label_prb_17")
		self.label_p_18 = self.findChild(QLabel,"label_prb_18")
		self.label_p_19 = self.findChild(QLabel,"label_prb_19")
		self.label_p_20 = self.findChild(QLabel,"label_prb_20")
		self.label_p_21 = self.findChild(QLabel,"label_prb_21")
		self.label_p_22 = self.findChild(QLabel,"label_prb_22")
		self.label_p_23 = self.findChild(QLabel,"label_prb_23")
		self.label_p_24 = self.findChild(QLabel,"label_prb_24")
		self.label_p_25 = self.findChild(QLabel,"label_prb_25")
		self.label_p_26 = self.findChild(QLabel,"label_prb_26")
		self.label_p_27 = self.findChild(QLabel,"label_prb_27")
		self.label_p_28 = self.findChild(QLabel,"label_prb_28")
		self.label_p_29 = self.findChild(QLabel,"label_prb_29")
		self.label_p_30 = self.findChild(QLabel,"label_prb_30")
		self.label_p_31 = self.findChild(QLabel,"label_prb_31")
		self.label_p_32 = self.findChild(QLabel,"label_prb_32")
		#Modo de prueba - Labels de salida
		self.label_p_ax = self.findChild(QLabel,"label_prb_ax")
		self.label_p_ay = self.findChild(QLabel,"label_prb_ay")
		self.label_p_az = self.findChild(QLabel,"label_prb_az")
		self.label_p_fp_Gx = self.findChild(QLabel,"label_prb_fp_Gx")
		self.label_p_d_Gy = self.findChild(QLabel,"label_prb_delta_Gy")
		self.label_p_Gz = self.findChild(QLabel,"label_prb_Gz")
		self.label_p_Mx = self.findChild(QLabel,"label_prb_Mx")
		self.label_p_My = self.findChild(QLabel,"label_prb_My")
		self.label_p_Mz = self.findChild(QLabel,"label_prb_Mz")
		self.label_p_T = self.findChild(QLabel,"label_prb_T")
		self.label_p_vrF_rollNav = self.findChild(QLabel,"label_prb_vr_F_rollNav")
		self.label_p_vrR_pitchNav = self.findChild(QLabel,"label_prb_vr_R_pitchNav")
		self.label_p_vrL_yawNav = self.findChild(QLabel,"label_prb_vr_L_yawNav")
		self.label_p_v5r_velENav = self.findChild(QLabel,"label_prb_v5_r_velENav")
		self.label_p_velNNav = self.findChild(QLabel,"label_prb_velNNav")
		self.label_p_velUNav = self.findChild(QLabel,"label_prb_velUNav")
		self.label_p_LonNav = self.findChild(QLabel,"label_prb_LonNav")
		self.label_p_LatNav = self.findChild(QLabel,"label_prb_LatNav")
		self.label_p_altNav = self.findChild(QLabel,"label_prb_altNav")
		self.label_p_Hbar = self.findChild(QLabel,"label_prb_Hbar")
		self.label_p_Td_rollGPS = self.findChild(QLabel,"label_prb_Td_rollGPS")
		self.label_p_Ti_pitchGPS = self.findChild(QLabel,"label_prb_Ti_pitchGPS")
		self.label_p_B1_yawGPS = self.findChild(QLabel,"label_prb_B1_yawGPS")
		self.label_p_B2_velEGPS = self.findChild(QLabel,"label_prb_B2_velEGPS")
		self.label_p_velNGPS = self.findChild(QLabel,"label_prb_velNGPS")
		self.label_p_velUGPS = self.findChild(QLabel,"label_prb_velUGPS")
		self.label_p_LonGPS = self.findChild(QLabel,"label_prb_LonGPS")
		self.label_p_LatGPS = self.findChild(QLabel,"label_prb_LatGPS")
		self.label_p_AltGPS = self.findChild(QLabel,"label_prb_AltGPS")
		#Modo de prueba - Ocultar labels iniciales
		self.label_p_6.hide()
		self.label_p_7.hide()
		self.label_p_8.hide()
		self.label_p_9.hide()
		self.label_p_10.hide()
		self.label_p_15.hide()
		self.label_p_16.hide()
		self.label_p_17.hide()
		self.label_p_18.hide()
		self.label_p_19.hide()
		self.label_p_20.hide()
		self.label_p_25.hide()
		self.label_p_26.hide()
		self.label_p_27.hide()
		self.label_p_28.hide()
		self.label_p_29.hide()
		self.label_p_30.hide()
		#self.label_p_31.hide()
		self.label_p_32.hide()
		self.label_p_Gz.hide()
		self.label_p_Mx.hide()
		self.label_p_My.hide()
		self.label_p_Mz.hide()
		self.label_p_T.hide()
		self.label_p_velNNav.hide()
		self.label_p_velUNav.hide()
		self.label_p_LonNav.hide()
		self.label_p_LatNav.hide()
		self.label_p_altNav.hide()
		self.label_p_Hbar.hide()
		self.label_p_velNGPS.hide()
		self.label_p_velUGPS.hide()
		self.label_p_LonGPS.hide()
		self.label_p_LatGPS.hide()
		self.label_p_AltGPS.hide()

		self.label_p_31.setText('Sensores')
		self.combo_prueba.activated.connect(self.cambiar_disp_prueba)

		self.fre_widget_plot = self.findChild(PlotWidget,"fre_widget_plot")
		self.fre_widget_plot.setBackground('w')

		self.est_widget_plot = self.findChild(PlotWidget,"est_widget_plot")
		self.est_widget_plot.setBackground('w')
		
		self.vib_widget_plot = self.findChild(PlotWidget,"vib_widget_plot")
		self.vib_widget_plot.setBackground('w')

		self.red_pen = mkPen(color=(255, 0, 0), width=1)

		finish = QAction("Quit", self)
		finish.triggered.connect(self.closeEvent)

		self.show()

	@pyqtSlot()
	def tab_change(self):
		self.tab_index = self.tabs_pruebas.currentIndex()
		print(f'Current tab: {self.tab_index}')
		self.xdata = [x*0.1 for x in list(range(15))]
		self.ydata = [x*0 for x in list(range(15))]
		self.ydata = [self.ydata, self.ydata, self.ydata, self.ydata,self.ydata,self.ydata]
		self.t = -0.1

	@pyqtSlot()
	def start_acquisition(self):
		global start, d2db
		print('Configuring devices...') # Mostrar un mensaje en pantalla
		time.sleep(1)
		print('Start acquisition')
		start=True
		self.button_start.setEnabled(False)
		self.button_stop.setEnabled(True)
		self.combo_prueba.setEnabled(False)
		for index in (0,1,2,3,4):
			if index!=self.tab_index:
				self.tabs_pruebas.setTabEnabled(index,False)

		self.timer.setInterval(100)
		self.timer.timeout.connect(self.update_plot)
		self.timer.start()

		self.button_start.setEnabled(False)
		self.button_stop.setEnabled(True)

	@pyqtSlot()
	def stop_acquisition(self):
		global start
		print('Stop acquisition')
		self.timer.stop()
		start=False
		self.button_start.setEnabled(True)
		self.button_stop.setEnabled(False)
		self.combo_prueba.setEnabled(True)
		for index in (0,1,2,3,4):
			self.tabs_pruebas.setTabEnabled(index,True)

	@pyqtSlot()
	def cambiar_fase(self):
		self.xdata = [x*0.1 for x in list(range(15))]
		self.ydata = [x*0 for x in list(range(15))]
		self.ydata = [self.ydata, self.ydata, self.ydata, self.ydata,self.ydata,self.ydata]
		self.t = -0.1
		#self.line1 = self.fre_widget_plot.plot(self.xdata,self.ydata[0],pen=self.red_pen,symbol='+', symbolSize=10, symbolBrush=('b'))
		
		
		self.fase_frenado = self.fase_frenado + 1
		if self.fase_frenado>5:
			self.fase_frenado=1
		print(f'Siguiente fase -> Fase {self.fase_frenado}')
		self.label_f_fase.setText(self.fases_frenado[self.fase_frenado-1])
		if self.fase_frenado in (2,4):
			self.label_f_5.show()
			self.label_f_6.show()
			self.label_f_Ti.show()
			self.label_f_t_dr.show()
			
			if self.fase_frenado==2:
				self.label_f_4.setText('Td (°C)')
				self.label_f_6.setText('t (s)')

			if self.fase_frenado==4:
				self.label_f_4.setText('Td (°C)')
				self.label_f_6.setText('dr (m)')
		else:
			self.label_f_5.hide()
			self.label_f_6.hide()
			self.label_f_Ti.hide()
			self.label_f_t_dr.hide()
			self.label_f_4.setText('df (m)')
		
		if self.fase_frenado>=5:
			self.button_f_fase.setText('Finalizar')
		else:
			self.button_f_fase.setText('Siguiente fase')

	@pyqtSlot()
	def reiniciar_fase(self):
		self.fase_frenado = 0
		self.cambiar_fase()

	@pyqtSlot()
	def cambiar_disp_prueba(self):
		if self.combo_prueba.currentIndex()==0:
			self.label_p_4.setText('fp (N)')
			self.label_p_5.setText('δ (°)')
			self.label_p_11.setText('Vr_F (m/s)')
			self.label_p_12.setText('Vr_R (m/s)')
			self.label_p_13.setText('Vr_L (m/s)')
			self.label_p_14.setText('V5_r (m/s)')
			self.label_p_21.setText('Td (°C)')
			self.label_p_22.setText('Ti (°C)')
			self.label_p_23.setText('B1 (kg)')
			self.label_p_24.setText('B2 (kg)')
			self.label_p_31.setText('Sensores')

			self.label_p_6.hide()
			self.label_p_7.hide()
			self.label_p_8.hide()
			self.label_p_9.hide()
			self.label_p_10.hide()
			self.label_p_15.hide()
			self.label_p_16.hide()
			self.label_p_17.hide()
			self.label_p_18.hide()
			self.label_p_19.hide()
			self.label_p_20.hide()
			self.label_p_25.hide()
			self.label_p_26.hide()
			self.label_p_27.hide()
			self.label_p_28.hide()
			self.label_p_29.hide()
			self.label_p_30.hide()
			#self.label_p_31.hide()
			self.label_p_32.hide()
			self.label_p_Gz.hide()
			self.label_p_Mx.hide()
			self.label_p_My.hide()
			self.label_p_Mz.hide()
			self.label_p_T.hide()
			self.label_p_velNNav.hide()
			self.label_p_velUNav.hide()
			self.label_p_LonNav.hide()
			self.label_p_LatNav.hide()
			self.label_p_altNav.hide()
			self.label_p_Hbar.hide()
			self.label_p_velNGPS.hide()
			self.label_p_velUGPS.hide()
			self.label_p_LonGPS.hide()
			self.label_p_LatGPS.hide()
			self.label_p_AltGPS.hide()

		if self.combo_prueba.currentIndex()==1:
			self.label_p_4.setText('Gx (deg/s)')
			self.label_p_5.setText('Gy (deg/s)')
			self.label_p_11.setText('Roll (deg)')
			self.label_p_12.setText('Pitch (deg)')
			self.label_p_13.setText('Yaw (deg)')
			self.label_p_14.setText('Vel_E (m/s)')
			self.label_p_21.setText('Roll (deg)')
			self.label_p_22.setText('Pitch (deg)')
			self.label_p_23.setText('Yaw (deg)')
			self.label_p_24.setText('Vel_E (m/s)')
			self.label_p_31.setText('Navegación')

			self.label_p_6.show()
			self.label_p_7.show()
			self.label_p_8.show()
			self.label_p_9.show()
			self.label_p_10.show()
			self.label_p_15.show()
			self.label_p_16.show()
			self.label_p_17.show()
			self.label_p_18.show()
			self.label_p_19.show()
			self.label_p_20.show()
			self.label_p_25.show()
			self.label_p_26.show()
			self.label_p_27.show()
			self.label_p_28.show()
			self.label_p_29.show()
			self.label_p_30.show()
			#self.label_p_31.show()
			self.label_p_32.show()
			self.label_p_Gz.show()
			self.label_p_Mx.show()
			self.label_p_My.show()
			self.label_p_Mz.show()
			self.label_p_T.show()
			self.label_p_velNNav.show()
			self.label_p_velUNav.show()
			self.label_p_LonNav.show()
			self.label_p_LatNav.show()
			self.label_p_altNav.show()
			self.label_p_Hbar.show()
			self.label_p_velNGPS.show()
			self.label_p_velUGPS.show()
			self.label_p_LonGPS.show()
			self.label_p_LatGPS.show()
			self.label_p_AltGPS.show()

	def start_workers(self):
		# serialPort1 = 'COM8' # Debe revisarse el puerto al que se conecta el GINS
		# serialPort2 = 'COM9' # Debe revisarse el puerto al que se conecta el GINS
		# baudRate = 38400
		
		# self.thread[1] = MSerialPort(serialPort1,baudRate,parent=None,index=1)
		# self.thread[1].start()
		# self.thread[1].data.connect(self.update_labels)
		
		# self.thread[2] = MSerialPort(serialPort2,baudRate,parent=None,index=2)
		# self.thread[2].start()
		# self.thread[2].data.connect(self.update_labels2)
		
		serialPort = 'COM5' # Debe revisarse el puerto al que se conecta el GINS
		baudRate = 460800
		self.thread[1] = Gins(serialPort,baudRate,parent=None,index=1)
		self.thread[1].data.connect(self.update_gins_data)
		self.thread[1].start()
		
		self.thread[2] = CDaq(parent=None,index=2)
		self.thread[2].data.connect(self.update_cdaq_data)
		self.thread[2].start()

	def stop_workers(self):
		self.thread[1].stop()
		self.thread[2].stop()
		#self.pushButton.setEnabled(True)

	# def start_aqcuisiton(self):
		
	# 	self.timer.setInterval(98)
	# 	self.timer.timeout.connect(self.update_plot)
	# 	self.timer.start()

	# 	self.button_start.setEnabled(False)
	# 	self.button_stop.setEnabled(True)
		
		# self.thread[3] = MAcquisiton(parent=None,index=3)
		# self.thread[3].start()
		# self.thread[3].data.connect(self.show_data)
		
		# self.thread[1].data.connect(self.thread[3].update_val1)
		# self.thread[2].data.connect(self.thread[3].update_val2)
		
		#self.pushButton_3.setEnabled(False)
		
	# def stop_aqcuisiton(self):
	# 	self.thread[3].stop()
	# 	self.button_start.setEnabled(True)
	# 	self.button_stop.setEnabled(False)
	
	def pause_resume_aqcuisiton(self):
		self.pause = not self.pause
		if self.pause:
			self.thread[3].pause()
			self.button_pause.setText("Resume")
		else:
			self.thread[3].resume()
			self.button_pause.setText("Pause")
	
	def update_gins_data(self,data):
		self.gins_data = data
	
	def update_cdaq_data(self,data):
		for i,v in data.items():
			self.cdaq_data[i] = v[-1]
			
		
	def update_plot(self):
		#print(f'Print labels: {val}')
		gins = self.gins_data
		cdaq = self.cdaq_data
		self.t += 0.1
		#val = round(self.t,2)] + self.val1 + self.val2
		if self.tabs_pruebas.currentIndex()==0: #Prueba de frenado
			vx = 3.6*sqrt((gins["nav_vel_E"])**2 + (gins["nav_vel_N"])**2 + 
				(gins["nav_vel_U"])**2) #km/h
			if self.fase_frenado in (1,3,5):
				self.label_f_vx.setText(f'{vx}')
				self.label_f_ax.setText(f'{gins["acc_y"]}')
				self.label_f_fp.setText(f'{cdaq["fp"]}')
				
				self.ydata[0] = self.ydata[0][1:]  # Remove the first
				self.ydata[1] = self.ydata[1][1:]  # Remove the first
				self.ydata[2] = self.ydata[2][1:]  # Remove the first

				self.ydata[0].append(vx)
				self.ydata[1].append(gins["acc_y"])
				self.ydata[2].append(cdaq["fp"])
				i = self.combo_f_plot.currentIndex()
				self.line1.setData(self.xdata,self.ydata[i])
			
			elif self.fase_frenado==2:
				self.label_f_vx.setText(f'{vx}')
				self.label_f_ax.setText(f'{gins["acc_y"]}')
				self.label_f_fp.setText(f'{cdaq["fp"]}')
				self.label_f_df_Td.setText(f'{cdaq["Td"]}')
				self.label_f_Ti.setText(f'{cdaq["Ti"]}')
				self.label_f_t_dr.setText(f'{self.t}')
				
				self.ydata[0] = self.ydata[0][1:]  # Remove the first
				self.ydata[1] = self.ydata[1][1:]  # Remove the first
				self.ydata[2] = self.ydata[2][1:]  # Remove the first
				self.ydata[3] = self.ydata[3][1:]  # Remove the first
				self.ydata[4] = self.ydata[4][1:]  # Remove the first
				self.ydata[5] = self.ydata[5][1:]  # Remove the first

				#self.xdata.append(self.t)
				self.ydata[0].append(vx)
				self.ydata[1].append(gins["acc_y"])
				self.ydata[2].append(cdaq["fp"])
				self.ydata[3].append(cdaq["Td"])
				self.ydata[4].append(cdaq["Ti"])
				self.ydata[5].append(self.t)
				i = self.combo_f_plot.currentIndex()
				self.line1.setData(self.xdata,self.ydata[i])
			
			elif self.fase_frenado==4:
				self.label_f_vx.setText(f'{vx}')
				self.label_f_ax.setText(f'{gins["acc_y"]}')
				self.label_f_fp.setText(f'{cdaq["fp"]}')
				self.label_f_df_Td.setText(f'{cdaq["Td"]}')
				self.label_f_Ti.setText(f'{cdaq["Ti"]}')
				#self.label_f_t_dr.setText(f'{self.t}')
				
				self.ydata[0] = self.ydata[0][1:]  # Remove the first
				self.ydata[1] = self.ydata[1][1:]  # Remove the first
				self.ydata[2] = self.ydata[2][1:]  # Remove the first
				self.ydata[3] = self.ydata[3][1:]  # Remove the first
				self.ydata[4] = self.ydata[4][1:]  # Remove the first

				#self.xdata.append(self.t)
				self.ydata[0].append(vx)
				self.ydata[1].append(gins["acc_y"])
				self.ydata[2].append(cdaq["fp"])
				self.ydata[3].append(cdaq["Td"])
				self.ydata[4].append(cdaq["Ti"])
				i = self.combo_f_plot.currentIndex()
				self.line1.setData(self.xdata,self.ydata[i])
			
		if self.tabs_pruebas.currentIndex()==1: #Prueba de estabilidad
			vx = 3.6*sqrt((gins["nav_vel_E"])**2 + (gins["nav_vel_N"])**2 + 
				(gins["nav_vel_U"])**2)
			self.label_e_vx.setText(f'{vx}')
			self.label_e_ay.setText(f'{gins["acc_x"]}') # Aceleración lateral
			self.label_e_delta.setText(f'{cdaq["Vol"]}')
			
			self.ydata[0] = self.ydata[0][1:]  # Remove the first
			self.ydata[1] = self.ydata[1][1:]  # Remove the first
			self.ydata[2] = self.ydata[2][1:]  # Remove the first
			
			self.ydata[0].append(vx)
			self.ydata[1].append(gins["acc_x"])
			self.ydata[2].append(cdaq["Vol"])
			i = self.combo_e_plot.currentIndex()
			self.line2.setData(self.xdata, self.ydata[i])
		
		if self.tabs_pruebas.currentIndex()==2: #Prueba de vibraciones
			self.label_v_ax.setText(f'{round(1*cdaq["AccX"],4)}')
			self.label_v_ay.setText(f'{round(1*cdaq["AccY"],4)}') # Aceleración lateral
			self.label_v_az.setText(f'{round(1*cdaq["AccZ"],4)}')

			self.ydata[0] = self.ydata[0][1:]  # Remove the first
			self.ydata[1] = self.ydata[1][1:]  # Remove the first
			self.ydata[2] = self.ydata[2][1:]  # Remove the first	
			
			self.ydata[0].append(1*cdaq["AccY"])
			self.ydata[1].append(1*cdaq["AccX"])
			self.ydata[2].append(1*cdaq["AccZ"])
			i = self.combo_v_plot.currentIndex()
			self.line3.setData(self.xdata, self.ydata[i])  # Update the data.
		
		if self.tabs_pruebas.currentIndex()==4: #Modo de prueba
			if self.combo_prueba.currentIndex()==0: #cDAQ-9188
				self.label_p_ax.setText(f'{cdaq["AccX"]}')
				self.label_p_ay.setText(f'{cdaq["AccY"]}')
				self.label_p_az.setText(f'{cdaq["AccZ"]}')
				self.label_p_fp_Gx.setText(f'{cdaq["fp"]}')
				self.label_p_d_Gy.setText(f'{cdaq["Vol"]}')
				# self.label_p_Gz.setText()
				# self.label_p_Mx.setText()
				# self.label_p_My.setText()
				# self.label_p_Mz.setText()
				# self.label_p_T.setText()
				self.label_p_vrF_rollNav.setText(f'{cdaq["Rdel"]}')
				self.label_p_vrR_pitchNav.setText(f'{cdaq["Rder"]}')
				self.label_p_vrL_yawNav.setText(f'{cdaq["Rizq"]}')
				self.label_p_v5r_velENav.setText(f'{cdaq["R5a"]}')
				# self.label_p_velNNav.setText()
				# self.label_p_velUNav.setText()
				# self.label_p_LonNav.setText()
				# self.label_p_LatNav.setText()
				# self.label_p_altNav.setText()
				# self.label_p_Hbar.setText()
				self.label_p_Td_rollGPS.setText(f'{cdaq["Td"]}')
				self.label_p_Ti_pitchGPS.setText(f'{cdaq["Ti"]}')
				# self.label_p_B1_yawGPS.setText(f'{cdaq["B1"]}')
				# self.label_p_B2_velEGPS.setText(f'{cdaq["B2"]}')
				# self.label_p_velNGPS.setText()
				# self.label_p_velUGPS.setText()
				# self.label_p_LonGPS.setText()
				# self.label_p_LatGPS.setText()
				# self.label_p_AltGPS.setText()
			else:
				self.label_p_ax.setText(f'{gins["acc_x"]}')
				self.label_p_ay.setText(f'{gins["acc_y"]}')
				self.label_p_az.setText(f'{gins["acc_z"]}')
				self.label_p_fp_Gx.setText(f'{gins["gyro_x"]}')
				self.label_p_d_Gy.setText(f'{gins["gyro_y"]}')
				self.label_p_Gz.setText(f'{gins["gyro_z"]}')
				self.label_p_Mx.setText(f'{gins["magn_x"]}')
				self.label_p_My.setText(f'{gins["magn_y"]}')
				self.label_p_Mz.setText(f'{gins["magn_z"]}')
				self.label_p_T.setText(f'{gins["T"]}')
				self.label_p_vrF_rollNav.setText(f'{gins["nav_roll"]}')
				self.label_p_vrR_pitchNav.setText(f'{gins["nav_pitch"]}')
				self.label_p_vrL_yawNav.setText(f'{gins["nav_yaw"]}')
				self.label_p_v5r_velENav.setText(f'{gins["nav_vel_E"]}')
				self.label_p_velNNav.setText(f'{gins["nav_vel_N"]}')
				self.label_p_velUNav.setText(f'{gins["nav_vel_U"]}')
				self.label_p_LonNav.setText(f'{gins["nav_Lon"]}')
				self.label_p_LatNav.setText(f'{gins["nav_Lat"]}')
				self.label_p_altNav.setText(f'{gins["nav_alt"]}')
				self.label_p_Hbar.setText(f'{gins["h_bar"]}')
				#self.label_p_Td_rollGPS.setText(f'{gins["Td"]}')
				#self.label_p_Ti_pitchGPS.setText(f'{gins["Ti"]}')
				self.label_p_B1_yawGPS.setText(f'{gins["gps_yaw"]}')
				self.label_p_B2_velEGPS.setText(f'{gins["gps_vel_E"]}')
				self.label_p_velNGPS.setText(f'{gins["gps_vel_N"]}')
				self.label_p_velUGPS.setText(f'{gins["gps_vel_U"]}')
				self.label_p_LonGPS.setText(f'{gins["gps_Lon"]}')
				self.label_p_LatGPS.setText(f'{gins["gps_Lat"]}')
				self.label_p_AltGPS.setText(f'{gins["gps_alt"]}')
		# if val[0]>0:
		# 	self.line1.clear()
		# if len(self.xdata)>=15:
		# 	del self.xdata[0]
		# 	del self.ydata[0]
		# self.xdata.append(val[0])
		# self.ydata.append(val[1])
		# self.line1 = self.plot_widget.plot(self.xdata,self.ydata,pen=self.red_pen,symbol='+', symbolSize=20, symbolBrush=('b'))

	def closeEvent(self, event):
		close = QMessageBox.question(self,"SALIR","¿Desea salir del aplicativo?",QMessageBox.Yes | QMessageBox.No)
		if close == QMessageBox.Yes:
			print('Bye!')
			self.stop_workers()
			event.accept()
		else:
			event.ignore()


class Gins(QThread):
	vals = dict()
	message = None
	read_flag = False
	data = pyqtSignal(dict)
	def __init__(self,port,baud,index=0,parent=None):
		super(Gins, self).__init__(parent)
		self.index=index
		self.is_running = True
		self.port=serial.Serial(port,baud,bytesize=serial.EIGHTBITS,
			parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=1) #Para el GINS200
		self.port_open()
	def port_open(self):
		if not self.port.isOpen():
			self.port.open()
	def port_close(self):
		self.port.close()
	def send_data(self,data):
		number=self.port.write(data)
		return number
	def flush(self):
		self.port.flushInput()
		self.port.flushOutput()
	def run(self):
		print("GINS iniciado en hilo ->",self.index)
		while True:
			time.sleep(0.01)
			#t1 = time.time()
			#t1 = datetime.now()
			if not self.is_running:
				break
			out = ''
			while self.port.inWaiting() > 0: 
				out = self.port.read(self.port.inWaiting())#.decode('uint8')
			if out != '':
				self.message = self.get_gins_values(out.hex())
				#t = datetime.now() - t1
				#dt = t.total_seconds()
				#self.message["t_gins"] = dt
				self.data.emit(self.message)
				
			#time.sleep(0.05)
	def stop(self):
		self.is_running = False
		print('GINS finalizado en hilo ->',self.index)
		self.port_close()
		self.terminate()
	def get_gins_values(self,data):
		try:
			#data = str(hex(int(BitArray(in_stream).bin,2)))
			start_data = data.find('aa550364')
			out_stream = data[start_data:start_data+200]
			#print(out_stream)
			
			# Get values from separated bytes
			sens_gyro = 1e-4 #Gyro sens
			sens_acc = 1e-5 #Acc sens
			sens_magn = 1e-2 #Magn sens
			sens_hbar = 1e-2 #Hbar sens
			sens_att = 1e-2 #Att sens
			sens_vel = 1e-4 #Vel sens
			sens_lon_lat = 1e-7 #Lon and Lat sens
			sens_alt = 1e-2 # Alt sens
			sens_T = 1e-2 # Temp sens

			self.vals["gyro_x"] = sens_gyro*float(self.hex2sint(out_stream[8:14],3))
			self.vals["gyro_y"] = sens_gyro*float(self.hex2sint(out_stream[14:20],3))
			self.vals["gyro_z"] = sens_gyro*float(self.hex2sint(out_stream[20:26],3))
			#print(f'[gyro_x,gyro_y,gyro_z]: [{gyro_x},{gyro_y},{gyro_z}]')
			self.vals["acc_x"] = sens_acc*float(self.hex2sint(out_stream[26:32],3))
			self.vals["acc_y"] = sens_acc*float(self.hex2sint(out_stream[32:38],3))
			self.vals["acc_z"] = sens_acc*float(self.hex2sint(out_stream[38:44],3))
			#print(f'[acc_x,acc_y,acc_z]: [{acc_x},{acc_y},{acc_z}]')
			self.vals["magn_x"] = sens_magn*float(self.hex2sint(out_stream[44:48],2))
			self.vals["magn_y"] = sens_magn*float(self.hex2sint(out_stream[48:52],2))
			self.vals["magn_z"] = sens_magn*float(self.hex2sint(out_stream[52:56],2))
			#print(f'[magn_x,magn_y,magn_z]: [{magn_x},{magn_y},{magn_z}]')
			self.vals["h_bar"] = sens_hbar*float(self.hex2sint(out_stream[56:62],3))
						
			self.vals["gps_vel_E"] = sens_vel*float(self.hex2sint(out_stream[80:86],3))
			self.vals["gps_vel_N"] = sens_vel*float(self.hex2sint(out_stream[86:92],3))
			self.vals["gps_vel_U"] = sens_vel*float(self.hex2sint(out_stream[92:98],3))
			
			self.vals["gps_Lon"] = sens_lon_lat*float(self.hex2sint(out_stream[98:106],4))
			self.vals["gps_Lat"] = sens_lon_lat*float(self.hex2sint(out_stream[106:114],4))
			self.vals["gps_alt"] = sens_alt*float(self.hex2sint(out_stream[114:120],3))
			self.vals["gps_yaw"] = sens_att*float(self.hex2sint(out_stream[120:124],2))
			
			self.vals["nav_pitch"] = sens_att*float(self.hex2sint(out_stream[130:134],2))
			self.vals["nav_roll"] = sens_att*float(self.hex2sint(out_stream[134:138],2))
			self.vals["nav_yaw"] = sens_att*float(self.hex2sint(out_stream[138:142],2)) #Unsigned
			#print(f'[pitch,roll,yaw]: [{ang_pitch},{ang_roll},{ang_yaw}]')
			self.vals["nav_vel_E"] = sens_vel*float(self.hex2sint(out_stream[142:148],3))
			self.vals["nav_vel_N"] = sens_vel*float(self.hex2sint(out_stream[148:154],3))
			self.vals["nav_vel_U"] = sens_vel*float(self.hex2sint(out_stream[154:160],3))
			#print(f'[vel_E,vel_N]: [{vel_E},{vel_N}]')
			self.vals["nav_Lon"] = sens_lon_lat*float(self.hex2sint(out_stream[160:168],4))
			self.vals["nav_Lat"] = sens_lon_lat*float(self.hex2sint(out_stream[168:176],4))
			self.vals["nav_alt"] = sens_alt*float(self.hex2sint(out_stream[176:182],3))
			
			self.vals["T"] = sens_T*float(self.hex2sint(out_stream[192:196],2))

			return self.vals # Retorna un diccionario con todas las mediciones
		except Exception as ex:
			#print(ex)
			return self.vals

	def hex2sint(self,val,num_bytes):
		if num_bytes==4:	# Dato de 4 bytes / 32 bits
			bin_data = "{0:032b}".format(int(val, 16))
		elif num_bytes==3:	# Dato de 3 bytes / 24 bits
			bin_data = "{0:024b}".format(int(val, 16))
		elif num_bytes==2:	# Dato de 2 bytes / 16 bits
			bin_data = "{0:016b}".format(int(val, 16))
		return BitArray(bin=bin_data).int

	#def hex2uint(self,val,num_bytes):
	#	return int(val,8*num_bytes)


class CDaq(QThread):
	global start
	#callback_chasis = False
	task1 = None
	task2 = None
	task3 = None
	data = pyqtSignal(dict)
	datos = {}
	read_flag = False
	devC = nidaqmx.system.device.Device('cDAQ9188')
	devC.reserve_network_device(True)
	min_V = -10
	max_V = 10
	#data_task1=np.zeros((1, 1200))
	#data_task2=np.zeros((7, 1200))
	#data_task3=np.zeros((3, 1200))
	db_Name = "pruebaDB_cDAQ_Prueba.db"
	db_Table = "Variables_cDAQ1"
	
	def __init__(self,index=0,parent=None):
		super(CDaq, self).__init__(parent)		

		self.index=index
		self.is_running = True
		self.task1 = nidaqmx.Task() 
		self.task2 = nidaqmx.Task()
		self.task3 = nidaqmx.Task()
		
		#Config módulo 7
		self.task1.ai_channels.add_ai_bridge_chan("cDAQ9188Mod7/ai0",name_to_assign_to_channel='c7_0',
			bridge_config=nidaqmx.constants.BridgeConfiguration.FULL_BRIDGE,
			nominal_bridge_resistance=700.0)	#Pedal
		#print(c7_0)
		#print(c7_0.ai_meas_type)
		#Config módulo 2
		self.task2.ai_channels.add_ai_voltage_chan("cDAQ9188Mod2/ai0",name_to_assign_to_channel='c2_0',
			min_val=self.min_V,max_val=self.max_V)	#Temp der
		#print(c2_0)
		#c2_0.ai_meas_type = nidaqmx.constants.UsageTypeAI.VOLTAGE
		self.task2.ai_channels.add_ai_voltage_chan("cDAQ9188Mod2/ai1",name_to_assign_to_channel='c2_1',
			min_val=self.min_V,max_val=self.max_V)	#Temp izq
		#print(c2_1)
		#c2_1.ai_meas_type = nidaqmx.constants.UsageTypeAI.VOLTAGE
		self.task2.ai_channels.add_ai_voltage_chan("cDAQ9188Mod2/ai2",min_val=self.min_V,max_val=self.max_V)	#Rueda delantera
		
		#Config módulo 3
		self.task2.ai_channels.add_ai_voltage_chan("cDAQ9188Mod3/ai0",min_val=self.min_V,max_val=self.max_V)	#5ta rueda
		self.task2.ai_channels.add_ai_voltage_chan("cDAQ9188Mod3/ai1",min_val=self.min_V,max_val=self.max_V)	#Rueda izq
		self.task2.ai_channels.add_ai_voltage_chan("cDAQ9188Mod3/ai2",min_val=self.min_V,max_val=self.max_V)	#Rueda der
		self.task2.ai_channels.add_ai_voltage_chan("cDAQ9188Mod3/ai3",min_val=self.min_V,max_val=self.max_V)	#Volante
		
		#Config módulo 8
		#sensX=99.07e-3	#mV/g	10.10e-3; %V/ms-2  
		#sensY=97.08e-3	#mV/g	9.89e-3; %V/ms-2   
		#sensZ=101.7e-3	#mV/g	10.38e-3; %V/ms-2 
		sensX=99.07e-3	#V/g
		sensY=97.08e-3	#V/g
		sensZ=101.7e-3	#V/g
		self.task3.ai_channels.add_ai_accel_chan("cDAQ9188Mod8/ai0",
			units=nidaqmx.constants.AccelUnits.METERS_PER_SECOND_SQUARED, 
			sensitivity=sensX, sensitivity_units=nidaqmx.constants.AccelSensitivityUnits.VOLTS_PER_G)	#Acc x
		self.task3.ai_channels.add_ai_accel_chan("cDAQ9188Mod8/ai1",
			units=nidaqmx.constants.AccelUnits.METERS_PER_SECOND_SQUARED, 
			sensitivity=sensY, sensitivity_units=nidaqmx.constants.AccelSensitivityUnits.VOLTS_PER_G)	#Acc y
		self.task3.ai_channels.add_ai_accel_chan("cDAQ9188Mod8/ai2",
			units=nidaqmx.constants.AccelUnits.METERS_PER_SECOND_SQUARED, 
			sensitivity=sensZ, sensitivity_units=nidaqmx.constants.AccelSensitivityUnits.VOLTS_PER_G)	#Acc z
		
		bufsize_callback=1200
		self.task1.timing.cfg_samp_clk_timing(rate=12000,sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS, samps_per_chan=144000)
		self.task2.timing.cfg_samp_clk_timing(rate=12000,sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS, samps_per_chan=144000)
		self.task3.timing.cfg_samp_clk_timing(rate=12000,sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS, samps_per_chan=144000)
		
		self.readertask1 = stream_readers.AnalogMultiChannelReader(self.task1.in_stream)
		self.readertask2 = stream_readers.AnalogMultiChannelReader(self.task2.in_stream)
		self.readertask3 = stream_readers.AnalogMultiChannelReader(self.task3.in_stream)
		
		self.task1.register_every_n_samples_acquired_into_buffer_event(bufsize_callback,
                                                            self.reading_task1_callback)
		self.task2.register_every_n_samples_acquired_into_buffer_event(bufsize_callback,
                                                            self.reading_task2_callback)
		self.task3.register_every_n_samples_acquired_into_buffer_event(bufsize_callback,
                                                            self.reading_task3_callback)
		
		self.task1.start()
		self.task2.start()
		self.task3.start()

	def task_close(self):
		self.task1.close()
		self.task2.close()
		self.task3.close()

	def list2dict(self):
		res = dict() #'[fp,Td,Ti,Rdel,5aR,Rder,Rizq,Vol,AccX,AccY,AccZ]'
		res["fp"] = self.data_task1[0,:]
		res["Td"] = self.data_task2[0,:]
		res["Ti"] = self.data_task2[1,:]
		res["Rdel"] = self.data_task2[2,:]
		res["R5a"] = self.data_task2[3,:]
		res["Rder"] = self.data_task2[4,:]
		res["Rizq"] = self.data_task2[5,:]
		res["Vol"] = self.data_task2[6,:]
		res["AccX"] = self.data_task3[0,:]
		res["AccY"] = self.data_task3[1,:]
		res["AccZ"] = self.data_task3[2,:]	
		return res

	def reading_task1_callback(self, task_idx, event_type, num_samples, callback_data):
		buffertask1 = np.zeros((1, num_samples))
		self.readertask1.read_many_sample(buffertask1, num_samples,
                                   timeout=constants.WAIT_INFINITELY)
		# Convert the data from channel as a row order to channel as a column
		self.data_task1 = buffertask1
		#print('Datos='+str(self.data_task1)+' Tamano buffer='+str(len(self.data_task1[0])))
		
		return 0
		
	def reading_task2_callback(self,task_idx, event_type, num_samples, callback_data):
		buffertask2 = np.zeros((7, num_samples))
		self.readertask2.read_many_sample(buffertask2, num_samples,
                                   timeout=constants.WAIT_INFINITELY)
		# Convert the data from channel as a row order to channel as a column
		self.data_task2 = buffertask2
		return 0

	def reading_task3_callback(self,task_idx, event_type, num_samples, callback_data):
		
		buffertask3 = np.zeros((3, num_samples))
		self.readertask3.read_many_sample(buffertask3, num_samples,
                                   timeout=constants.WAIT_INFINITELY)
		# Convert the data from channel as a row order to channel as a column
		self.data_task3 = buffertask3
		self.datos=self.list2dict()
		#self.callback_chasis=True
		return 0
		
	def run(self):
		print("Tarea cDAQ iniciada en hilo ->",self.index)
		while True:
			if not self.is_running:
				break
			#if self.callback_chasis==True:
				#print(self.callback_chasis)
			if start:
				self.d2db = Dict2Db(self.db_Table,self.db_Name)
				self.d2db.insert2db(self.datos)
			self.data.emit(self.datos)
			self.callback_chasis=False			
			
	def stop(self):
		self.is_running = False
		print("Tarea cDAQ terminada en hilo ->",self.index)
		self.task_close()
		self.terminate()


class Dict2Db():
	list_indexes = []
	list_values = []
	create_table_str = ''
	db_conn = None
	def __init__(self,db_table,db_name):
		super(Dict2Db, self).__init__()
		self.db_table = db_table
		self.db_name = db_name
		self.db_conn = sqlite3.connect("PVE-Python/database/" + self.db_name, check_same_thread=False)
		self.cursor = self.db_conn.cursor()
		self.create_table_str = "CREATE TABLE IF NOT EXISTS " + self.db_table + " (t REAL AUTO_INCREMENT, "

	def dict2tup(self,data):
		create_table_str = self.create_table_str
		dict_keys = list(data.keys())
		dict_values = list(data.values())
		for indx in dict_keys:
			create_table_str += indx + " REAL NOT NULL, "
		create_table_str += "PRIMARY KEY (t))" 

		return tuple(dict_keys),tuple(dict_values),create_table_str
	
	def dict2tuplist(self,data):
		create_table_str = self.create_table_str
		dict_keys = list(data.keys())
		dict_values = list(data.values())
		for indx in dict_keys:
			create_table_str += indx + " REAL NOT NULL, "
		create_table_str += "PRIMARY KEY (t))" 
		# print(f'k_data = {dict_keys}')
		tup_list = []
		for i in range(len(dict_values[0])):
			tup = []
			for k in dict_values:
				tup.append(k[i])
			tup_list.append(tuple(tup))
		return tuple(dict_keys),tup_list,create_table_str

	def insert2db(self,data):
		if isinstance(list(data.values())[0],np.ndarray):
			tup_keys,list_values,create_table_str = self.dict2tuplist(data)
			#tup_keys,tup_values,create_table_str = self.dict2tup(data)
			#print(f'tup_values = {tup_values}')
			#print(f'tup_keys = {tup_keys}')
			#print(f'list_values = {list_values}')
			try:
				#cursor.execute("CREATE TABLE IF NOT EXISTS " + db_Table + " (t REAL NOT NULL, Dist REAL NOT NULL, Fp REAL NOT NULL, Vx REAL NOT NULL, Vy REAL NOT NULL, Vz REAL NOT NULL, Ax REAL NOT NULL, Ay REAL NOT NULL, Az REAL NOT NULL, Ti REAL NOT NULL, Td REAL NOT NULL, PRIMARY KEY (t))")
				self.cursor.execute(create_table_str)
				#cursor.execute("INSERT INTO " + db_Table + "(t, Dist, Fp, Vx, Vy, Vz, Ax, Ay, Az, Ti, Td) VALUES(?,?,?,?,?,?,?,?,?,?,?)",tuple(data))
				#self.cursor.execute(f"\n\nINSERT INTO {self.db_table} {tuple(list_indexes)} VALUES {str(tuple(list_values))}")
				#values = ', '.join(map(str, list_values))
				sql = "INSERT INTO " + self.db_table + " " + str(tup_keys) + " VALUES ("
				for i in range(len(tup_keys)):
					if i==0:
						sql += "?"
					else:
						sql += ",?"
				sql += ")"
				print(f'sql = {sql}')
				#self.cursor.execute(f"\n\nINSERT INTO {self.db_table} {tup_keys} VALUES {str(tup_values)}")
				self.cursor.executemany(sql,list_values)
				self.db_conn.commit()
			except Exception as ex:
				print(ex)
		else:
			tup_keys,tup_values,create_table_str = self.dict2tup(data)
			#print(f'tup_values = {tup_values}')
			try:
				#cursor.execute("CREATE TABLE IF NOT EXISTS " + db_Table + " (t REAL NOT NULL, Dist REAL NOT NULL, Fp REAL NOT NULL, Vx REAL NOT NULL, Vy REAL NOT NULL, Vz REAL NOT NULL, Ax REAL NOT NULL, Ay REAL NOT NULL, Az REAL NOT NULL, Ti REAL NOT NULL, Td REAL NOT NULL, PRIMARY KEY (t))")
				self.cursor.execute(create_table_str)
				#cursor.execute("INSERT INTO " + db_Table + "(t, Dist, Fp, Vx, Vy, Vz, Ax, Ay, Az, Ti, Td) VALUES(?,?,?,?,?,?,?,?,?,?,?)",tuple(data))
				#self.cursor.execute(f"\n\nINSERT INTO {self.db_table} {tuple(list_indexes)} VALUES {str(tuple(list_values))}")
				self.cursor.execute(f"\n\nINSERT INTO {self.db_table} {tup_keys} VALUES {str(tup_values)}")
				self.db_conn.commit()
			except Exception as ex:
				print(ex)


if __name__ == '__main__':
	import sys
	app = QApplication(sys.argv)
	win = UI()
	win.show()
	sys.exit(app.exec())