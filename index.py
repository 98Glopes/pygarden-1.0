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
	
@app.route('/video_feed') # stream desabilitado por hora
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
		conn = sqlite3.connect('pygarden.db')
		curso = conn.cursor()
		contador = 0
		#leitura incial dos sensores
		s1.read()
		s2.read()
		s3.read()
		dht.read()
		sensores = np.array([[s1.ground, s2.ground, s3.ground,
								dht.umid, dht.temp]])
		print('leitura inicial ok')
		while True:
#			httpAdress = str(input('Dominio do app: '))
			init = time.time()
			#leitura dos sensore
			s1.read()
			s2.read()
			s3.read()
			dht.read()
			leituras = np.array([[s1.ground, s2.ground, s3.ground,
								dht.umid, dht.temp]])
			if contador >= 100:
				#grava os dados dos sensores a cada 1 minuto e bate uma foto
				print('Burning')
				print(dht.read())
				contador = 0 
			contador += 1
			print('Run current Task')
			time.sleep(4)
	thread = threading.Thread(target=run_job)
	thread.start()



if __name__ == '__main__':
#	inicialização das classes usadas para manipular os sensores	
	board_init()
	dht = dht(4)
	v1, v2, v3 = valve(17), valve(27), valve(22) #irrigação
	s1, s2, s3 = hygrometer(1), hygrometer(2), hygrometer(3) #higrometro
#	cam  = VideoCamera() # camera
	app.secret_key = os.urandom(12)
	app.run(debug=True)
