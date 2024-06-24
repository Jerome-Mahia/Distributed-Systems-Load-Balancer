import requests
import matplotlib.pyplot as plt

def analyze_load_balancer():
    # Define the URL of the load balancer
    url = 'http://localhost:5000/home'

    # Define the number of server containers
    n = 3

    # Send 10000 requests to the load balancer
    total_requests = 10000
    requests_per_server = [0] * n
    for _ in range(total_requests):
        response = requests.get(url)
        server_id = response.json().get('server_id')
        
        # Ensure that the server_id is valid before accessing its index
        if server_id:
            try:
                # Extract the server index from the server_id string
                server_index = int(server_id.split()[-1]) - 1
                requests_per_server[server_index] += 1
            except (IndexError, ValueError):
                print(f"Unexpected server ID format: {server_id}")

    # Plot the request count handled by each server instance in a bar graph
    labels = [f'Server {i+1}' for i in range(n)]
    plt.bar(labels, requests_per_server)
    plt.xlabel('Server ID')
    plt.ylabel('Request Count')
    plt.title('Request Count Handled by Each Server Instance')
    plt.show()

    # Calculate and print the average load of each server container
    total_load = sum(requests_per_server)
    avg_load = total_load / n
    print(f"Average load per server: {avg_load}")

if __name__ == "__main__":
    analyze_load_balancer()
