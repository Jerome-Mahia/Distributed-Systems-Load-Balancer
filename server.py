from flask import Flask, jsonify

import os

app = Flask(__name__)

server_id = os.getenv('SERVER_ID', 'Unknown')

@app.route('/home', methods=['GET'])
def home():
	#Implement logic to reture a unique identifier for the server
	# return f"Hello from Server: [ID]"
	
	#Return a response with the server ID
	response = {
	"message": f"Hello from Server: {server_id}",
	"status": "successful"
	}
	return jsonify(response), 200
	

@app.route('/heartbeat', methods=['GET'])
def heartbeat():
	#Implement logic to handle heartbeat requests
	return '', 200
	
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)
