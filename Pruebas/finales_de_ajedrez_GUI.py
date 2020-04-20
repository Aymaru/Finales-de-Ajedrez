from tkinter import *
from tkinter import ttk
from time import *
import os

class Espera(Frame):
    """Crea la ventana de espera
    """
    def __init__(self):
        """Crea una instancia de la clase Espera
        """    
        self.ventana = Tk() # Crea una ventana
        self.ventana.title('Instituto Tecnológico de Costa Rica')
        self.ventana.focus_set() # Provoca que la ventana tome el focus
        self.ventana.grab_set() # Desabilita todas las otras ventanas hasta que esta ventana sea destruida        Frame.__init__(self, self.ventana)
        self.ventana.geometry("800x600")
        self.ventana.resizable(0,0)

        self.fondo = PhotoImage(file="espera3.gif") # Crea una imagen de fondo
        self.lblFondo = Label(self.ventana, image=self.fondo, background='black')
        s = ttk.Style()
        s.theme_use('clam')
        s.configure("red.Horizontal.TProgressbar", foreground='black', background='black')
        self.progress = ttk.Progressbar(self.ventana, orient="horizontal", length=800, mode="determinate",style = "red.Horizontal.TProgressbar") # Crea una Progressbar
        self.lblFondo.grid(row=0, column=0)
        self.bytes = 0
        self.maxbytes = 0
        self.progress.place(x=0, y=585)
        self.progress["value"] = 0
        self.maxbytes = 1000
        self.progress["maximum"] = 1000
        self.leer_bytes()

    def leer_bytes(self):
        """Lee los bytes para la Progressbar
        """
        self.bytes += 35
        self.progress["value"] = self.bytes
        if self.bytes < self.maxbytes:
            self.ventana.after(100, self.leer_bytes)
        else:
            self.ventana.destroy()
            inicio()

def _create_circle(self, x, y, r, **kwargs):
    """
    Crea la función de canvas "_create_circle" modificando la función "create_oval"

    Entradas: x: posición en el eje x
              y: posición enj el eje y
              r: radio del circulo
              **kwargs: parámetros adicionales

    Salidas: Nueva función create_circle
    """
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)

