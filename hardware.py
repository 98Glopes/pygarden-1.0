#import RPi.GPIO as gpio
'''
GPIO -> Hardware
setup -> BOARD

7 - dht11
11 - v1
13 - v2
15 - v3
'''

class valve(object):
	
	def __init__(self, io):
		self.io = io
		self.state = False
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
		
#		if self.state == True:
#			gpio.output(self.io , gpio.LOW)
#		else:
#			gpio.output(self.io , gpio.HIGH)
		
class dht(object):
	
	def __init__(self, io):
		self.io = io
		self.temp = 0
		self.umid = 0
	
	@property
	def temperatura(self):
		return '{}ºC'.format(self.temp)
	
	@property
	def umidade(self):
		return '{}%'.format(self.umid)
		
	def read(self):
#	'''
#	Le os valores do sensor e retorna pras variaveis self.temp e self.umid
#		'''
		pass
		
def board_init():
#	gpio.setmode(gpio.BOARD)
	return 'Ok'
