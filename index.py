# Creditos pela parte do stream: http://blog.miguelgrinberg.com/post/video-streaming-with-flask
from flask import Flask , request, render_template , Response
import requests
from hardware import *
from camera import *
import traceback

board_init()
dht = dht(4)
v1 = valve(17)
v2 = valve(27)
v3 = valve(22)

	
app = Flask(__name__)



@app.route('/')
def home(): #home page do pygarden
	sensores = [dht.temperatura , dht.umidade]
	img = [v1.img_link , v2.img_link , v3.img_link]
	return render_template('index.html' , sensores=sensores , img=img)
	
@app.route('/<valvula>')
def change_state(valvula): #reexibe a homepage do pygarden, mas atualiza as valvulas
	if valvula == 'v1':
		v1.change_state()
	elif valvula == 'v2':
		v2.change_state()
	elif valvula == 'v3':
		v3.change_state()

	sensores = [dht.temperatura , dht.umidade]
	img = [v1.img_link , v2.img_link , v3.img_link]
	return render_template('index.html' , sensores=sensores , img=img)

@app.route('/stream')
def stream():
	return render_template('stream.html')
	
@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

	
@app.route('/valv' , methods=['GET' , 'POST'])
def valv():
	v1.change_state()
	return 'ok'

@app.route('/img')
def img_viewer():
	return Response(v1.img_link)

if __name__ == '__main__':
    app.run(debug=True)
