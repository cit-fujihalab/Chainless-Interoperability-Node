import tkinter as tk
from blockchain.blockchain_manager import BlockchainManager

class MainWindow():
    print("Initializing Mainwindow")
    def __init__(self,my_port):
        self.info = tk.Tk()
        self.my_port = my_port
        print("==========================================================================================================================================-",self.my_port)
        self.Break_state = False
        self.block_state_P = []
        self.block_state_C = []
        self.bmc = BlockchainManager()

    def generate_genesis_window(self):
        self.info.title("Info -" + str(self.my_port))
        self.info.geometry("400x300")
        button1 = tk.Button(self.info, text="Owner_node_list", command=self.create_window1, width=50)
        button2 = tk.Button(self.info, text="Block Part", command=self.create_window2, width=50)
        button3 = tk.Button(self.info, text="Cross Reference Part", command=self.create_window3, width=50)
        button4 = tk.Button(self.info, text="Show Last Heartbeat", command=self.create_window2, width=50)
        button5 = tk.Button(self.info, text="Show signature", command=self.create_window3, width=50)
        button6 = tk.Button(self.info, text="Cause node failure.", command=self.Break_node,width=50, foreground='#ff0000', background='#ffaacc')
        button7 = tk.Button(self.info, text="Revive node.", command=self.Revive_node,width=50, foreground='#000000', background='#4169e1')

        button1.pack(side="top")
        button2.pack(side="top")
        button3.pack(side="top")
        button4.pack(side="top")
        button5.pack(side="top")
        button6.pack(side="bottom")
        button7.pack(side="bottom")
        self.info.mainloop()

    def create_window1(self):
        t = tk.Toplevel(self.info)
        t.wm_title("Create Info")
        t.geometry("400x300")
        l = tk.Label(t, text='consensus information ', foreground='#ff0000', background='#ffaacc')
        l.pack(side="top", fill="both", expand=True, padx=100, pady=100)
        
    def create_window2(self):
        t = tk.Toplevel(self.info)
        t.wm_title("Create Info")
        t.geometry("400x300")
        l = tk.Label(t, text='consensus information ',  foreground='#ff0000', background='#ffaacc')
        l.pack(side="top", fill="both", expand=True, padx=100, pady=100)

    def create_window3(self):
        t = tk.Toplevel(self.info)
        t.wm_title("Create Info")
        t.geometry("400x300")
        l = tk.Label(t, text='information ',  foreground='#ff0000', background='#ffaacc')
        l.pack(side="top", fill="both", expand=True, padx=100, pady=100)

    def create_window4(self):
        t = tk.Toplevel(self.info)
        t.wm_title("Create Info")
        t.geometry("400x300")
        l = tk.Label(t, text='consensus information ',  foreground='#ff0000', background='#ffaacc')
        l.pack(side="top", fill="both", expand=True, padx=100, pady=100)

    def create_window5(self):
        t = tk.Toplevel(self.info)
        t.wm_title("Create Info")
        t.geometry("400x300")
        l = tk.Label(t, text='consensus information ',  foreground='#ff0000', background='#ffaacc')
        l.pack(side="top", fill="both", expand=True, padx=100, pady=100)

    def Break_node(self):
        t = tk.Toplevel(self.info)
        t.wm_title("Create Info")
        t.geometry("400x300")
        l = tk.Label(t, text='broken ', foreground='#ff0000', background='#ffaacc')
        l.pack(side="top", fill="both", expand=True, padx=100, pady=100)
        self.Break_state = True
        print("broken")

    def Revive_node(self):
        t = tk.Toplevel(self.info)
        t.wm_title("Create Info")
        t.geometry("400x300")
        l = tk.Label(t, text='broken ', foreground='#000000', background='#4169e1')
        l.pack(side="top", fill="both", expand=True, padx=100, pady=100)
        self.Break_state = False
        print("broken")

    def renew_block_state(self, block_P): 
        print("block")
        self.block_state_P = block_P
    
    def renew_previous_cross_reference_block_state(self, block_C): 
        print("previous")
        self.block_state_C = block_C
    

if __name__ == "__main__":
        MainWindow()
