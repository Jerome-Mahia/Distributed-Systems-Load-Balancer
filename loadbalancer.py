from flask import Flask, request, jsonify
from Consistenthashing import ConsistentHashMap  # Import ConsistentHashMap class from Consistenthashing.py

app = Flask(__name__)

# Initialize a ConsistentHashMap instance with the specified parameters
consistent_hash_map = ConsistentHashMap(num_containers=3, num_slots=512, num_virtual_servers=9)

# List of server replicas managed by the load balancer
server_replicas = ["Server1", "Server2", "Server3"]

# Add server containers to the consistent hash map
for i in range(len(server_replicas)):
    consistent_hash_map.add_server_container(i)  # Pass integer identifiers for the server containers

# Endpoint to get the status of the replicas
@app.route('/rep', methods=['GET'])
def get_replica_status():
    replicas = [container_id for container_id in server_replicas]
    response = {
        "message": {
            "N": len(replicas),
            "replicas": replicas
        },
        "status": "successful"
    }
    return jsonify(response), 200

# Endpoint to handle client requests and perform load balancing using consistent hashing
@app.route('/request/<request_id>', methods=['GET'])
def handle_request(request_id):
    # Use consistent hashing to determine the server replica for the given request ID
    selected_replica = consistent_hash_map.get_server_container(request_id)
    response = {
        "message": f"Request with ID {request_id} routed to {selected_replica}",
        "status": "successful"
    }
    return jsonify(response), 200
    

@app.route('/add', methods=['POST'])
def add_server_instances():
    # Parse JSON payload from the POST request
    request_data = request.get_json()
    num_instances = request_data.get('n')
    hostnames = request_data.get('hostnames')

    # Perform sanity checks on the request payload
    if num_instances is None or hostnames is None:
        return jsonify({"message": "Invalid request payload", "status": "failure"}), 400
        
    if len(hostnames) > num_instances:
        return jsonify({"message": "Length of hostname list is more than newly added instances", "status": "failure"}), 400


    # Add the new server instances to the load balancer
    for hostname in hostnames:
        consistent_hash_map.add_server_container(hostname)

    # Construct response JSON
    response = {
        "message": {
            "N": len(consistent_hash_map.hash_map),
            "replicas": [replica for replicas in consistent_hash_map.hash_map for replica in replicas]
        },
        "status": "successful"
    }

    return jsonify(response), 200
    
    
@app.route('/rm', methods=['DELETE'])
def remove_server_instances():
    # Parse JSON payload from the DELETE request
    request_data = request.get_json()
    num_instances = request_data.get('n')
    hostnames = request_data.get('hostnames')

    # Perform sanity checks on the request payload
    if num_instances is None or hostnames is None:
        return jsonify({"message": "Invalid request payload", "status": "failure"}), 400

    # Check if the number of hostnames is less than or equal to the number of instances to be removed
    if len(hostnames) > num_instances:
        return jsonify({"message": "Length of hostname list is more than removable instances", "status": "failure"}), 400

    # Remove the specified server instances from the load balancer
    for hostname in hostnames:
        consistent_hash_map.remove_server_container(hostname)

    # Construct response JSON
    response = {
        "message": {
            "N": len(consistent_hash_map.hash_map),
            "replicas": [replica for replicas in consistent_hash_map.hash_map for replica in replicas]
        },
        "status": "successful"
    }

    return jsonify(response), 200


@app.route('/<path>', methods=['GET'])
	def route_request(path):
	# Check if the requested path is registered with any of the server replicas
	# If not, return a failure response
	for replica_url in server_replicas:
	try:
	response = requests.get(f"{replica_url}/{path}")
	if response.status_code == 200:
	# If successful response received from a server replica, return it
	return response.text, response.status_code
	except requests.exceptions.RequestException as e:
	# Handle any exceptions (e.g., connection errors) and continue to the next replica
	print(f"Error connecting to {replica_url}: {e}")
	# If the requested path is not registered with any server replica, return a failure response
response = {
    "message": f"'{path}' endpoint does not exist in server replicas",
    "status": "failure"
}
return jsonify(response), 400


if __name__ == '__main__':
    app.run(debug=True)

