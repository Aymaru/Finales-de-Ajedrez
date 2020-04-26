import sys
sys.path.append("..")
import tkinter as tk
from tkinter import ttk

from Main import centrar
from GUI import Configuracion

class Carga(tk.Frame):
    """Crea la ventana de inicio con un progressbar.
    """
        ###Constructor de la clase###
    def __init__(self,master):
        """Crea una instancia de la clase Inicio
        """         
        self.master = master          
        self.dimensiones()      # Crea una ventana inicio.
        centrar(self.master)    # Centra la pantalla.
        self.imagen()           # Agrega la imagen al fondo.
        self.progressBar()      # Configuracion del ProgressBar.
        self.pack()
        self.leer_bytes()       # Aumenta los bytes del progressBar.
        
    # ###Ajuste UI###
    def dimensiones(self):
        """Define los aspectos de la ventana inicio
        """
        tk.Frame.__init__(self,self.master)
        self.master.title('Instituto Tecnológico de Costa Rica')
        self.master.focus_set()           # Provoca que la ventana tome el focus.
        self.master.grab_set() 
        self.master.geometry("800x600")   # Tamaño de la ventana de inicio.
        self.master.resizable(0,0)        # Bloquea que se cambien las dimensiones de la ventana inicio.
        #self.master.pack()

    def imagen(self):
        """Carga las imagenes a la ventana
        """
        self.fondo = tk.PhotoImage(file="./Imagenes/espera3.gif")  # Crea la imagen de fondo de la ventana inicio.
        self.lblFondo = tk.Label(self, image=self.fondo, background='black') # Agrega la imagen en el fondo.
        self.lblFondo.pack()

    # ###SubComponentes de la Ventana###
    def progressBar(self):
        self.estiloBar = ttk.Style()
        self.estiloBar.theme_use('classic')
        self.estiloBar.configure("red.Horizontal.TProgressbar", foreground='black', background='black')
        self.progress = ttk.Progressbar(self, orient="horizontal", length=803, mode="determinate",style = "red.Horizontal.TProgressbar") # Crea una Progressbar
        self.lblFondo.grid(row=0, column=0)
        self.bytes = 0
        self.maxbytes = 1000
        self.progress["value"] = 0
        self.progress["maximum"] = 1000
        self.progress.place(x=-2, y=585) # Ubico el progressBar.

    # ###Métodos especializados###
    def leer_bytes(self):
        """Lee los bytes para la Progressbar
        """
        self.bytes += 45                            # Incremeta el progressBar en 45.
        self.progress["value"] = self.bytes         # Actualizo el valor.
        if self.bytes < self.maxbytes:
            self.master.after(100, self.leer_bytes) #Cada 100 milisegundo realice la funcion.
        else:
            self.destroy()                   # Se destruye si el progressBar se lleno.
            Configuracion.Configuracion(self.master)                         # Comienza la configuración del juego.
