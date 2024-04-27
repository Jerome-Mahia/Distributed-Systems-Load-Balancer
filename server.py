from flask import Flask, jsonify, request
import random

app = Flask(__name__)

# Define the number of server containers managed by the load balancer
NUM_SERVER_CONTAINERS = 3

# Total number of slots in the consistent hash map
NUM_SLOTS = 512

# Number of virtual servers for each server container
K = int(NUM_SLOTS / NUM_SERVER_CONTAINERS)

# List to store server replicas
server_replicas = ["Server 1", "Server 2", "Server 3"]

# Hash function for request mapping
def hash_request(request_path):
    return hash(request_path) % (NUM_SLOTS * 2)

# Hash function for virtual server mapping
def hash_virtual_server(server_id, j):
    return (hash(server_id) + j + 2 * j + 25) % (NUM_SLOTS * 2)

# Consistent Hashing Implementation
class ConsistentHashing:
    def __init__(self):
        self.servers = []

    def add_server(self, server_id):
        for j in range(K):
            virtual_server_id = hash_virtual_server(server_id, j)
            self.servers.append((virtual_server_id, server_id))

    def get_server(self, request_path):
        hashed_request = hash_request(request_path)
        closest_server = None
        min_distance = float('inf')
        for virtual_server_id, server_id in self.servers:
            distance = abs(hashed_request - virtual_server_id)
            if distance < min_distance:
                min_distance = distance
                closest_server = server_id
        print("Hashed request:", hashed_request)
        print("Closest server:", closest_server)
        return closest_server

# Create an instance of the ConsistentHashing class
consistent_hashing = ConsistentHashing()

# Add initial server replicas
for server_id in server_replicas:
    consistent_hashing.add_server(server_id)

@app.route('/home', methods=['GET'])
def home():
    # Get the request path
    request_path = request.path
    # Use consistent hashing to determine the server for this request
    mapped_server = consistent_hashing.get_server(request_path)
    # Return a JSON response with a greeting message including the server ID
    return jsonify({
        "message": f"Hello from server: {mapped_server}",
        "status": "successful",
        "server_id": mapped_server
    }), 200

@app.route('/heartbeat', methods=['GET'])
def heartbeat():
    # Return an empty response with status code 200 to indicate the server is alive
    return 'Heartbeat received', 200

@app.route('/add', methods=['POST'])
def add_servers():
    data = request.json
    n = data.get('n')
    hostnames = data.get('hostnames')

    # Perform sanity checks on the request payload
    if n is None or hostnames is None:
        return jsonify({"error": "Both 'n' and 'hostnames' must be provided"}), 400

    if not isinstance(n, int) or n <= 0:
        return jsonify({"error": "'n' must be a positive integer"}), 400

    if not isinstance(hostnames, list):
        return jsonify({"error": "'hostnames' must be a list"}), 400

    if len(hostnames) != n:
        return jsonify({"error": "'hostnames' length must match the number of new instances 'n'"}), 400

    if len(set(hostnames)) != len(hostnames):
        return jsonify({"error": "Hostnames must be unique"}), 400

    # Add new server instances with preferred hostnames
    for hostname in hostnames:
        server_replicas.append(hostname)
        consistent_hashing.add_server(hostname)

    # Return response with updated server replicas list
    return jsonify({
        "message": {
            "N": len(server_replicas),
            "replicas": server_replicas
        },
        "status": "successful"
    }), 200

@app.route('/rep', methods=['GET'])
def get_replicas():
    # Return the current list of server replicas
    return jsonify({
        "message": {
            "N": len(server_replicas),
            "replicas": server_replicas
        },
        "status": "successful"
    }), 200

@app.route('/simulate_failure', methods=['POST'])
def simulate_failure():
    # Simulate a server failure by removing a random server replica
    if server_replicas:
        print("Server replicas before failure:", server_replicas)
        removed_server = random.choice(server_replicas)
        server_replicas.remove(removed_server)
        consistent_hashing.servers = [(virtual_server_id, server_id) for virtual_server_id, server_id in consistent_hashing.servers if server_id != removed_server]

        # Add a new server instance to cover the load
        new_server = f"Server {len(server_replicas) + 1}"
        server_replicas.append(new_server)
        consistent_hashing.add_server(new_server)
        print("Server replicas after failure:", server_replicas)

        return jsonify({
            "message": f"Simulated failure of server: {removed_server}. New server instance {new_server} added.",
            "status": "successful"
        }), 200
    else:
        return jsonify({
            "error": "No server replicas to remove",
            "status": "failure"
        }), 400

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"error": "Endpoint not found"}), 404

@app.route('/delete', methods=['DELETE'])
def remove_servers():
    data = request.json
    hostnames = data.get('hostnames')

    # Perform sanity checks on the request payload
    if hostnames is None:
        return jsonify({"error": "'hostnames' must be provided"}), 400

    if not isinstance(hostnames, list):
        return jsonify({"error": "'hostnames' must be a list"}), 400

    # Remove server instances with specified hostnames
    removed_count = 0
    for hostname in hostnames:
        if hostname in server_replicas:
            server_replicas.remove(hostname)
            consistent_hashing.servers = [(virtual_server_id, server_id) for virtual_server_id, server_id in consistent_hashing.servers if server_id != hostname]
            removed_count += 1

    if removed_count > 0:
        return jsonify({
            "message": f"Removed {removed_count} server instance(s)",
            "status": "successful"
        }), 200
    else:
        return jsonify({
            "error": "No matching server instances found for removal",
            "status": "failure"
        }), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
