import serial
from PyQt5.QtCore import QThread, pyqtSignal
from bitstring import BitArray
import time

class Gins(QThread):
	vals = dict()
	message = None
	read_flag = False
	data = pyqtSignal(dict)
	def __init__(self,port,baud,index=0,parent=None):
		super(Gins, self).__init__(parent)
		self.index=index
		self.is_running = True
		self.is_paused = False
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
			
			self.vals["Temp"] = sens_T*float(self.hex2sint(out_stream[192:196],2))

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
		elif num_bytes==1:	# Dato de 2 bytes / 16 bits
			bin_data = "{0:008b}".format(int(val, 16))
		return BitArray(bin=bin_data).int

	#def hex2uint(self,val,num_bytes): 
	#	return int(val,8*num_bytes)		# <---------- Revisar

	def run(self):
		print("GINS iniciado en hilo ->",self.index)
		while True:
			time.sleep(0.01)
			#t1 = time.time()
			#t1 = datetime.now()
			if self.is_paused:
				continue
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

	def pause(self):
		self.is_paused = True
		print(f'Tarea pausada en hilo {self.index}')

	def resume(self):
		self.is_paused = False
		print(f'Tarea continuada en hilo {self.index}')

			#time.sleep(0.05)
	def stop(self):
		self.is_running = False
		print('GINS finalizado en hilo ->',self.index)
		self.port_close()
		self.terminate()
	
class Do_every(QThread):
	Muestreo_Time = pyqtSignal(float)
	def __init__(self, period):
		QThread.__init__(self)
		self.period = period
		
	def run(self):
		self.ThreadActive=True
		g = self.g_tick()
		print("Empezando...")
		while self.ThreadActive:
			self.start=time.time()
			time.sleep(next(g))
			self.Muestreo_Time.emit(time.time()-self.start)

	def g_tick(self):
		t = time.time()
		while self.ThreadActive:
			t += self.period
			yield max(t - time.time(),0)
				
	def stop(self):
		self.ThreadActive = False
		self.quit()
