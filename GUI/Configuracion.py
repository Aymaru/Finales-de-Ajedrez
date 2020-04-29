import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

from Main import centrar
from Main import leer_tablero
import os.path as path

from Juego import Juego
from GUI import Ajedrez

class Configuracion(tk.Frame):
    """Crea la ventana de configuracion de juego.
    """
    ###Constructor de la clase###
    def __init__(self,master):
        """Crea una instancia de la clase Configuracion
        """
        self.master = master
        self.dimensiones()          # Ajusta las dimensiones de la ventana.
        self.imagen()               # Agrega un fondo.
        self.componentes()
        centrar(self.master) # Centra la pantalla.
        self.pack()

    ##Ajuste UI###
    def dimensiones(self):
        """Define los aspectos de la ventana configuracion
        """        
        tk.Frame.__init__(self, self.master)
        self.master.title('Configuración')
        self.master.focus_set()           # Provoca que la ventana tome el focus.
        self.master.grab_set()      
        self.master.geometry("400x400")   # Tamaño de la ventana de configuración.
        

    def imagen(self):
        """Carga las imagenes a la ventana
        """
        self.fondo = tk.PhotoImage(file="./Imagenes/fondoConfig.gif") # Crea la imagen de fondo de la ventana inicio.
        self.lblFondo = tk.Label(self, image=self.fondo, background='black')
        self.lblFondo.grid(row=0, column=0)

    # ###SubComponentes de la Ventana###

    def componentes(self):
        self.btn_buscar_archivo_de_tablero()
        self.btn_finalizar()
        self.btn_turno()
        self.rb_tipo_de_juego()
        self.btn_comenzar()

    def btn_buscar_archivo_de_tablero(self):
        """Boton que acciona la busqueda de un archivo.
        """
        self.btn_buscar_archivo_de_tablero = tk.Button(self,text = "Buscar",command= self.buscar_archivo)
        self.btn_buscar_archivo_de_tablero.place(x=290,y=284)
        self.path_tablero = tk.StringVar()
        self.entry_archivo_de_juego = tk.Entry(self, textvariable=self.path_tablero,width=20,state="disabled")       
        self.entry_archivo_de_juego.place(x=155,y=285)
        self.scrollbar = tk.Scrollbar(self.entry_archivo_de_juego,orient="horizontal")
        self.scrollbar = tk.Scrollbar(orient="horizontal")        
        self.scrollbar.config(command=self.entry_archivo_de_juego.xview,width=13)
        self.scrollbar.place(x=155,y=305)
        
        
        self.entry_archivo_de_juego['xscrollcommand'] = self.scrollbar.set

    def btn_comenzar(self):
        """Boton que acciona la busqueda de un archivo.
        """
        self.boton = tk.Button(self,text = "Comenzar",command= self.comenzar)
        self.boton.place(x=95,y=352)

    def btn_finalizar(self):
        """Boton que acciona la busqueda de un archivo.
        """
        self.btn_finalizar = tk.Button(self,text = "Finalizar",command= self.salir)
        self.btn_finalizar.place(x=248,y=352)

    def buscar_archivo(self):
        """Buscar el archivo de arranca del juego.
        """
        self.archDialog = filedialog.askopenfilename(initialdir = "./Tableros", title = "Archivo de Inicio de Juego",defaultextension=".txt")
        self.path_tablero.set(self.archDialog)

    def rb_tipo_de_juego(self):
        self.tipo_de_juego = tk.IntVar()
        s = ttk.Style()
        s.theme_use('clam')
        s.configure('Wild.TRadiobutton', foreground='black')
        rb_tipo1 = tk.Radiobutton(self, variable=self.tipo_de_juego, value=1,padx=0,pady=0).place(x=95,y=179)
        rb_tipo2 = tk.Radiobutton(self, variable=self.tipo_de_juego, value=2,padx=0,pady=0).place(x=95,y=199)
        rb_tipo3 = tk.Radiobutton(self, variable=self.tipo_de_juego, value=3,padx=0,pady=0).place(x=95,y=219)

    def btn_turno(self):
        self.turno = tk.StringVar()
        self.turno.set("Blancas")
        self.equipo = tk.OptionMenu(self,self.turno,"Blancas","Negras")
        self.equipo.place(x=225,y=253)
    
    def colocar_turno(self,turno):
        if (turno == "Blancas"):
            return 'B'
        else:
            return 'N'
    ###Métodos especializados###   
    def salir(self):
        """Finaliza el programa
        """
        self.master.destroy()  # Fin del Juego.

    def obtener_piezas_iniciales(self):
        path_tablero = self.path_tablero.get()
        if  path_tablero == "":
            path_tablero = './Tableros/tablero_inicial.txt'
            self.piezas_iniciales = leer_tablero(path_tablero)
        elif path.exists(path_tablero):
            #agregar validacion de archivo de partida
            #No necesario??? se asume correcta la entrada
            self.piezas_iniciales = leer_tablero(path_tablero)
        else:
            #popup,diciendo que el archivo no existe
            print("error de archivo")
            self.salir()

    def comenzar(self):
        """ Verificiamos que los paramtreos de inicio del juego esten completos y inicia 
        """
        self.obtener_piezas_iniciales()
        self.master.juego = Juego.Juego(self.colocar_turno(self.turno.get()),self.piezas_iniciales,self.tipo_de_juego.get())
        self.destroy()
        Ajedrez.Ajedrez(self.master)
 
    # def popUp(self,tipo,mensaje):
    #     """Ventana que muestra un mensaje al usuario
    #     """
    #     self.pop = Toplevel()
    #     self.pop.focus_set()         # Provoca que la ventana tome el focus
    #     self.pop.grab_set()          # Desabilita todas las otras ventanas hasta que esta ventana sea destruida
    #     self.pop.geometry("412x138") # Tamaño de la ventana de inicio.
    #     if(tipo == 1):
    #         self.pop.title('Información')
    #         icono = PhotoImage(file="info.gif")           # Crea un icono de Informacion
    #     elif(tipo == 2):
    #         self.pop.title('Precaución')
    #         icono = PhotoImage(file="warning.gif")        # Crea un icono de Precaucion
    #     else:  
    #         self.pop.title('Error')
    #         icono = PhotoImage(file="error.gif")          # Crea un icono de Error
    #     lblIcono = Label(self.pop,image=icono, background='white')        # Agrega el icono en el fondo según el tipo de mensaje.
    #     boton = Button(self.pop,text = "Entendido",command = self.pop.destroy) # Opción de confirmación que entiende el mensaje. Se destruye la pantalla si se selecciona.
    #     boton.place(x=290,y=100)
    #     lblIcono.place(x=40,y=30)
    #     msg = Label(self.pop,text=mensaje, background='white') # Inserta el mensaje en la ventana pop.
    #     msg.place(x=110,y=32)
    #     centrar(self.pop)            # Centra la pantalla
    #     self.pop.wait_window()
