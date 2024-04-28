"""
This module implements the Consistent Hashing Algortithm
"""

import hashlib
import math


class ConsistentHashing:
    def __init__(self, servers=[]):
        self.N = len(servers)  # Number of server containers
        self.slots = 512  # Total number of slots in the consistent hash map
        self.K = math.ceil(math.log(self.slots, 2))  # Number of virtual servers for each server container  (9)
        self.circle = {}
        for server in servers:
            self.add_server(server)
        print(len(self.circle))

    def add_server(self, server):
        for i in range(self.N):
            for j in range(self.K):
                key = self.hash_key(server, i, j)
                print(i,j,key)
                self.circle[key] = server

    def remove_server(self, server):
        for i in range(self.N):
            for j in range(self.K):
                key = self.hash_key(server, i, j)
                del self.circle[key]

    def get_server(self, key):
        key = self.hash_key(key)
        keys = sorted(self.circle.keys())
        for i, k in enumerate(keys):
            if key <= k:
                return self.circle[k]
        return self.circle[keys[0]]
    
    def hash_key(self, key, i=0, j=0):
        key = f"{key}-{i}-{j}".encode()
        return int(hashlib.sha256(key).hexdigest(), 16) % self.slots
  
    def hash_virtual_server(self, server, j):
        return ((server**2) + (j**2) + (2*j) + 25) % self.slots
    
    def __str__(self):
        return str(self.circle)


