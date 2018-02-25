# Creditos pela parte do stream: http://blog.miguelgrinberg.com/post/video-streaming-with-flask
from flask import Flask , request, render_template , Response ,jsonify, redirect, url_for, flash, request, session, abort
import os
import threading
from hardware import *
from camera import *
import sqlite3
from datetime import datetime
import time
import numpy as np
import json
app = Flask(__name__)


@app.route('/')
@app.route('/home')
def home(): #home page do pygarden
	database = dataBase('pygarden.db')
	charts = database.info_charts()
	database.close()
	return render_template('dash.html', title='PyGARDEN-Dashboard',
			header=('Dashboard - Acompanhe em tempo real'),
			sensores={
				'umid':dht.read()[1],
				'temp':dht.read()[0],
				'img':v1.img_link,
				'hygro': s1.read()
				},
			date = charts[1],
			hygro = charts[2],
			temp = charts[3],
			umid = charts[4]
			)
	

@app.route('/valve/<valvula>')
def change_state(valvula): #reexibe a homepage do pygarden, mas atualiza as valvulas
	if valvula == 'v1':
		v1.change_state()
		return v1.genJson('pump')
	else:
		return 'valve not found'


@app.route('/stream')
def stream():
	return render_template('stream.html')
	

#@app.route('/video_feed') # stream desabilitado por hora
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
					

@app.route('/timer')
def temp():
	return jsonify({
		'temperatura': dht.read()[0],
		'umidade': dht.read()[1],
		'src': v1.img_link,
		'hygro': s1.read(),
		'labels':[0,1,2,3,4,5,6,7,8,9,10],
		'data': [0,1,2,3,4,5,6,7,8,9,10]
		})
		

def index():
	return redirect(url_for('home'))


@app.route('/login', methods=['POST'])
def do_admin_login():
#	time.sleep(2)
	if request.form['password'] == 'admim' and request.form['username'] == 'admim':
		session['logged_in'] = True
#		time.sleep(3)
	else:
#		time.sleep(3)
		flash('wrong password')
	return redirect(url_for('home'))

	
@app.before_first_request
def activate_job():
	def run_job(): 
		while True:
			database = dataBase('pygarden.db')
			leitura = read_sensor(sensores)
			database.burn(leitura)
			print('burned')
			time.sleep(600)
			database.close()
	thread = threading.Thread(target=run_job)
	thread.start()
	

@app.route('/login_screen')
def login():
	return render_template('login.html')


@app.route('/info_charts')	
def charts():
	return jsonify({
		'labels':[0,1,2,3,4,5,6,7,8,9,10],
		'data': [0,1,2,3,4,5,6,7,8,9,10]
		})


if __name__ == '__main__':
#	inicialização das classes usadas para simular os sensores	
	dht = dht(4)
	v1 = valve(17) #irrigação
	s1 = hygrometer(1) #higrometro
	sensores = [s1,dht] #lista com os objetos dos sensores
#	cam  = VideoCamera() # camera
	app.secret_key = os.urandom(12)
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port, debug=True)
