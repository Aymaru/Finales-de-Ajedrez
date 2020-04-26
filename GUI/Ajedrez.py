import tkinter as tk
from tkinter import ttk

from Main import centrar
from GUI import Ayuda
from GUI import Configuracion
from GUI import Pieza
from Juego import Posicion

class Ajedrez(tk.Frame):
    """Crea la ventana de configuracion de juego.
    """

    ###Constructor de la clase###
    def __init__(self, master):
        """Crea una instancia de la clase Ajefrez
        """
        self.master = master
        
        self.dimensiones()
        
        self.componentes()
        centrar(self.master)
        self.pack()
        # self.tablero = tablero           # Cuadricula con cuadros[wight,height,]
        # self.piezasJug1 = piezasJug1  
        # self.piezasJug2 = piezasJug2
        # self.tipo = tipoJuego
        # self.movPreCargados = movPreCargados
        # self.principal = Toplevel()      # Crea una pantalla
        # self.dimensiones()
        # self.imagen()
        # self.cajaResultados()
        # self.botonIniciarJuego()
        # self.botonRegresarCofiguracion()
        # self.botonesRadio()
        # self.botonAyuda()
        # self.botonSiguienteJugador()
        # self.entradaSiguienteMov()
        # self.cargarPiezasPozo()
        # self.cargarPiezasTablero()
        # self.principal.mainloop()
        

    ###Ajuste UI###
    def componentes(self):
        self.imagen()
        self.btn_regresar()
        self.historial_movimientos()
        self.colocar_piezas_en_tablero()

    def dimensiones(self):
        """Define los aspectos de la ventana principal
        """
        tk.Frame.__init__(self, self.master)
        self.master.title("Instituto Tecnológico de Costa Rica")
        self.master.geometry("801x601") # Tamaño de la ventana de inicio.
        self.canvas = tk.Canvas(self, height=601, width=801, bg = "black")
        self.canvas.pack()

    def imagen(self):
        """Carga las imagenes a la ventana
        """
        self.fondo = tk.PhotoImage(file="./Imagenes/Tablero.gif") # Crea la imagen de fondo de la ventana inicio.
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.fondo)
        self.canvas.pack()
        
    def historial_movimientos(self):
        self.result = tk.Listbox(self, height=13, width=38,borderwidth=2.5,relief="raised", highlightthickness=1.5)
        self.canvas.create_window(545, 100, anchor=tk.NW, window=self.result)
        self.result.insert(tk.END,"            Historial de Movimientos")
        # if(self.movPreCargados != []):
        #     self.result.insert(tk.END,"Movimientos iniciales...")
        #     for i in self.movPreCargados:
        #         self.result.insert(tk.END, "  "+i)
        #     self.result.insert(tk.END,"Presione comenzar...")
        # else:
        #     self.result.insert(tk.END,"Sin movimientos inciales.")

    # def botonIniciarJuego(self):
    #     """Boton que acciona la busqueda de un archivo.
    #     """
    #     self.boton = Button(self.principal,text = "Comenzar")
    #     self.canvas.create_window(566,547, anchor=NW, window=self.boton)

    def btn_regresar(self):
        """Boton que acciona la busqueda de un archivo.
        """
        self.boton = tk.Button(self,text = "Regresar",command= self.regresar)
        self.canvas.create_window(695,547, anchor=tk.NW, window=self.boton)

    # def botonAyuda(self):
    #     """Boton que acciona la busqueda de un archivo.
    #     """
    #     self.boton = Button(self.principal,text = "Ayudar",command= self.mostrarAyuda)
    #     self.canvas.create_window(325,555, anchor=NW, window=self.boton)
    

    # def botonesRadio(self):
    #     self.legales = IntVar()
    #     self.defensa = IntVar()
    #     self.contrataque = IntVar()
    #     s = ttk.Style()
    #     s.theme_use('clam')
    #     s.configure('Wild.TRadiobutton', foreground='black')
    #     self.btncheck1 = Checkbutton(self.principal, variable=self.legales,padx=0,pady=0)
    #     self.btncheck2 = Checkbutton(self.principal, variable=self.defensa,padx=0,pady=0)
    #     self.btncheck3 = Checkbutton(self.principal, variable=self.contrataque,padx=0,pady=0)
    #     self.canvas.create_window(553,400, anchor=NW, window=self.btncheck1)
    #     self.canvas.create_window(553,437, anchor=NW, window=self.btncheck2)
    #     self.canvas.create_window(553,476, anchor=NW, window=self.btncheck3)
        
        
    # def botonSiguienteJugador(self):
    #     self.turno = Canvas(self.principal, height=20, width=80,borderwidth=2.5,relief="sunken", highlightthickness=1.5)
    #     self.turnoText = "Jugador 1"
    #     label_resultados = self.turno.create_text(46, 15, text=self.turnoText, font="Arial 15")
    #     self.canvas.create_window(83,544, anchor=NW, window=self.turno)

    # def entradaSiguienteMov(self):
    #     self.boton = Button(self.principal,text = "Aplicar")
    #     self.boton.place(x=350,y=548)
    #     self.movNuevo = StringVar()
    #     self.entradaArch = Entry(self.principal, textvariable=self.movNuevo,width=12)
    #     self.entradaArch.place(x=200,y=541)
    #     self.canvas.create_window(325,533, anchor=NW, window=self.boton)

    # ###Métodos especializados######Métodos especializados###
    def regresar(self):
        self.destroy()
        Configuracion.Configuracion(self.master)

    def colocar_piezas_en_tablero(self):
        self.piezas = []
        for fila in range(0,8):
            for columna in range(0,8):
                casilla_actual = Posicion.Posicion(fila,columna)
                pieza_actual = self.master.juego.tablero.obtener_pieza_de_casilla(casilla_actual)
                if pieza_actual == 0:
                    self.piezas.append(None)
                else:
                    pieza = Pieza.Pieza(self.canvas,pieza_actual)
                    pieza.calcular_posicion_en_tablero(casilla_actual)
                    pieza.colocar_imagen_en_tablero()
                    self.piezas.append(pieza)
                    

    # def mostrarAyuda(self):
    #     Ayuda.Ayuda()

    # def cargarPiezasPozo(self):
    #     """ self.tablero = tablero 
    #         self.piezasJug1 = piezasJug1
    #         self.piezasJug2 = piezasJug2
    #         self.tipo = tipoJuego
    #     """
    #     self.imagenJ1 = []
    #     self.imagenJ2 = []
    #     acum = 0
    #     for pieza in self.piezasJug1:
    #         self.imagenJ1.append(PhotoImage(file=pieza.imagen))
    #         pieza.idCanvas = self.canvas.create_image(pieza.posiciones[0],pieza.posiciones[1],image=self.imagenJ1[acum])
    #         acum = acum + 1
    #     acum = 0
    #     for pieza in self.piezasJug2:
    #         self.imagenJ2.append(PhotoImage(file=pieza.imagen))
    #         pieza.idCanvas = self.canvas.create_image(pieza.posiciones[0],pieza.posiciones[1],image=self.imagenJ2[acum])
    #         acum = acum + 1
            
    # def cargarPiezasTablero(self):
    #     for cuadro in self.tablero.cuadros:
    #         if(cuadro[2] != None):
    #             if(cuadro[2].jugador == 1):
    #                 for pieza in self.piezasJug1:
    #                     if(cuadro[2].id == pieza.id and cuadro[2].idChar == pieza.idChar):
    #                         print(cuadro)
    #                         fila = cuadro[4]
    #                         col = cuadro[5]
    #                         posXTablero = pieza.posiciones[2]
    #                         posYTablero = pieza.posiciones[3]
    #                         #print(col,posXTablero,fila,posYTablero)
    #                         movX = posXTablero + (col-1) * 48
    #                         movY = posYTablero + (fila-1) * 46
    #                         #print(movX,movY)
    #                         self.canvas.coords(pieza.idCanvas,(movX,movY))
    #             if(cuadro[2].jugador == 2):
    #                 for pieza in self.piezasJug2:
    #                     if(cuadro[2].id == pieza.id and cuadro[2].idChar == pieza.idChar):
    #                         print(cuadro)
    #                         fila = cuadro[4]
    #                         col = cuadro[5]
    #                         posXTablero = pieza.posiciones[2]
    #                         posYTablero = pieza.posiciones[3]
    #                         #print(col,posXTablero,fila,posYTablero)
    #                         movX = posXTablero + (col-1) * 48
    #                         movY = posYTablero + (fila-1) * 46
    #                         #print(movX,movY)
    #                         self.canvas.coords(pieza.idCanvas,(movX,movY))
    