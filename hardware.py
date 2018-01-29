#import RPi.GPIO as gpio
#import Adafruit_DHT
from flask import jsonify


'''
GPIO -> Hardware
setup -> BOARD

4 - dht11
17 - v1
27 - v2
22 - v3
'''

class valve(object):
	
	def __init__(self, io):
		self.io = io
		self.state = False
		self.id = id
#		gpio.setup(self.io , gpio.OUT) #configura o pino como sa?da
		
	@property
	def img_link(self):
		if self.state == False:
			return '../static/img/pump_off.png'
		else:
			return '../static/img/pump_on.png'
			
	def change_state(self):
		if self.state == True:
			self.state = False
		else:
			self.state = True
		'''
			a partir daqui ele manipula as GPIO do RPi//os pinos funcionam com logica invertida			
		'''
		'''
		if self.state == True:
			gpio.output(self.io , gpio.LOW)
		else:
			gpio.output(self.io , gpio.HIGH)
		'''
	def genJson(self , id):
		return jsonify(
		{
			'valveId':id,
			'newSrc':self.img_link
		})
class dht(object):
	
	def __init__(self, io):
		self.io = io
		self.temp = 0
		self.umid = 0
#		self.sensor = Adafruit_DHT.DHT11
	
	@property
	def temperatura(self):
		return '{}ºC'.format(self.temp)
	
	@property
	def umidade(self):
		return '{}%'.format(self.umid)
		
	def read(self):
#		try:
#			self.umid, self.temp = Adafruit_DHT.read_retry(self.sensor, self.io)
#		except Exeception:
#			self.umid , self.temp = 404, 404
		pass
		
class hygrometer(object):
	
	def __init__(self, io):
		self.io = io
		self.ground = 0
	
	def read(self):
		self.ground = 0

		
def board_init():
#	gpio.setmode(gpio.BOARD)
	return 'Ok'
	
# fun??o timer, le a cada 10s o estado dos sensores e a cada 10min grava no db (pelo menos ? pra fazer isso)
# inutiliza o arquivo time.py	

		
