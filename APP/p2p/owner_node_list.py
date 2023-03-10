import threading


class OwnerCoreNodeList:

    def __init__(self):
        self.lock = threading.Lock()
        self.list = set()

    def add(self, peer):
        with self.lock:
            print('Adding Owner peer: ', peer)
            self.list.add((peer))
            print('Current Owner List: '+ str(len(self.list)), self.list)

    def remove(self, peer):
        with self.lock:
            if peer in self.list:
                print('Removing peer: ', peer)
                self.list.remove(peer)
                print('Current Owner list: '+ str(len(self.list)), self.list)

    def overwrite(self, new_list):
        with self.lock:
            print('owner node list will be going to overwrite')
            self.list = new_list
            print('Current Owner list: '+ str(len(self.list)), self.list)

    def get_list(self):
        return self.list

    def get_length(self):
        print("get_length(self):" , len(self.list))
        return len(self.list)

    def get_c_node_info(self):
        return list(self.list)[0]

    def has_this_peer(self, peer):
        return peer in self.list
