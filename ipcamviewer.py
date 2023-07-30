import tkinter as tk
from tkinter.messagebox import showerror
import cv2
import os
import json

class App:
    def __init__(self):
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.json_name = "addresses.json"
        try:
            with open(self.json_name) as f:
                self.addresses = json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            open(self.json_name, "w").close()
            self.addresses = []

        self.root = tk.Tk()
        self.root.title("RTSP Monitor")
        self.root.resizable(False, False)
        self.root.geometry("400x350")
        
        tk.Label(text="Pojmenuj kameru:").place(x=145, y=25)
        
        self.name_entry = tk.Entry(self.root, width=30)
        self.name_entry.place(x=105, y=50)
        
        tk.Label(text="Zadej RTSP odkaz:\n"
                + "(formát rtsp://uživatel:heslo@IPadresa:port\n"
                + "nebo rtsp://IPadresa:port)").place(x=85, y=70)
        
        self.address_entry = tk.Entry(self.root, width=45)
        self.address_entry.place(x=65, y=120)
        
        tk.Label(text="Poslední použité adresy:").place(x=135, y=190)
        
        self.address_list = tk.Listbox(self.root, width=45, height=5)
        self.address_list.place(x=65, y=210)
        
        for address in self.addresses:
            self.address_list.insert("end", address)
        if len(self.addresses):
            self.address_entry.insert("end", self.addresses[-1])
        
        tk.Button(self.root, width=5, height=1, text="Spustit",
                  command=self.play).place(x=180, y=150) 
        tk.Button(self.root, width=5, height=1, text="Zvolit",
                  command=self.insert_address).place(x=110, y=310)      
        tk.Button(self.root, width=6, height=1, text="Smazat",
                  command=self.delete_address).place(x=160, y=310)       
        tk.Button(self.root, width=9, height=1, text="Smazat vše",
                  command=self.delete_all).place(x=215, y=310)

        self.root.mainloop()

    def insert_address(self):
        address = self.address_list.get(self.address_list.curselection())
        self.address_entry.delete(0, "end")
        self.address_entry.insert(0, self.address_list.get(address))

    def delete_address(self):
        self.address_list.delete(self.address_list.curselection())

    def delete_all(self):
        self.addresses = []
        self.address_list.delete(0, "end")
        with open(self.json_name, "w") as f:
            json.dump(self.addresses, f)

    def play(self):
        address = self.address_entry.get()
        name = self.name_entry.get()
        
        if address == "":
            showerror("Chyba", "Chybí odkaz!")
            return
        elif name == "":
            showerror("Chyba", "Chybí název kamery!")
            return
            
        self.addresses.append(address)
        self.address_list.insert("end", address)
        
        with open(self.json_name, "w") as f:
            json.dump(self.addresses, f)
            
        cap = cv2.VideoCapture(address)
        if not cap.isOpened():
            showerror(message="Chybně zadaná nebo nefunkční adresa!")
            return

        winname = f"Monitoring kamery {name} - stiskni S pro ukonceni"
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            cv2.imshow(winname, frame)

            if cv2.waitKey(1) == ord("s"):
                break
        cv2.destroyAllWindows()

App()