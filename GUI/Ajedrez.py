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
        self.events()
        centrar(self.master)        
        
        self.pack()
        self.canvas.pack()

        self.master.juego.set_movimientos_legales()
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
        self.inicializar_cantidad_de_capturas()
        self.colocar_piezas_en_tablero()
        self.generar_posiciones_de_capturas()
        self.colocar_piezas_capturadas()
        self.inicializar_dimensiones_de_tablero_en_pantalla()
        self.entry_movimiento()
        self.btn_mover_pieza()

    def dimensiones(self):
        """Define los aspectos de la ventana principal
        """
        tk.Frame.__init__(self, self.master)
        self.master.title("Instituto Tecnológico de Costa Rica")
        self.master.geometry("801x601") # Tamaño de la ventana de inicio.
        self.canvas = tk.Canvas(self, height=601, width=801, bg = "black")
        

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
    def entry_movimiento(self):        
        self.movimiento_casilla_inicial = tk.StringVar()
        self.movimiento_casilla_objetivo = tk.StringVar()
        self.entry_movimiento_casilla_inicial = tk.Entry(self,textvariable=self.movimiento_casilla_inicial,width=8)
        self.entry_movimiento_casilla_objetivo = tk.Entry(self,textvariable=self.movimiento_casilla_objetivo,width=8)
        self.canvas.create_window(195,543, anchor=tk.NW, window=self.entry_movimiento_casilla_inicial)
        self.canvas.create_window(255,543, anchor=tk.NW, window=self.entry_movimiento_casilla_objetivo)

    def btn_mover_pieza(self):
        self.btn_mover_pieza = tk.Button(self,text="Mover",command=self.regresar,width=8)
        #self.btn_mover_pieza.place(x=320,y=545)
        self.canvas.create_window(318,540,anchor=tk.NW,window=self.btn_mover_pieza)

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
                    self.contar_captura(pieza_actual)
                    pieza = Pieza.Pieza(self.canvas,pieza_actual)
                    pieza.calcular_posicion_en_tablero(casilla_actual)
                    pieza.colocar_imagen_en_tablero()
                    self.piezas.append(pieza)

    def inicializar_cantidad_de_capturas(self):
        self.cantidad_capturas_blancas_peones = 8
        self.cantidad_capturas_blancas_caballos = 2
        self.cantidad_capturas_blancas_alfiles = 2
        self.cantidad_capturas_blancas_torres = 2
        self.cantidad_capturas_blancas_dama = 1
        self.cantidad_capturas_negras_peones = 8
        self.cantidad_capturas_negras_caballos = 2
        self.cantidad_capturas_negras_alfiles = 2
        self.cantidad_capturas_negras_torres = 2
        self.cantidad_capturas_negras_dama = 1
    
    def contar_captura(self,pieza):
        if pieza == 1:
            self.cantidad_capturas_blancas_peones -= 1
        elif pieza == 2:
            self.cantidad_capturas_blancas_caballos -= 1
        elif pieza == 3:
            self.cantidad_capturas_blancas_alfiles -= 1
        elif pieza == 4:
            self.cantidad_capturas_blancas_torres -= 1
        elif pieza == 5:
            self.cantidad_capturas_blancas_dama -= 1
        elif pieza == -1:
            self.cantidad_capturas_negras_peones -= 1
        elif pieza == -2:
            self.cantidad_capturas_negras_caballos -= 1
        elif pieza == -3:
            self.cantidad_capturas_negras_alfiles -= 1
        elif pieza == -4:
            self.cantidad_capturas_negras_torres -= 1
        elif pieza == -5:
            self.cantidad_capturas_negras_dama -= 1

    def colocar_piezas_capturadas(self):

        if self.cantidad_capturas_blancas_peones > 0:
            i = 0
            for i in range(0,self.cantidad_capturas_blancas_peones):
                pieza = Pieza.Pieza(self.canvas,1)
                posicion_de_captura = self.posiciones_de_capturas_blancas_peones[i]
                pieza.colocar_posicion_en_tablero(posicion_de_captura)
                pieza.colocar_imagen_en_tablero()
                self.posiciones_de_capturas_blancas_peones[i] = pieza
        
        if self.cantidad_capturas_blancas_caballos > 0:
            i = 0
            for i in range(0,self.cantidad_capturas_blancas_caballos):
                pieza = Pieza.Pieza(self.canvas,2)
                posicion_de_captura = self.posiciones_de_capturas_blancas_caballos[i]
                pieza.colocar_posicion_en_tablero(posicion_de_captura)
                pieza.colocar_imagen_en_tablero()
                self.posiciones_de_capturas_blancas_caballos[i] = pieza
        
        if self.cantidad_capturas_blancas_alfiles > 0:
            i = 0
            for i in range(0,self.cantidad_capturas_blancas_alfiles):
                pieza = Pieza.Pieza(self.canvas,3)
                posicion_de_captura = self.posiciones_de_capturas_blancas_alfiles[i]
                pieza.colocar_posicion_en_tablero(posicion_de_captura)
                pieza.colocar_imagen_en_tablero()
                self.posiciones_de_capturas_blancas_alfiles[i] = pieza
        
        if self.cantidad_capturas_blancas_torres > 0:
            i = 0
            for i in range(0,self.cantidad_capturas_blancas_torres):
                pieza = Pieza.Pieza(self.canvas,4)
                posicion_de_captura = self.posiciones_de_capturas_blancas_torres[i]
                pieza.colocar_posicion_en_tablero(posicion_de_captura)
                pieza.colocar_imagen_en_tablero()
                self.posiciones_de_capturas_blancas_torres[i] = pieza
        
        if self.cantidad_capturas_blancas_dama > 0:
            i = 0
            for i in range(0,self.cantidad_capturas_blancas_dama):
                pieza = Pieza.Pieza(self.canvas,5)
                posicion_de_captura = self.posiciones_de_capturas_blancas_dama[i]
                pieza.colocar_posicion_en_tablero(posicion_de_captura)
                pieza.colocar_imagen_en_tablero()
                self.posiciones_de_capturas_blancas_dama[i] = pieza

        if self.cantidad_capturas_negras_peones > 0:
            i = 0
            for i in range(0,self.cantidad_capturas_negras_peones):
                pieza = Pieza.Pieza(self.canvas,-1)
                posicion_de_captura = self.posiciones_de_capturas_negras_peones[i]
                pieza.colocar_posicion_en_tablero(posicion_de_captura)
                pieza.colocar_imagen_en_tablero()
                self.posiciones_de_capturas_negras_peones[i] = pieza
        
        if self.cantidad_capturas_negras_caballos > 0:
            i = 0
            for i in range(0,self.cantidad_capturas_negras_caballos):
                pieza = Pieza.Pieza(self.canvas,-2)
                posicion_de_captura = self.posiciones_de_capturas_negras_caballos[i]
                pieza.colocar_posicion_en_tablero(posicion_de_captura)
                pieza.colocar_imagen_en_tablero()
                self.posiciones_de_capturas_negras_caballos[i] = pieza
        
        if self.cantidad_capturas_negras_alfiles > 0:
            i = 0
            for i in range(0,self.cantidad_capturas_negras_alfiles):
                pieza = Pieza.Pieza(self.canvas,-3)
                posicion_de_captura = self.posiciones_de_capturas_negras_alfiles[i]
                pieza.colocar_posicion_en_tablero(posicion_de_captura)
                pieza.colocar_imagen_en_tablero()
                self.posiciones_de_capturas_negras_alfiles[i] = pieza
        
        if self.cantidad_capturas_negras_torres > 0:
            i = 0
            for i in range(0,self.cantidad_capturas_negras_torres):
                pieza = Pieza.Pieza(self.canvas,-4)
                posicion_de_captura = self.posiciones_de_capturas_negras_torres[i]
                pieza.colocar_posicion_en_tablero(posicion_de_captura)
                pieza.colocar_imagen_en_tablero()
                self.posiciones_de_capturas_negras_torres[i] = pieza
        
        if self.cantidad_capturas_negras_dama > 0:
            i = 0
            for i in range(0,self.cantidad_capturas_negras_dama):
                pieza = Pieza.Pieza(self.canvas,-5)
                posicion_de_captura = self.posiciones_de_capturas_negras_dama[i]
                pieza.colocar_posicion_en_tablero(posicion_de_captura)
                pieza.colocar_imagen_en_tablero()
                self.posiciones_de_capturas_negras_dama[i] = pieza

    def generar_posiciones_de_capturas(self):
        ## Posiciones de Blancas Capturadas

        ##Peones
        # [ [211.98 , 460.32] , [211.98 ,  485.32] , [211.98 , 510.32] , [241.38 , 460.32] , [241.38 , 485.32] , [241.38 , 510.32] , [271.02 , 475.32] , [271.02 , 495.32] ]
        self.posiciones_de_capturas_blancas_peones = []
        self.posiciones_de_capturas_blancas_peones.append(Posicion.Posicion(211.98 , 460.32))
        self.posiciones_de_capturas_blancas_peones.append(Posicion.Posicion(211.98 , 485.32))
        self.posiciones_de_capturas_blancas_peones.append(Posicion.Posicion(211.98 , 510.32))
        self.posiciones_de_capturas_blancas_peones.append(Posicion.Posicion(241.38 , 460.32))
        self.posiciones_de_capturas_blancas_peones.append(Posicion.Posicion(241.38 , 485.32))
        self.posiciones_de_capturas_blancas_peones.append(Posicion.Posicion(241.38 , 510.32))
        self.posiciones_de_capturas_blancas_peones.append(Posicion.Posicion(271.02 , 475.32))
        self.posiciones_de_capturas_blancas_peones.append(Posicion.Posicion(271.02 , 495.32))

        ##Caballos
        # [ [140 , 458.90] , [140 ,  511.32] ]
        self.posiciones_de_capturas_blancas_caballos = []
        self.posiciones_de_capturas_blancas_caballos.append(Posicion.Posicion(140.00 , 458.90))
        self.posiciones_de_capturas_blancas_caballos.append(Posicion.Posicion(140.00 , 511.32))

        ##Alfiles
        # [ [181 , 473.32] , [181 ,  496.32] ]
        self.posiciones_de_capturas_blancas_alfiles = []
        self.posiciones_de_capturas_blancas_alfiles.append(Posicion.Posicion(181 , 473.32))
        self.posiciones_de_capturas_blancas_alfiles.append(Posicion.Posicion(181 , 496.32))

        ##Torres
        # [ [102.00 , 458.90] , [102.00 , 511.32] ]
        self.posiciones_de_capturas_blancas_torres = []
        self.posiciones_de_capturas_blancas_torres.append(Posicion.Posicion(102.00 , 458.90))
        self.posiciones_de_capturas_blancas_torres.append(Posicion.Posicion(102.00 , 511.32))

        ##Dama
        # [ [140 , 485.32] ]
        self.posiciones_de_capturas_blancas_dama = []
        self.posiciones_de_capturas_blancas_dama.append(Posicion.Posicion(140 , 485.32))

        ## Posiciones de Negras Capturadas

        ##Peones
        # [ [499.98 , 460.32] , [499.98 ,  485.32] , [499.98 , 510.32] , [529.38 , 460.32] , [529.38 , 485.32] , [529.38 , 510.32] , [559.02 , 475.32] , [559.02 , 495.32] ]
        self.posiciones_de_capturas_negras_peones = []
        self.posiciones_de_capturas_negras_peones.append(Posicion.Posicion(499.98 , 460.32))
        self.posiciones_de_capturas_negras_peones.append(Posicion.Posicion(499.98 , 485.32))
        self.posiciones_de_capturas_negras_peones.append(Posicion.Posicion(499.98 , 510.32))
        self.posiciones_de_capturas_negras_peones.append(Posicion.Posicion(529.38 , 460.32))
        self.posiciones_de_capturas_negras_peones.append(Posicion.Posicion(529.38 , 485.32))
        self.posiciones_de_capturas_negras_peones.append(Posicion.Posicion(529.38 , 510.32))
        self.posiciones_de_capturas_negras_peones.append(Posicion.Posicion(559.02 , 475.32))
        self.posiciones_de_capturas_negras_peones.append(Posicion.Posicion(559.02 , 495.32))

        ##Caballos
        # [ [425.90 , 458.90] , [425.90 ,  511.32] ]
        self.posiciones_de_capturas_negras_caballos = []
        self.posiciones_de_capturas_negras_caballos.append(Posicion.Posicion(425.90 , 458.90))
        self.posiciones_de_capturas_negras_caballos.append(Posicion.Posicion(425.90 , 511.32))

        ##Alfiles
        # [ [464.90 , 473.32] , [464.90 ,  496.32] ]
        self.posiciones_de_capturas_negras_alfiles = []
        self.posiciones_de_capturas_negras_alfiles.append(Posicion.Posicion(464.90 , 473.32))
        self.posiciones_de_capturas_negras_alfiles.append(Posicion.Posicion(464.90 ,  496.32))

        ##Torres
        # [ [387.90 , 458.90] , [387.90 ,  511.32] ]
        self.posiciones_de_capturas_negras_torres = []
        self.posiciones_de_capturas_negras_torres.append(Posicion.Posicion(387.90 , 458.90))
        self.posiciones_de_capturas_negras_torres.append(Posicion.Posicion(387.90 ,  511.32))

        ##Dama
        # [ [425.9 , 485.32] ]
        self.posiciones_de_capturas_negras_dama = []
        self.posiciones_de_capturas_negras_dama.append(Posicion.Posicion(425.90 , 485.32))

    def inicializar_dimensiones_de_tablero_en_pantalla(self):
        
        ## tam de cuadro = 48 46.25
        ## esquina superior izquierda = 26 103
        ## esquina superior derecha = 410 103
        ## esquina inferior izquierda = 26 473
        ## esquina inferior derecha = 410 473
        self.fila_inicial = 103
        self.fila_final = 472.9999
        self.columna_inicial = 26
        self.columna_final = 409.9999
        self.largo_fila = 46.25
        self.largo_columna = 48

    def generar_posicion_de_tablero(self,fila,columna):
        largo_filas = self.fila_final - self.fila_inicial 
        largo_columnas = self.columna_final - self.columna_inicial
        posicion_seleccionada = Posicion.Posicion(int((fila-self.fila_inicial)//self.largo_fila),int((columna-self.columna_inicial)//self.largo_columna))
        return posicion_seleccionada

    def validar_posicion_de_tablero_en_pantalla(self,fila,columna):
        return (self.number_between_range(fila,self.fila_inicial,self.fila_final) and self.number_between_range(columna,self.columna_inicial,self.columna_final))

    def number_between_range(self,number,first,last):
        #print("validar numero %d, inicio %d, final %d",(number,first,last))
        return (number >= first and number <= last)

    ##EVENTS

    def events(self):
        self.canvas.bind("<Button-1>", self.callback)
        self.canvas.pack()

    def callback(self,event):
        fila = event.y
        columna = event.x
        #print(len(self.master.juego.movimientos_legales))
        if self.validar_posicion_de_tablero_en_pantalla(fila, columna):
            posicion_seleccionada = self.generar_posicion_de_tablero(fila, columna)
            print(self.master.juego.casilla_seleccionada)
            if self.master.juego.casilla_seleccionada == None:
                self.master.juego.set_casilla_selecionada(posicion_seleccionada)
                if(self.master.juego.es_casilla_inicial_permitida()):
                    self.movimiento_casilla_inicial.set(self.master.juego.casilla_seleccionada.to_string())
                    print("??")
                else:
                    self.master.juego.limpiar_casilla_seleccionada()
                # if self.master.juego.casilla_seleccionada.equals(posicion_seleccionada):
                #     #self.master.juego.l
                # return
            else:
                self.master.juego.limpiar_casilla_seleccionada()
                return
            posicion_seleccionada.imprimir()
        print ("clicked at", event.x, event.y)
        return

    # def mostrarAyuda(self):
    #     Ayuda.Ayuda()
