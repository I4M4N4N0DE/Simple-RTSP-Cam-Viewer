import tkinter as Tk
import cv2
import keyboard
import os
import json

ipdata = {"adresa1":"",
          "adresa2":"",
          "adresa3":"",
          "adresa4":"",
          "adresa5":""}

cesta = os.path.dirname(os.path.abspath(__file__))

koule = "\u2022"

def warn(obsah):
    achtung = Tk.Tk()
    achtung.geometry("300x150")
    achtung.title("Chyba")
    achtung.resizable(False, False)
    
    vnimanie = Tk.Label(achtung, text=obsah)
    vnimanie.place(x=80, y=50)
    achtung.mainloop()

def main():
    window = Tk.Tk()
    window.title("RTSP Monitor")
    window.resizable(False, False)
    window.geometry("400x350")
    
    camname = Tk.Label(text="Pojmenuj kameru:")
    camname.place(x=145, y=25)
    
    nameget = Tk.Entry(window, width=30)
    nameget.place(x=105, y=50)
    
    addresstext = Tk.Label(text="Zadej RTSP odkaz:" + "\n" + "(formát rtsp://uživatel:heslo@IPadresa:port"
                           + "\n" + "nebo rtsp://IPadresa:port)")
    addresstext.place(x=85, y=70)
    
    address = Tk.Entry(window, width=45, show=koule)
    address.place(x=65, y=120)
    
    datatext = Tk.Label(text="Poslední použité adresy:")
    datatext.place(x=135, y=190)
    
    listadres = Tk.Listbox(window, width=45, height=5)
    listadres.place(x=65, y=210)
    
    try:
        with open(cesta + "/adresy.json", "r") as prectidaresy:
            lastused = json.load(prectidaresy)
        
        for adresa in lastused:
            if adresa != "":
                listadres.insert("end", lastused[adresa])
            else:
                break
    except FileNotFoundError:
        pass
    
    def play():
        ip = address.get()
        name = nameget.get()
        
        if ip == "" and name != "":
            warn("Odkaz chybí!")
        elif ip != "" and name == "":
            warn("Chybí název kamery!")
        elif ip == "" and name == "":
            warn("Nejsou zadány" + "\n" + "žádné údaje.")
        else:
            
            try:
                for kamera, adresa in ipdata.items():
                    if adresa == "":
                        ipdata[kamera] = ip
                        break
                    else:
                        continue
                
                with open(cesta + "/adresy.json", "w") as ulozadresy:
                    json.dump(ipdata, ulozadresy)
                
                for adresa in ipdata.values():
                    if adresa != "":
                        listadres.insert("end", adresa)
                        break
                    else:
                        continue
                    
                video = cv2.VideoCapture(ip)
            
                winname = "Monitoring kamery " + name + " - stiskni S pro ukonceni"
                while(keyboard.is_pressed("s") == False):
                
                    cv2.namedWindow(winname, cv2.WINDOW_NORMAL)
                
                    ret, frame = video.read()
                    cv2.imshow(winname,frame)
                    cv2.waitKey(1)
                cv2.destroyAllWindows()
            except cv2.error: 
                cv2.destroyAllWindows()
                warn("Chybně zadaná," + "\n" +
                     "nebo nefunkční ip adresa")
    
    start = Tk.Button(window, width=5, height=1, text="Spustit", command=play)
    start.place(x=180, y=150)

    def vlozitadresu():
        zvoleno = listadres.get(listadres.curselection())
        address.insert(0, zvoleno)
    
    def smazatadresu():
        listadres.delete(listadres.curselection())
        
        if not listadres.get(0,4):
            listadres.delete(0,4)
            os.remove(cesta + "/adresy.json")
        else:
            pass
    
    def smazatvse():
        listadres.delete(0,4)
            
    vyber = Tk.Button(window, width=5, height=1, text="Zvolit", command=vlozitadresu)
    vyber.place(x=110, y=310)
    
    smazani = Tk.Button(window, width=6, height=1, text="Smazat", command=smazatadresu)
    smazani.place(x=160, y=310)
    
    smazanivseho = Tk.Button(window, width=9, height=1, text="Smazat vše", command=smazatvse)
    smazanivseho.place(x=215, y=310)
    window.mainloop()

main()