class Application(Frame):
    """Crea la intefaz del programa
    """
    def __init__(self,master):
        """
        """
        self.root = master  # Crea una pantalla
        Frame.__init__(self, master)
        self.root.resizable(0,0)
        self.root.geometry("800x600")
        self.root.title("Instituto Tecnológico de Costa Rica")
        self.root["bg"] = "black"
        self.crearWidgets()

    def crearWidgets(self):
        ##Tablero
        self.canvasTablero = Canvas(self.root, height=400, width=400)
        self.tablero = PhotoImage(file='tablero.gif')
        self.lblTalero = Label(self.canvasTablero, image=self.tablero, background='black')
        self.canvasTablero.place(x=28,y=80)
        self.lblTalero.place(x=0, y=0)
        ##SalidaResultador
        self.canvasResutados = Canvas(self.root, height=200, width=230,borderwidth=3,relief="solid", highlightthickness=2)
        self.canvasResutados.place(x = 545, y = 100)
        self.resultados = "Hola como estás -> configuracion"
        label_resultados = self.canvasResutados.create_text(0, 0, text=self.resultados, font="Arial 10")
        ##CrearPiezas
        self.canvasImg1 = Canvas(self.root, height=40, width=40,bd=0,highlightthickness=0)
        self.canvasImg1.create_rectangle(0,0,41,41,fill="white")
        self.image1 = PhotoImage(file='TorreN.gif')
        self.image_id = self.canvasImg1.create_image(20,20,image=self.image1)
        num = 42 * 0
        self.canvasImg1.place(x = 64.8 + num, y = 116)
        ##CrearPiezas
        self.canvasImg2 = Canvas(self.root, height=40, width=40,bd=0,highlightthickness=0)
        self.canvasImg2.create_rectangle(0,0,41,41,fill="black")
        self.image2 = PhotoImage(file='CaballoN.gif')
        self.image_id = self.canvasImg2.create_image(20,20,image=self.image2)
        num = 42 * 1
        self.canvasImg2.place(x = 64.8  + num, y = 116)
        ##CrearPiezas
        self.canvasImg3 = Canvas(self.root, height=40, width=40,bd=0,highlightthickness=0)
        self.canvasImg3.create_rectangle(0,0,41,41,fill="white")
        self.image3 = PhotoImage(file='AlfilN.gif')
        self.image_id = self.canvasImg3.create_image(20,20,image=self.image3)
        num = 42 * 2
        self.canvasImg3.place(x = 64.8  + num, y = 116)
        ##CrearPiezas
        self.canvasImg4 = Canvas(self.root, height=40, width=40,bd=0,highlightthickness=0)
        self.canvasImg4.create_rectangle(0,0,41,41,fill="black")
        self.image4 = PhotoImage(file='AlfilN.gif')
        self.image_id = self.canvasImg4.create_image(20,20,image=self.image4)
        num = 42 * 3
        self.canvasImg4.place(x = 64.8  + num, y = 116)
        ##CrearPiezas
        self.canvasImg5 = Canvas(self.root, height=40, width=40,bd=0,highlightthickness=0)
        self.canvasImg5.create_rectangle(0,0,41,41,fill="white")
        self.image5 = PhotoImage(file='ReyN.gif')
        self.image_id = self.canvasImg5.create_image(20,20,image=self.image5)
        num = 42 * 4
        self.canvasImg5.place(x = 64.8  + num, y = 116)
        ##CrearPiezas
        self.canvasImg6 = Canvas(self.root, height=40, width=40,bd=0,highlightthickness=0)
        self.canvasImg6.create_rectangle(0,0,41,41,fill="white")
        self.image6 = PhotoImage(file='ReinaN.gif')
        self.image_id = self.canvasImg6.create_image(20,20,image=self.image6)
        num = 42 * 4
        self.canvasImg6.place(x = 64.8  + num, y = 116)
        ##CrearPiezas
        self.canvasImg7 = Canvas(self.root, height=40, width=40,bd=0,highlightthickness=0)
        self.canvasImg7.create_rectangle(0,0,41,41,fill="white")
        self.image7 = PhotoImage(file='AlfilN.gif')
        self.image_id = self.canvasImg7.create_image(20,20,image=self.image7)
        num = 42 * 5
        self.canvasImg7.place(x = 64.8  + num, y = 116)
        ##CrearPiezas
        self.canvasImg8 = Canvas(self.root, height=40, width=40,bd=0,highlightthickness=0)
        self.canvasImg8.create_rectangle(0,0,41,41,fill="black")
        self.image8 = PhotoImage(file='CaballoN.gif')
        self.image_id = self.canvasImg8.create_image(20,20,image=self.image8)
        num = 42 * 6
        self.canvasImg8.place(x = 64.8  + num, y = 116)
        ##CrearPiezas
        self.canvasImg9 = Canvas(self.root, height=40, width=40,bd=0,highlightthickness=0)
        self.canvasImg9.create_rectangle(0,0,41,41,fill="white")
        self.image9 = PhotoImage(file='TorreN.gif')
        self.image_id = self.canvasImg9.create_image(20,20,image=self.image9)
        num = 42 * 7
        self.canvasImg9.place(x = 64.8  + num, y = 116)
        ##CrearPiezas
        self.listaPeonesN = []
        self.listaPeonesIDN = []
        self.image10 = PhotoImage(file='PeonN.gif')
        for n in range(0,7):
            self.listaPeonesN.append(Canvas(self.root, height=40, width=40,bd=0,highlightthickness=0))
            if(n % 2 == 0):
                self.listaPeonesN[n].create_rectangle(0,0,41,41,fill="white")
            else:
                self.listaPeonesN[n].create_rectangle(0,0,41,41,fill="green")
            self.listaPeonesN[n].create_image(20,20,image=self.image10)
            self.listaPeonesIDN.append(self.listaPeonesN[n])
            num = 42 * n
            self.listaPeonesN[n].place(x = 64.7 + num, y = 157)
   
        
        ###########################################################################################
        ##CrearPiezas
        self.canvasImg100 = Canvas(self.root, height=40, width=40,bd=0,highlightthickness=0)
        self.canvasImg100.create_rectangle(0,0,41,41,fill="black")
        self.image100 = PhotoImage(file='TorreB.gif')
        self.image_id = self.canvasImg100.create_image(20,20,image=self.image100)
        num = 42 * 0
        self.canvasImg100.place(x = 64.4 + num, y = 410)
        ##CrearPieza
        self.canvasImg11 = Canvas(self.root, height=40, width=40,bd=0,highlightthickness=0)
        self.canvasImg11.create_rectangle(0,0,41,41,fill="green")
        self.image11 = PhotoImage(file='CaballoB.gif')
        self.image_id = self.canvasImg11.create_image(20,20,image=self.image11)
        num = 42 * 1
        self.canvasImg11.place(x = 64.4 + num, y = 410)
        ##CrearPiezas
        self.canvasImg12 = Canvas(self.root, height=40, width=40,bd=0,highlightthickness=0)
        self.canvasImg12.create_rectangle(0,0,41,41,fill="black")
        self.image12 = PhotoImage(file='AlfilB.gif')
        self.image_id = self.canvasImg12.create_image(20,20,image=self.image12)
        num = 42 * 2
        self.canvasImg12.place(x = 64.4 + num, y = 410)
        ##CrearPiezas
        self.canvasImg13 = Canvas(self.root, height=40, width=40,bd=0,highlightthickness=0)
        self.canvasImg13.create_rectangle(0,0,41,41,fill="yellow")
        self.image13 = PhotoImage(file='Reinab.gif')
        self.image_id = self.canvasImg13.create_image(20,20,image=self.image13)
        num = 42 * 3
        self.canvasImg13.place(x = 64.4 + num, y = 410)
        ##CrearPiezaB
        self.canvasImg14 = Canvas(self.root, height=40, width=40,bd=0,highlightthickness=0)
        self.canvasImg14.create_rectangle(0,0,41,41,fill="black")
        self.image14 = PhotoImage(file='ReyB.gif')
        self.image_id = self.canvasImg14.create_image(20,20,image=self.image14)
        num = 42 * 4
        self.canvasImg14.place(x = 64.4 + num, y = 410)
        
        ##CrearPiezas
        self.canvasImg16 = Canvas(self.root, height=40, width=40,bd=0,highlightthickness=0)
        self.canvasImg16.create_rectangle(0,0,41,41,fill="red")
        self.image16 = PhotoImage(file='AlfilB.gif')
        self.image_id = self.canvasImg16.create_image(20,20,image=self.image16)
        num = 42 * 5
        self.canvasImg16.place(x = 64.4 + num, y = 410)
        ##CrearPiezas
        self.canvasImg17 = Canvas(self.root, height=40, width=40,bd=0,highlightthickness=0)
        self.canvasImg17.create_rectangle(0,0,41,41,fill="black")
        self.image17 = PhotoImage(file='CaballoB.gif')
        self.image_id = self.canvasImg17.create_image(20,20,image=self.image17)
        num = 42 * 6
        self.canvasImg17.place(x = 64.4 + num, y = 410)
        ##CrearPiezas
        self.canvasImg18 = Canvas(self.root, height=40, width=40,bd=0,highlightthickness=0)
        self.canvasImg18.create_rectangle(0,0,41,41,fill="white")
        self.image18 = PhotoImage(file='TorreB.gif')
        self.image_id = self.canvasImg18.create_image(20,20,image=self.image18)
        num = 42 * 7
        self.canvasImg18.place(x = 64.4 + num, y = 410)
        ##CrearPiezas
        self.listaPeonesB = []
        self.listaPeonesIDB = []
        self.image19 = PhotoImage(file='PeonB.gif')
        for n in range(0,8):
            self.listaPeonesB.append(Canvas(self.root, height=40, width=40,bd=0,highlightthickness=0))
            if(n % 2 == 0):
                pass
                #self.listaPeonesB[n].create_rectangle(0,0,41,41,fill="white")
            else:
                self.listaPeonesB[n].create_rectangle(0,0,41,41,fill="black")
            self.listaPeonesB[n].create_image(20,20,image=self.image19)
            self.listaPeonesIDB.append(self.listaPeonesB[n])
            num = 42 * n
            self.listaPeonesB[n].place(x = 64.4 + num, y = 365.2)


def inicio():
    """Funcion main del programa donde se ejecutan las instrucciones.
    """
    # Desarrollo del interfaz del programa.
    root = Tk() # Creación de la Ventana principal.
    app = Application(root)
    #app.crearWidgets()
    app.mainloop() # Espera a que se cierre la panatalla.
    

inicio()
