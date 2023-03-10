import threading
import time

class EdgeNodeList:

    def __init__(self):
        self.lock = threading.Lock()
        self.list = set()
        self.last_ping_list = {}##

    def add(self, edge):
        with self.lock:
            print('Adding edge: ', edge)
            self.list.add((edge))
            print('Current Edge List: ', self.list)
            self.last_ping_list[edge] = time.time()##

    def remove(self, edge):

        with self.lock:
            if edge in self.list:
                print('Removing edge: ', edge)
                self.list.remove(edge)
                self.remove(edge)##
                print('Current Edge list: ', self.list)

    def overwrite(self, new_list):
        with self.lock:
            print('edge node list will be going to overwrite')
            self.list = new_list
            print('Current Edge list: ', self.list)

    def get_list(self):
        return self.list
    
    def ping_recv(self, edge):##
        self.last_ping_list[edge] = time.time()
        return
    
    def has_this_edge(self, edge):##
        return edge in self.list
    
    def last_ping(self, edge):##try?
        return self.last_ping_list[edge]