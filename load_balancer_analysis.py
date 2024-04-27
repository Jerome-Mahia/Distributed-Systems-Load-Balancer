import requests
import matplotlib.pyplot as plt

def analyze_load_balancer():
    # Define the URL of the load balancer
    url = 'http://localhost:5000/home'

    # Loop over values of N from 2 to 6
    for n in range(2, 7):
        total_requests = 10000
        requests_per_server = [0] * n

        # Send 10000 requests to the load balancer
        for _ in range(total_requests):
            response = requests.get(url)
            server_id = response.json().get('server_id')
            
            # Check if server_id is not None and is in the expected format
            if server_id and server_id[-1].isdigit():
                server_index = int(server_id[-1]) - 1
                requests_per_server[server_index] += 1
            else:
                print(f"Unexpected server ID format: {server_id}")

        # Calculate the average load of the servers
        average_load = sum(requests_per_server) / n

        # Print or store the average load for analysis
        print(f"Average load with {n} server(s): {average_load}")

        # Plot the average load against the value of N
        plt.plot(n, average_load, marker='o', label=f"N={n}")

    # Add labels and legend to the plot
    plt.xlabel('Number of Server Containers (N)')
    plt.ylabel('Average Load')
    plt.title('Average Load of Servers vs. Number of Server Containers')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    analyze_load_balancer()

