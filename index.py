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

@app.route('/home')
def home(): #home page do pygarden
	if not session.get('logged_in'):
		return render_template('login.html')
	else:
		return render_template('index.html', img=(v1.img_link , v2.img_link , v3.img_link), sensor=dht.read())
	
@app.route('/valve/<valvula>')
def change_state(valvula): #reexibe a homepage do pygarden, mas atualiza as valvulas
	if valvula == 'v1':
		v1.change_state()
		return v1.genJson('imgv1')
	elif valvula == 'v2':
		v2.change_state()
		return v2.genJson('imgv2')
	elif valvula == 'v3':
		v3.change_state()
		return v3.genJson('imgv3')		
	return Response('valve not found')


@app.route('/stream')
def stream():
	if not session.get('logged_in'):
		return render_template('login.html')
	return render_template('stream.html')
	
#@app.route('/video_feed') # stream desabilitado por hora
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
					
@app.route('/timer')
def temp():
	return jsonify({
		'temperatura':dht.temp,
		'umidade':dht.umid,
		'img_links': [v1.img_link, v2.img_link, v3.img_link]
		})
		
@app.route('/')
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
		#starta comunicação com a database
		database = dataBase('pygarden.db')
		#leitura incial dos sensores
		read = read_sensor(sensores)
		print('leitura inicial ok')
		contador = 0
		while True:
			init = time.time()
			leitura = read_sensor(sensores)
			read = np.concatenate((read , leitura), axis=0)
			if contador >= 2:
				#grava os dados dos sensores a cada 1 minuto e bate uma foto
				print('Burning')				
				read = np.mean(read, axis=0)
				read = np.around(read, decimals=3)
				database.burn(read)
				read = read_sensor(sensores)
				contador = 0 
			print('Run current Task')			
			time.sleep(2)
			contador += 1
	thread = threading.Thread(target=run_job)
	thread.start()
	


if __name__ == '__main__':
#	inicialização das classes usadas para manipular os sensores	
	board_init()
	dht = dht(4)
	v1, v2, v3 = valve(17), valve(27), valve(22) #irrigação
	s1, s2, s3 = hygrometer(1), hygrometer(2), hygrometer(3) #higrometro
	sensores = [v1,v2,v3,s1,s2,s3,dht] #lista com os objetos dos sensores
#	cam  = VideoCamera() # camera
	app.secret_key = os.urandom(12)
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', debug=True)
