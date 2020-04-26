from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from time import *
import os

def centrar(ventana):
    """Centra una ventana Tkinter
    """
    # Calculo del centro de la pantalla según el display.
    ventana.update_idletasks() # Actualiza desde el inicio en vez del update que lo hace despues del primer after
    # Dimension de la pantalla
    width = ventana.winfo_width()
    height = ventana.winfo_height()
    # Dimensiones de la ventana de inicio
    x = (ventana.winfo_screenwidth() // 2) - (width // 2)
    y = (ventana.winfo_screenheight() // 2) - (height // 2) -20
    ventana.geometry('{}x{}+{}+{}'.format(width, height, x, y)) # Ubico la pantalla
    return ventana


class Ayuda(Frame):
    """Crea la ventana de inicio con un progressbar.
    """
        ###Constructor de la clase###
    def __init__(self):
        """Crea una instancia de la clase Inicio
        """
        self.dimensiones()      # Crea una ventana inicio.
        #self.imagen()           # Agrega la imagen al fondo.'
        self.botonEntendido()
        centrar(self.ayuda)    # Centra la pantalla.
        
    ###Ajuste UI###
    def dimensiones(self):
        """Define los aspectos de la ventana inicio
        """
        self.ayuda = Toplevel() 
        self.ayuda.title('Ayuda')
        self.ayuda.focus_set()           # Provoca que la ventana tome el focus.
        Frame.__init__(self, self.ayuda) #
        self.ayuda.geometry("440x434")   # Tamaño de la ventana de inicio.
        self.ayuda.resizable(0,0)        # Bloquea que se cambien las dimensiones de la ventana inicio.

    def imagen(self):
        """Carga las imagenes a la ventana
        """
        self.fondo = PhotoImage(file="../Imagenes/fondoAyuda.gif")  # Crea la imagen de fondo de la ventana inicio.
        self.lblFondo = Label(self.ayuda, image=self.fondo, background='black') # Agrega la imagen en el fondo.
        self.lblFondo.place(x=-1,y=-1)

    def botonEntendido(self):
        """Boton que acciona la busqueda de un archivo.
        """
        self.boton = Button(self.ayuda,text = "Entendido",command= self.ayuda.destroy)
        self.boton.place(x=64,y=395)
