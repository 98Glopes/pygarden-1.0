# Creditos pela parte do stream: http://blog.miguelgrinberg.com/post/video-streaming-with-flask
from flask import Flask , request, render_template , Response ,jsonify
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
def home(): #home page do pygarden
	sensores = [dht.temperatura , dht.umidade]
	img = [v1.img_link , v2.img_link , v3.img_link]
	return render_template('index.html' , sensores=sensores , img=img)
	
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
	return render_template('stream.html')
	
@app.route('/video_feed') # stream desabilitado por hora
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
					

@app.before_first_request
def activate_job():
	def run_job(): 
	#starta comunicação com a database
		conn = sqlite3.connect('pygarden.db')
		curso = conn.cursor()
		#leitura incial dos sensores
		s1.read()
		s2.read()
		s3.read()
		dht.read()
		sensores = np.array([[s1.ground, s2.ground, s3.ground,
								dht.umid, dht.temp]])
		print('leitura inicial ok')
		while True:
			init = time.time()
			#leitura dos sensore
			s1.read()
			s2.read()
			s3.read()
			dht.read()
			leituras = np.array([[s1.ground, s2.ground, s3.ground,
								dht.umid, dht.temp]])
			if ((time.time() - init) > 60):
				#grava os dados dos sensores a cada 1 minuto e bate uma foto
				pass
			print('Run current Task')
			time.sleep(10)
	thread = threading.Thread(target=run_job)
	thread.start()



if __name__ == '__main__':
#	inicialização das classes usadas para manipular os sensores	
	board_init()
	dht = dht(4)
	v1, v2, v3 = valve(17), valve(27), valve(22) #irrigação
	s1, s2, s3 = hygrometer(1), hygrometer(2), hygrometer(3) #higrometro
#	cam  = VideoCamera() # camera
	app.run(debug=True)
