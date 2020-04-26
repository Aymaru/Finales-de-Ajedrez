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
        self.entradaArch = tk.Entry(self, textvariable=self.path_tablero,width=13)
        self.entradaArch.place(x=155,y=280)

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
            self.piezas_iniciales = leer_tablero(path_tablero)
        else:
            #popup,diciendo que el archivo no existe
            print("error de archivo")
            self.salir()

    def comenzar(self):
        """ Verificiamos que los paramtreos de inicio del juego esten completos y inicia 
        """
        # self.tipo_de_juego.get()
        # #self.valor.get()
        # #self.path_tablero.get()
        # if self.tipo_de_juego.get() == 0:
        #     #popup, diciendo que se debe seleccionar un tipo de juego
        #     return
                
        self.obtener_piezas_iniciales()
        self.master.juego = Juego.Juego(self.turno.get(),self.piezas_iniciales,self.tipo_de_juego.get())
        self.destroy()
        Ajedrez.Ajedrez(self.master)
            #self.printearTablero()
            #Ajedrez(self.componentes[0],self.componentes[1],self.componentes[2],self.valor.get(),self.movIniciales)

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
        
    # def printearTablero(self):
    #     tablero = self.componentes[2]
    #     for cuadros in tablero.cuadros:
    #         print(cuadros)

    # def cagarArchivo(self):
    #     """Obtiene las piezas del archivo escogido
    #     """
    #     #print((self.path_tablero.get(),type(self.path_tablero)))
    #     # Verifica si el cuadro de texto no es vacio.
    #     # Si escribió en el cuadro de texto.
    #     # Usabamos un try para verificar si realmente existe el documento.
    #     try:
    #         archivo = open(self.path_tablero.get(), "r")  # Abre el archivo de inicio escrito o cargado por el jugador.
    #         datos = archivo.readlines()
    #         self.movIniciales = []
    #         for x in datos:
    #             for y in x.split():
    #                 if(len(y) == 5 and y[0] in Configuracion.C and
    #                    y[1] in Configuracion.P and y[2] in Configuracion.Fil and
    #                    y[3] in Configuracion.Col and y[4] in Configuracion.Fil):
    #                     self.movIniciales.append(y)
    #         self.movIniciales = list(dict.fromkeys(self.movIniciales)) # Elimino duplicados obteniendo los values del diccionario.
    #         if(self.movIniciales == []): # Verifica si el archivo no tenia movimientos en el formato correspondiente.
    #             # No ten[ia movimeintos.
    #             self.popUp(2,"[Error.B] ¡El archivo no posee movimientos iniciales!")
    #             int("AutoError")
    #         #print(self.movIniciales)
    #         #print(len(self.movIniciales))
    #         return True
    #     except:
    #         self.popUp(3,"Error, el archivo es incorrecto.")
    #         return False

    # def convertirLetra(self,letra):
    #     """Conviertiendo la letra en el numero de columna
    #     """
    #     nueva = ''
    #     if(letra == 'A'):
    #         nueva = 1
    #     elif(letra == 'B'):
    #         nueva = 2
    #     elif(letra == 'C'):
    #         nueva = 3
    #     elif(letra == 'D'):
    #         nueva = 4
    #     elif(letra == 'E'):
    #         nueva = 5
    #     elif(letra == 'F'):
    #         nueva = 6
    #     elif(letra == 'G'):
    #         nueva = 7
    #     else:
    #         nueva = 8
    #     return nueva
        
    # def cargarMovimientosTablero(self,mov):
    #     """
    #     """
    #     self.temporalC   = mov[0]           # C   = "NB"
    #     self.temporalP   = mov[1]           # P   = "RDTACP"
    #     self.temporalId  = int(mov[2])      # Id  = "12345678"
    #     self.temporalCol = mov[3]           # Col = "ABCDEFGH" -> "12345678"
    #     self.temporalFil = int(mov[4])      # Fil = "87654321"
    #     self.transformarInicalesAlTablero() # Procesa el movimiento

    # def transformarInicalesAlTablero(self):
    #     """ Método que transforma la C-P-Id-Col-Fil al Tablero
    #     """
    #     # Recorremos los movimientos inciales por cada componentes para verificar cual hace match.
    #     if(self.temporalC == "N"):                 # Movimiento en las piezas Negras
    #         if(self.equipoJug1 == "Negras"):
    #             # Movimiento del Jugador 1
    #             for pieza in self.componentes[0]:  # Primero estan las Negras
    #                 self.agregarPieza(pieza)
    #         else:
    #             # Movimiento del Jugador 2
    #             for pieza in self.componentes[1]:  # Segundo estan las Blancas
    #                 self.agregarPieza(pieza)
    #     else:                                      # Movimiento en las piezas Blancas
    #         if(self.equipoJug1 == "Blancas"):
    #             # Movimiento del Jugador 1  
    #             for pieza in self.componentes[0]: # Primero estan las Blancas
    #                 self.agregarPieza(pieza)
    #         else:
    #             # Movimiento del Jugador 2
    #             for pieza in self.componentes[1]: # Segundo estan las Negras
    #                 self.agregarPieza(pieza)

    # def agregarPieza(self,pieza):
    #     if(pieza.idChar == self.temporalP):  # Verifica la pieza
    #         if(pieza.id == self.temporalId): # Verifica el ID
    #             if(self.componentes[2].existePieza(self.temporalFil,self.convertirLetra(self.temporalCol)) == False):
    #                 self.componentes[2].agregarPieza(self.temporalFil,self.convertirLetra(self.temporalCol),pieza)
    #             else:                        # Existe una pieza previamente asignada
    #                 self.componentes[2].eliminarPieza(self.temporalFil,self.convertirLetra(self.temporalCol))
    #                 self.componentes[2].agregarPieza(self.temporalFil,self.convertirLetra(self.temporalCol),pieza)
    #         else:
    #             pass # Es la pieza, pero no con la identificación.
    #     else:
    #         pass # No es la pieza.
        
    # # def crearComponentes(self):
    # #     """self.componentes = [fichasJug1 = [], fichasJug2 = [], tablero]
    # #     """
    # #     # Se crean/inicializan las piezas del juego de ambos jugadores.
    # #     color = self.equipoJug1
    # #     self.componentes = []
    # #     fichas = []
    # #     for jugador in [1,2]:
    # #         fichas.append(Rey(jugador,color))
    # #         fichas.append(Dama(jugador,color))
    # #         for num in [1,2]:
    # #             fichas.append(Caballo(num,jugador,color))
    # #             fichas.append(Alfil(num,jugador,color))
    # #             fichas.append(Torre(num,jugador,color))         
    # #         for num in [1,2,3,4,5,6,7,8]:
    # #             fichas.append(Peon(num,jugador,color))
    # #         color = self.equipoJug2
    # #         self.componentes.append(fichas)
    # #         fichas = []  # Limpio la lista para cargar el conjunto de piezas del segundo jugador con su color respectivo
    # #     # Se crea el tablero del juego
    # #     self.componentes.append(Tablero(self.equipoJug1,self.equipoJug2))
    # #     #self.printearComponentes()

    # def printearComponentes(self):
    #     """Muestra los valores de los componentes.
    #     """
    #     for comp in range(0,3):
    #         print(self.componentes[comp])
