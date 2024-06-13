class ConsistentHashMap:
    def __init__(self, num_containers, num_slots, num_virtual_servers):
        self.num_containers = num_containers
        self.num_slots = num_slots
        self.num_virtual_servers = num_virtual_servers
        self.hash_map = [[] for _ in range(num_slots)]  # Initialize hash map as an array of empty lists

    def hash_function_request(self, i):
        return (i + 2 * i + 17) % self.num_slots

    def hash_function_virtual_server(self, i, j):
    	container_id_int = int(i)  # Convert container_id to integer
    	return (container_id_int + j + 2 * j + 25) % self.num_slots

    def add_server_container(self, container_id):
        # Add virtual servers for the container
        for j in range(self.num_virtual_servers):
            virtual_server_id = f"{container_id}-V{j}"
            hash_value = self.hash_function_virtual_server(container_id, j)
            self.hash_map[hash_value].append(virtual_server_id)

    def get_server_container(self, request_id):
        hash_value = self.hash_function_request(request_id)
        # Linear probing to find the next suitable slot if there's a conflict
        while not self.hash_map[hash_value]:
            hash_value = (hash_value + 1) % self.num_slots
        return self.hash_map[hash_value][0]  # Return the first server container in the slot
        
        
    def remove_server_container(self, hostname):
        # Remove the specified server container from the hash map
        for i in range(len(self.hash_map)):
            if hostname in self.hash_map[i]:
                self.hash_map[i].remove(hostname)

