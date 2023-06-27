import tkinter as Tk
import cv2
import keyboard

def warn(content):
    
    achtung = Tk.Tk()
    achtung.geometry("300x150")
    achtung.title("Problem")
    achtung.resizable(False, False)
    
    vnimanie = Tk.Label(achtung, text=content)
    vnimanie.place(x=110, y=50)
    achtung.mainloop()

def main():
    
    window = Tk.Tk()
    window.title("RTSP Monitor")
    window.resizable(False, False)
    window.geometry("400x200")
    
    addresstext = Tk.Label(text="Enter an RTSP link:" + "\n" + "(format: rtsp://username:password@IPaddress:port)")
    addresstext.place(x=55, y=85)
    
    address = Tk.Entry(window, width=45)
    address.place(x=65, y=120)
    
    camname = Tk.Label(text="Name your camera:")
    camname.place(x=145, y=30)
    
    nameget = Tk.Entry(window, width=30)
    nameget.place(x=105, y=50)
    
    def play():
        
        ip = address.get()
        name = nameget.get()
        
        if ip == "" and name != "":
            warn("The link is missing!")
        elif ip != "" and name == "":
            warn("The name is missing!")
        elif ip == "" and name == "":
            warn("There isn't" + "\n" + "any data.")
        else:
            
            try:
                video = cv2.VideoCapture(ip)
            
                winname = "Monitoring of " + name + " - press S for shutdown"
                while(keyboard.is_pressed("s") == False):
                
                    cv2.namedWindow(winname, cv2.WINDOW_NORMAL)
                
                    ret, frame = video.read()
                    cv2.imshow(winname,frame)
                    cv2.waitKey(1)
                cv2.destroyAllWindows()
            except cv2.error: 
                cv2.destroyAllWindows()
                warn("Badly written address")
    
    start = Tk.Button(window, width=5, height=1, text="Stream", command=play)
    start.place(x=180, y=160)
    window.mainloop()

main()
