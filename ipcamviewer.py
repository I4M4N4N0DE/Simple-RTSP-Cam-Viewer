import tkinter as Tk
import cv2
import keyboard

def warn(obsah):
    
    achtung = Tk.Tk()
    achtung.geometry("300x150")
    achtung.title("Chyba")
    achtung.resizable(False, False)
    
    vnimanie = Tk.Label(achtung, text=obsah)
    vnimanie.place(x=110, y=50)
    achtung.mainloop()

def main():
    
    okno = Tk.Tk()
    okno.title("RTSP Monitor")
    okno.resizable(False, False)
    okno.geometry("400x200")
    
    textadresa = Tk.Label(text="Zadej RTSP odkaz:" + "\n" + "(formát rtsp://uživatel:heslo@veřejnáIPadresa:port)")
    textadresa.place(x=80, y=70)
    
    adresa = Tk.Entry(okno, width=45)
    adresa.place(x=65, y=120)
    
    textnazev = Tk.Label(text="Pojmenuj kameru:")
    textnazev.place(x=145, y=30)
    
    nazev = Tk.Entry(okno, width=30)
    nazev.place(x=105, y=50)
    
    def play():
        
        ip = adresa.get()
        name = nazev.get()
        
        if ip == "" and name != "":
            warn("Odkaz chybí!")
        elif ip != "" and name == "":
            warn("Chybí název kamery!")
        elif ip == "" and name == "":
            warn("Nejsou zadány" + "\n" + "žádné údaje.")
        else:
            
            try:
                video = cv2.VideoCapture(ip)
            
                nazevokna = "Monitoring kamery " + name + " - stiskni S pro ukonceni"
                while(keyboard.is_pressed("s") == False):
                
                    cv2.namedWindow(nazevokna, cv2.WINDOW_NORMAL)
                
                    ret, frame = video.read()
                    cv2.imshow(nazevokna,frame)
                    cv2.waitKey(1)
                cv2.destroyAllWindows()
            except cv2.error: 
                cv2.destroyAllWindows()
                warn("Chybně zadaná adresa")
    
    start = Tk.Button(okno, width=5, height=1, text="Spustit", command=play)
    start.place(x=180, y=160)
    okno.mainloop()

main()
