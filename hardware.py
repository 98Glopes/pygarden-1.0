#import RPi.GPIO as gpio
#import Adafruit_DHT
from flask import jsonify
import numpy as np
from random import randint
import sqlite3
from index import *

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
		
	def read(self):
		return self.state
		

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
		self.umid , self.temp = randint(30,80) , randint(20,35)
		return [self.temp , self.umid]
		

class hygrometer(object):
	
	def __init__(self, io):
		self.io = io
		self.ground = 0
	
	def read(self):
		self.ground = randint(0,99)
		return self.ground

		
def board_init():
#	gpio.setmode(gpio.BOARD)
	return 'Ok'
	
# fun??o timer, le a cada 10s o estado dos sensores e a cada 10min grava no db (pelo menos ? pra fazer isso)
# inutiliza o arquivo time.py	

def read_sensor(obj):
	values =[]
	for x in obj:
		try:
			values = values + x.read()
		except Exception:
			values.append(x.read())
	return(np.array([[values]]))

	
class dataBase(object):
	
	def __init__(self, database):
		try:
			self.conn = sqlite3.connect(database)
		except Exception:
			return 'N?o foi possivel se conectar ao database'		
		self.cursor = self.conn.cursor()
	
	def burn(self, read):
		v1, v2, v3 = read[0][0], read[0][1], read[0][2]
		s1, s2, s3 = read[0][3], read[0][4], read[0][5]
		temp, umid = read[0][6], read[0][7]
		self.cursor.execute( """
		INSERT INTO pygarden (v1, v2, v3, s1, s2, s3, temp, umid)
		VALUES(?, ?, ?, ?, ?, ?, ?, ?)
		""" , (v1, v2, v3, s1, s2, s3, temp, umid))
		self.conn.commit()

	
if __name__ ==	 '__main__':
	obj =[]
	v1, v2, v3 = valve(17), valve(27), valve(22) #irriga??o
	s1, s2, s3 = hygrometer(1), hygrometer(2), hygrometer(3) #higrometro
	dht = dht(9)
	sensores = [v1,v2,v3,s1,s2,s3,dht]
	
	array = read_sensor(sensores)
	
	print (array)
	

	
		
