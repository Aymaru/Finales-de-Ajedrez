import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

from Main import centrar
from Main import leer_tablero
import os.path as path

from Juego import Juego
from GUI.TableroGUI import TableroGUI

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
        self.opt_menu_turno()
        self.opt_menu_jugador_1()
        self.rb_tipo_de_juego()
        self.btn_comenzar()

    def btn_buscar_archivo_de_tablero(self):
        """Boton que acciona la busqueda de un archivo.
        """
        self.btn_buscar_archivo_de_tablero = tk.Button(self,text = "Buscar",command= self.buscar_archivo,bd=0,bg="grey60")
        self.btn_buscar_archivo_de_tablero.place(x=282,y=284)
        self.path_tablero = tk.StringVar()
        self.entry_archivo_de_juego = tk.Entry(self, textvariable=self.path_tablero,width=20,state="disabled")       
        self.entry_archivo_de_juego.place(x=147,y=285)
        self.scrollbar = tk.Scrollbar(self.entry_archivo_de_juego,orient="horizontal")
        self.scrollbar = tk.Scrollbar(orient="horizontal")        
        self.scrollbar.config(command=self.entry_archivo_de_juego.xview,width=13)
        self.scrollbar.place(x=147,y=305)
        
        
        self.entry_archivo_de_juego['xscrollcommand'] = self.scrollbar.set

    def btn_comenzar(self):
        """Boton que acciona la busqueda de un archivo.
        """
        self.boton = tk.Button(self,text = "Comenzar",command= self.comenzar,bd=0,bg="grey60")
        self.boton.place(x=96,y=352)

    def btn_finalizar(self):
        """Boton que acciona la busqueda de un archivo.
        """
        self.btn_finalizar = tk.Button(self,text = "Finalizar",command= self.salir,bd=0,bg="grey60")
        self.btn_finalizar.place(x=253,y=352)

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
        
        self.rb_tipo1_img = tk.PhotoImage(file="./Imagenes/rb_jug_v_jug.gif") 
        self.rb_tipo2_img = tk.PhotoImage(file="./Imagenes/rb_jug_v_pc.gif")
        self.rb_tipo3_img = tk.PhotoImage(file="./Imagenes/rb_pc_v_pc.gif")
        #self.rb_tipo1_img = tk.PhotoImage(file="./Imagenes/bg transparente.gif")
        self.b_tipo1 = tk.Radiobutton(self, variable=self.tipo_de_juego, value=1,image=self.rb_tipo1_img,bd=0,bg="grey60").place(x=95,y=179)
        self.rb_tipo2 = tk.Radiobutton(self, variable=self.tipo_de_juego, value=2,image=self.rb_tipo2_img,bd=0,bg="grey60").place(x=95,y=199)
        self.rb_tipo3 = tk.Radiobutton(self, variable=self.tipo_de_juego, value=3,image=self.rb_tipo3_img,bd=0,bg="grey60").place(x=95,y=219)

    def opt_menu_turno(self):
        self.turno = tk.StringVar()
        self.turno.set("Blancas")
        self.opt_menu_turno = tk.OptionMenu(self,self.turno,"Blancas","Negras")
        self.opt_menu_turno.place(x=263,y=247)
    
    def opt_menu_jugador_1(self):
        self.jugador_1 = tk.StringVar()
        self.jugador_1.set("Blancas")
        self.opt_menu_jugador_1 = tk.OptionMenu(self,self.jugador_1,"Blancas","Negras")
        self.opt_menu_jugador_1.place(x=110,y=247)
    
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
        path_tablero_inicial = '/Tableros/tablero_inicial.txt'
        path_tablero = self.path_tablero.get()
        if  path_tablero == "":
            path_tablero = '.'+path_tablero_inicial
            self.piezas_iniciales = leer_tablero(path_tablero)
            self.es_juego_inicial = True
        elif path.exists(path_tablero):
            #agregar validacion de archivo de partida
            #No necesario??? se asume correcta la entrada
            if not path_tablero_inicial in path_tablero:
                self.es_juego_inicial = False
            
            self.piezas_iniciales = leer_tablero(path_tablero)
        else:
            #popup,diciendo que el archivo no existe
            print("error de archivo")
            self.salir()

    def comenzar(self):
        """ Verificiamos que los paramtreos de inicio del juego esten completos y inicia 
        """
        self.es_juego_inicial = True
        turno = self.colocar_turno(self.turno.get())
        jug_1 = self.colocar_turno(self.jugador_1.get())
        tipo_de_juego = self.tipo_de_juego.get()
        self.obtener_piezas_iniciales()
        #print("turno: %s, jug_1: %s", (turno,jug_1))
        self.destroy()
        self.master.juego = Juego.Juego(self.master,turno,jug_1,self.piezas_iniciales,tipo_de_juego,self.es_juego_inicial)
        self.master.GUI_ajedrez = TableroGUI(self.master)
        self.master.juego.ejecutar()
        
        
 
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
