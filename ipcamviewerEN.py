import tkinter as Tk
import cv2
import keyboard
import os
import json

ipdata = {"adress1":"",
          "adress2":"",
          "adress3":"",
          "adress4":"",
          "adress5":""}

path = os.path.dirname(os.path.abspath(__file__))

bullet = "\u2022"

def warn(content):
    achtung = Tk.Tk()
    achtung.geometry("300x150")
    achtung.title("Fault")
    achtung.resizable(False, False)
    
    vnimanie = Tk.Label(achtung, text=content)
    vnimanie.place(x=80, y=50)
    achtung.mainloop()

def main():
    window = Tk.Tk()
    window.title("Simple RTSP Monitor")
    window.resizable(False, False)
    window.geometry("400x350")
    
    camname = Tk.Label(text="Camera name:")
    camname.place(x=160, y=25)
    
    nameget = Tk.Entry(window, width=30)
    nameget.place(x=105, y=50)
    
    addresstext = Tk.Label(text="Enter an RTSP link:" + "\n" + "(format rtsp://user:password@IPadress:port"
                           + "\n" + "or rtsp://IPadress:port)")
    addresstext.place(x=85, y=70)
    
    address = Tk.Entry(window, width=45, show=bullet)
    address.place(x=65, y=120)
    
    datatext = Tk.Label(text="Last used addresses:")
    datatext.place(x=145, y=190)
    
    addresslist = Tk.Listbox(window, width=45, height=5)
    addresslist.place(x=65, y=210)
    
    try:
        with open(path + "/adresses.json", "r") as readaddresses:
            lastused = json.load(readaddresses)
        
        for address in lastused:
            if address != "":
                addresslist.insert("end", lastused[address])
            else:
                break
    except FileNotFoundError:
        pass
    
    def play():
        ip = address.get()
        name = nameget.get()
        
        if ip == "" and name != "":
            warn("The link is missing!")
        elif ip != "" and name == "":
            warn("Unnamed camera!")
        elif ip == "" and name == "":
            warn("There isn't" + "\n" + "any data.")
        else:
            
            try:
                for camera, ipaddress in ipdata.items():
                    if ipaddress == "":
                        ipdata[camera] = ip
                        break
                    else:
                        continue
                
                with open(path + "/adresses.json", "w") as saveaddresses:
                    json.dump(ipdata, saveaddresses)
                
                for ipaddress in ipdata.values():
                    if ipaddress != "":
                        addresslist.insert("end", ipaddress)
                        break
                    else:
                        continue
                    
                video = cv2.VideoCapture(ip)
            
                winname = "Monitoring of " + name + " - press S to terminate"
                while(keyboard.is_pressed("s") == False):
                
                    cv2.namedWindow(winname, cv2.WINDOW_NORMAL)
                
                    ret, frame = video.read()
                    cv2.imshow(winname,frame)
                    cv2.waitKey(1)
                cv2.destroyAllWindows()
            except cv2.error: 
                cv2.destroyAllWindows()
                warn("Badly typed" + "\n" +
                     "or not-working IP address!")
    
    start = Tk.Button(window, width=5, height=1, text="Watch", command=play)
    start.place(x=180, y=150)

    def enteraddress():
        chosen = addresslist.get(addresslist.curselection())
        address.insert(0, chosen)
    
    def deleteaddresses():
        addresslist.delete(addresslist.curselection())
        
        if not addresslist.get(0,4):
            addresslist.delete(0,4)
            os.remove(path + "/adresses.json")
        else:
            pass
    
    def deleteall():
        addresslist.delete(0,4)
            
    choice = Tk.Button(window, width=6, height=1, text="Choose", command=enteraddress)
    choice.place(x=110, y=310)
    
    delete = Tk.Button(window, width=6, height=1, text="Delete", command=deleteaddresses)
    delete.place(x=165, y=310)
    
    alldelete = Tk.Button(window, width=10, height=1, text="Delete all", command=deleteall)
    alldelete.place(x=220, y=310)
    window.mainloop()

main()
