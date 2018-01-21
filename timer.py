import time
import requests
import json


if __name__ == '__main__':
	send = {
		'dia':'21/01/18',
		'hora':'15:40'
		}
	while True:
		try:
			r = requests.get('http://127.0.0.1:5000/v1')
			print('200')
		except Exception as e:
			print('error')
		time.sleep(10)
		
	
		