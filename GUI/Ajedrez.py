import time

import tkinter as tk
from tkinter import ttk

from Main import centrar
from GUI import Ayuda
from GUI import Configuracion
from GUI import Pieza
from GUI import Label_IMG
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

        self.lbl_img_jaque = None
        self.lbl_img_turno = None

        self.componentes()        
        self.events()
        centrar(self.master)        
        
        
        #self.eliminar_lbl_img(self.lbl_img_jugador1)
        
        self.pack()
        self.canvas.pack()
        #self.master.juego.ejecutar()

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
        self.cargar_lbl_img_turno()
        self.cargar_lbl_img_jaque()
        self.colocar_lbl_img_jugadores()
        self.actualizar_estado_de_pantalla()

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

    def colocar_lbl_img_jugadores(self): ##35,450
        posicion_lbl_img_blancas = Posicion.Posicion(50,485)
        posicion_lbl_img_negras = Posicion.Posicion(340,485)
        if self.master.juego.tipo_de_juego == 1:
            self.lbl_img_jugador1 = Label_IMG.Label_IMG(self.canvas,"jugador1")
            self.lbl_img_jugador2 = Label_IMG.Label_IMG(self.canvas,"jugador2")
            if self.master.juego.J1 == "B":
                self.lbl_img_jugador1.colocar_posicion_en_tablero(posicion_lbl_img_blancas)
                self.lbl_img_jugador2.colocar_posicion_en_tablero(posicion_lbl_img_negras)
            else:
                self.lbl_img_jugador1.colocar_posicion_en_tablero(posicion_lbl_img_negras)
                self.lbl_img_jugador2.colocar_posicion_en_tablero(posicion_lbl_img_blancas)    

        elif self.master.juego.tipo_de_juego == 2:
            self.lbl_img_jugador1 = Label_IMG.Label_IMG(self.canvas,"jugador")
            self.lbl_img_jugador2 = Label_IMG.Label_IMG(self.canvas,"pc")
            if self.master.juego.J1 == "B":
                self.lbl_img_jugador1.colocar_posicion_en_tablero(posicion_lbl_img_blancas)
                self.lbl_img_jugador2.colocar_posicion_en_tablero(posicion_lbl_img_negras)
            else:
                self.lbl_img_jugador1.colocar_posicion_en_tablero(posicion_lbl_img_negras)
                self.lbl_img_jugador2.colocar_posicion_en_tablero(posicion_lbl_img_blancas)
        
        elif self.master.juego.tipo_de_juego == 3:
            self.lbl_img_jugador1 = Label_IMG.Label_IMG(self.canvas,"pc1")
            self.lbl_img_jugador2 = Label_IMG.Label_IMG(self.canvas,"pc2")
            if self.master.juego.J1 == "B":
                self.lbl_img_jugador1.colocar_posicion_en_tablero(posicion_lbl_img_blancas)
                self.lbl_img_jugador2.colocar_posicion_en_tablero(posicion_lbl_img_negras)
            else:
                self.lbl_img_jugador1.colocar_posicion_en_tablero(posicion_lbl_img_negras)
                self.lbl_img_jugador2.colocar_posicion_en_tablero(posicion_lbl_img_blancas)
 
        self.lbl_img_jugador1.colocar_imagen_en_tablero()
        self.lbl_img_jugador2.colocar_imagen_en_tablero()

    def eliminar_lbl_img(self,imagen):
        imagen.delete_image()
        

    def colocar_lbl_img(self,imagen):
        imagen.colocar_imagen_en_tablero()

    def entry_movimiento(self):        
        self.movimiento_casilla_inicial = tk.StringVar()
        self.movimiento_casilla_objetivo = tk.StringVar()
        self.entry_movimiento_casilla_inicial = tk.Entry(self,textvariable=self.movimiento_casilla_inicial,width=8)
        self.entry_movimiento_casilla_objetivo = tk.Entry(self,textvariable=self.movimiento_casilla_objetivo,width=8)
        self.canvas.create_window(195,543, anchor=tk.NW, window=self.entry_movimiento_casilla_inicial)
        self.canvas.create_window(255,543, anchor=tk.NW, window=self.entry_movimiento_casilla_objetivo)

    def btn_mover_pieza(self):
        self.btn_mover_pieza = tk.Button(self,text="Mover",command=self.realizar_movimiento,width=8,state=tk.DISABLED)
        #self.btn_mover_pieza.place(x=320,y=545)
        self.canvas.create_window(318,540,anchor=tk.NW,window=self.btn_mover_pieza)
    
    def realizar_movimiento(self):
        self.master.juego.queue.put(self.master.juego.movimiento_a_realizar)
        #time.sleep(1)
        self.master.after(100, self.master.juego.process_queue)
        #self.master.juego.ejecutar()

    def cargar_lbl_img_turno(self):
        posicion_lbl_img_turno = Posicion.Posicion(545,125)
        self.lbl_img_turno_blancas = Label_IMG.Label_IMG(self.canvas,"turno_blancas")
        self.lbl_img_turno_negras = Label_IMG.Label_IMG(self.canvas,"turno_negras")
        self.lbl_img_turno_blancas.colocar_posicion_en_tablero(posicion_lbl_img_turno)
        self.lbl_img_turno_negras.colocar_posicion_en_tablero(posicion_lbl_img_turno)
        self.colocar_lbl_img_turno()

    def colocar_lbl_img_turno(self):
        self.eliminar_lbl_img_turno()
        #print("lbl turno:%s",(self.master.juego.turno))
        if self.master.juego.turno == 'B':
            self.lbl_img_turno = self.lbl_img_turno_blancas
        elif self.master.juego.turno == 'N':
            self.lbl_img_turno = self.lbl_img_turno_negras
        self.colocar_lbl_img(self.lbl_img_turno)

    def eliminar_lbl_img_turno(self):
        if self.lbl_img_turno != None:
            self.eliminar_lbl_img(self.lbl_img_turno)
            self.lbl_img_turno = None

    def cargar_lbl_img_jaque(self):
        posicion_lbl_img_jaque = Posicion.Posicion(565,125)
        self.lbl_img_es_jaque = Label_IMG.Label_IMG(self.canvas,"jaque")
        self.lbl_img_jaque_mate = Label_IMG.Label_IMG(self.canvas,"jaque_mate")
        ##falta agregar tablas
        self.lbl_img_es_jaque.colocar_posicion_en_tablero(posicion_lbl_img_jaque)
        self.lbl_img_jaque_mate.colocar_posicion_en_tablero(posicion_lbl_img_jaque)
        self.colocar_lbl_img_jaque()

    def colocar_lbl_img_jaque(self):
        ##falta agregar tablas
        self.eliminar_lbl_img_jaque()
        if self.master.juego.es_jaque == True:
            
            if self.master.juego.jaque_mate == True:
                self.lbl_img_jaque = self.lbl_img_jaque_mate
            else:
                self.lbl_img_jaque = self.lbl_img_es_jaque

            self.colocar_lbl_img(self.lbl_img_jaque)
        elif self.master.juego.es_tablas == True:
            ## self.lbl_img_jaque = self.lbl_img_tablas
            self.colocar_lbl_img(self.lbl_img_jaque)
        
    def eliminar_lbl_img_jaque(self):
        if self.lbl_img_jaque != None:
            self.eliminar_lbl_img(self.lbl_img_jaque)
            self.lbl_img_jaque = None
     

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

    # def mover_pieza(self):
    #     casilla_inicial = self.master.juego.movimiento_a_realizar.casilla_inicial
    #     casilla_objetivo = self.master.juego.movimiento_a_realizar.casilla_objetivo
    #     pieza_a_mover = self.piezas[casilla_inicial.calcular_posicion_tablero()]
    #     self.piezas[casilla_inicial.calcular_posicion_tablero()] = None
    #     pieza_objetivo = self.piezas[casilla_objetivo.calcular_posicion_tablero()]
    #     pieza_a_mover.calcular_posicion_en_tablero(casilla_objetivo)
    #     pieza_a_mover.mover_pieza()
    #     print(pieza_objetivo)
    #     if pieza_objetivo != None:
    #         self.mover_captura_a_pozo(casilla_objetivo)
    #     self.piezas[casilla_objetivo.calcular_posicion_tablero()] = pieza_a_mover
    #     self.eliminar_lbl_img(self.lbl_img_turno)
    #     self.master.juego.mover_pieza()
    #     #self.turno.set(self.master.juego.turno_to_string())
    #     self.colocar_lbl_img_turno()
    #     self.movimiento_casilla_inicial.set("")
    #     self.movimiento_casilla_objetivo.set("")
    #     self.disable_btn_mover_pieza()

    def mover_pieza(self,movimiento):
        casilla_inicial = movimiento.casilla_inicial
        casilla_objetivo = movimiento.casilla_objetivo
        pieza_a_mover = self.piezas[casilla_inicial.calcular_posicion_tablero()]
        
        pieza_objetivo = self.piezas[casilla_objetivo.calcular_posicion_tablero()]
        pieza_a_mover.calcular_posicion_en_tablero(casilla_objetivo)
        pieza_a_mover.mover_pieza()
        

        if pieza_objetivo != None:
            self.mover_captura_a_pozo(casilla_objetivo)
        self.piezas[casilla_objetivo.calcular_posicion_tablero()] = pieza_a_mover
        self.piezas[casilla_inicial.calcular_posicion_tablero()] = None
        
        #self.master.juego.mover_pieza()
        #self.turno.set(self.master.juego.turno_to_string())
        ## separar en otra funcion
        # self.colocar_lbl_img_turno()
        # self.movimiento_casilla_inicial.set("")
        # self.movimiento_casilla_objetivo.set("")
        # self.disable_btn_mover_pieza()

    def actualizar_estado_de_pantalla(self):
        self.colocar_lbl_img_turno()
        self.colocar_lbl_img_jaque()
        self.movimiento_casilla_inicial.set("")
        self.movimiento_casilla_objetivo.set("")
        self.disable_btn_mover_pieza()

    def colocar_coronamiento(self,movimiento,pieza_de_coronamiento):
        casilla_inicial = movimiento.casilla_inicial
        casilla_objetivo = movimiento.casilla_objetivo
        color_de_pieza = self.master.juego.tablero.obtener_color_de_pieza(casilla_inicial)
        pieza_objetivo = self.piezas[casilla_objetivo.calcular_posicion_tablero()]
        if pieza_objetivo != None:
            self.mover_captura_a_pozo(casilla_objetivo)
        self.mover_captura_a_pozo(casilla_inicial)
        self.piezas[casilla_inicial.calcular_posicion_tablero()] = None
        pieza_coronamiento = Pieza.Pieza(self.canvas,pieza_de_coronamiento)
        pieza_coronamiento.calcular_posicion_en_tablero(casilla_objetivo)
        pieza_coronamiento.colocar_imagen_en_tablero()
        self.piezas[casilla_objetivo.calcular_posicion_tablero()] = pieza_coronamiento
    
    def colocar_enrroque(self,movimiento):
        casilla_inicial = movimiento.casilla_inicial
        casilla_objetivo = movimiento.casilla_objetivo
        pieza_a_mover = self.piezas[casilla_inicial.calcular_posicion_tablero()]
        pieza_a_mover.calcular_posicion_en_tablero(casilla_objetivo)
        pieza_a_mover.mover_pieza()
        
        self.piezas[casilla_inicial.calcular_posicion_tablero()] = None
        
        if casilla_objetivo.columna == 2:
            posicion_torre = Posicion.Posicion(casilla_inicial.fila,0)
            torre = self.piezas[posicion_torre.calcular_posicion_tablero()]
            
            self.piezas[posicion_torre.calcular_posicion_tablero()] = None
            posicion_torre.columna = 3
            torre.calcular_posicion_en_tablero(posicion_torre)
            torre.mover_pieza()
            self.piezas[posicion_torre.calcular_posicion_tablero()] = torre
           
        elif casilla_objetivo.columna == 6:
            posicion_torre = Posicion.Posicion(casilla_inicial.fila,7)
            torre = self.piezas[posicion_torre.calcular_posicion_tablero()]

            self.piezas[posicion_torre.calcular_posicion_tablero()] = None
            posicion_torre.columna = 5
            torre.calcular_posicion_en_tablero(posicion_torre)
            torre.mover_pieza()
            self.piezas[posicion_torre.calcular_posicion_tablero()] = torre
            

        self.piezas[casilla_objetivo.calcular_posicion_tablero()] = pieza_a_mover
        # if movimiento.casilla_objetivo.columna == 2:
        #     posicion_torre = Posicion.Posicion(movimiento.casilla_inicial.fila,0)
        #     pieza_torre = self.obtener_pieza_de_casilla(posicion_torre)
        #     self.limpiar_casilla(posicion_torre)
        #     posicion_torre.columna = 3
        #     self.colocar_pieza_en_casilla(pieza_torre,posicion_torre)
        #     ##enrroque largo

        # elif movimiento.casilla_objetivo.columna == 6:
        #     posicion_torre = Posicion.Posicion(movimiento.casilla_inicial.fila,7)
        #     pieza_torre = self.obtener_pieza_de_casilla(posicion_torre)
        #     self.limpiar_casilla(posicion_torre)
        #     posicion_torre.columna = 5
        #     self.colocar_pieza_en_casilla(pieza_torre,posicion_torre)
        #     ##enrroque largo

    def enable_btn_mover_pieza(self):
        self.btn_mover_pieza['state'] = tk.NORMAL

    def disable_btn_mover_pieza(self):
        self.btn_mover_pieza['state'] = tk.DISABLED

    def mover_captura_a_pozo(self,posicion):
        pieza = self.piezas[posicion.calcular_posicion_tablero()]
        
        if pieza.pieza == 1:
            for posicion_pozo in range(0,len(self.posiciones_de_capturas_blancas_peones)):
                if type(self.posiciones_de_capturas_blancas_peones[posicion_pozo]) == type(posicion):
                    pieza.colocar_posicion_en_tablero(self.posiciones_de_capturas_blancas_peones[posicion_pozo])
                    pieza.mover_pieza()
                    self.posiciones_de_capturas_blancas_peones[posicion_pozo] = pieza
                    break
                else:
                    continue
        elif pieza.pieza == 2:
            for posicion_pozo in range(0,len(self.posiciones_de_capturas_blancas_caballos)):
                if type(self.posiciones_de_capturas_blancas_caballos[posicion_pozo]) == type(posicion):
                    pieza.colocar_posicion_en_tablero(self.posiciones_de_capturas_blancas_caballos[posicion_pozo])
                    pieza.mover_pieza()
                    self.posiciones_de_capturas_blancas_caballos[posicion_pozo] = pieza
                    break
                else:
                    continue
        elif pieza.pieza == 3:
            for posicion_pozo in range(0,len(self.posiciones_de_capturas_blancas_alfiles)):
                if type(self.posiciones_de_capturas_blancas_alfiles[posicion_pozo]) == type(posicion):
                    pieza.colocar_posicion_en_tablero(self.posiciones_de_capturas_blancas_alfiles[posicion_pozo])
                    pieza.mover_pieza()
                    self.posiciones_de_capturas_blancas_alfiles[posicion_pozo] = pieza
                    break
                else:
                    continue
        elif pieza.pieza == 4:
            for posicion_pozo in range(0,len(self.posiciones_de_capturas_blancas_torres)):
                if type(self.posiciones_de_capturas_blancas_torres[posicion_pozo]) == type(posicion):
                    pieza.colocar_posicion_en_tablero(self.posiciones_de_capturas_blancas_torres[posicion_pozo])
                    pieza.mover_pieza()
                    self.posiciones_de_capturas_blancas_torres[posicion_pozo] = pieza
                    break
                else:
                    continue
        elif pieza.pieza == 5:
            for posicion_pozo in range(0,len(self.posiciones_de_capturas_blancas_dama)):
                if type(self.posiciones_de_capturas_blancas_dama[posicion_pozo]) == type(posicion):
                    pieza.colocar_posicion_en_tablero(self.posiciones_de_capturas_blancas_dama[posicion_pozo])
                    pieza.mover_pieza()
                    self.posiciones_de_capturas_blancas_dama[posicion_pozo] = pieza
                    break
                else:
                    continue
        elif pieza.pieza == -1:
            for posicion_pozo in range(0,len(self.posiciones_de_capturas_negras_peones)):
                if type(self.posiciones_de_capturas_negras_peones[posicion_pozo]) == type(posicion):
                    pieza.colocar_posicion_en_tablero(self.posiciones_de_capturas_negras_peones[posicion_pozo])
                    pieza.mover_pieza()
                    self.posiciones_de_capturas_negras_peones[posicion_pozo] = pieza
                    break
                else:
                    continue
        elif pieza.pieza == -2:
            for posicion_pozo in range(0,len(self.posiciones_de_capturas_negras_caballos)):
                if type(self.posiciones_de_capturas_negras_caballos[posicion_pozo]) == type(posicion):
                    pieza.colocar_posicion_en_tablero(self.posiciones_de_capturas_negras_caballos[posicion_pozo])
                    pieza.mover_pieza()
                    self.posiciones_de_capturas_negras_caballos[posicion_pozo] = pieza
                    break
                else:
                    continue
        elif pieza.pieza == -3:
            for posicion_pozo in range(0,len(self.posiciones_de_capturas_negras_alfiles)):
                if type(self.posiciones_de_capturas_negras_alfiles[posicion_pozo]) == type(posicion):
                    pieza.colocar_posicion_en_tablero(self.posiciones_de_capturas_negras_alfiles[posicion_pozo])
                    pieza.mover_pieza()
                    self.posiciones_de_capturas_negras_alfiles[posicion_pozo] = pieza
                    break
                else:
                    continue
        elif pieza.pieza == -4:
            for posicion_pozo in range(0,len(self.posiciones_de_capturas_negras_torres)):
                if type(self.posiciones_de_capturas_negras_torres[posicion_pozo]) == type(posicion):
                    pieza.colocar_posicion_en_tablero(self.posiciones_de_capturas_negras_torres[posicion_pozo])
                    pieza.mover_pieza()
                    self.posiciones_de_capturas_negras_torres[posicion_pozo] = pieza
                    break
                else:
                    continue
        elif pieza.pieza == -5:
            for posicion_pozo in range(0,len(self.posiciones_de_capturas_negras_dama)):
                if type(self.posiciones_de_capturas_negras_dama[posicion_pozo]) == type(posicion):
                    pieza.colocar_posicion_en_tablero(self.posiciones_de_capturas_negras_dama[posicion_pozo])
                    pieza.mover_pieza()
                    self.posiciones_de_capturas_negras_dama[posicion_pozo] = pieza
                    break
                else:
                    continue
    
    ##EVENTS

    def events(self):
        self.canvas.bind("<Button-1>", self.callback)
        self.canvas.pack()

    def callback(self,event):
        if self.master.juego.tipo_de_juego == 1 or (self.master.juego.tipo_de_juego == 2 and not self.master.juego.es_turno_pc):
            fila = event.y
            columna = event.x
            #print(len(self.master.juego.movimientos_legales))
            if self.validar_posicion_de_tablero_en_pantalla(fila, columna):
                posicion_seleccionada = self.generar_posicion_de_tablero(fila, columna)
                #print(self.master.juego.casilla_inicial)
                
                if self.master.juego.casilla_inicial == None:
                    self.master.juego.set_casilla_inicial(posicion_seleccionada)
                    if(self.master.juego.es_casilla_inicial_permitida()):
                        self.movimiento_casilla_inicial.set(self.master.juego.casilla_inicial.to_string())
                        #print("set casilla inicial")
                    else:
                        self.master.juego.limpiar_casilla_inicial()
                        self.movimiento_casilla_inicial.set("")
                    
                else:
                    
                    if self.master.juego.casilla_objetivo == None:
                    
                        if self.master.juego.casilla_inicial.equals(posicion_seleccionada):
                            self.movimiento_casilla_inicial.set("")
                            self.master.juego.limpiar_casilla_inicial()
                            #print("selecciona misma posicion inicial, entonces la quita")
                        else:
                            self.master.juego.set_casilla_objetivo(posicion_seleccionada)
                            if self.master.juego.es_movimiento_a_realizar_legal():
                                self.enable_btn_mover_pieza()
                                self.movimiento_casilla_objetivo.set(self.master.juego.casilla_objetivo.to_string())
                                #print("set casilla objetivo")
                            else:
                                self.master.juego.limpiar_casilla_objetivo()
                                self.master.juego.limpiar_movimiento_a_realizar()
                                self.movimiento_casilla_objetivo.set("")
                    else:
                        if self.master.juego.casilla_objetivo.equals(posicion_seleccionada):
                            self.movimiento_casilla_objetivo.set("")
                            self.master.juego.limpiar_casilla_objetivo()
                            self.master.juego.limpiar_movimiento_a_realizar()
                            self.disable_btn_mover_pieza()
                            #print("selecciona misma posicion objetivo, entonces la quita")

                    ##verificar si la posicion seleccionada es igual a la casilla seleccionada 
                    #self.master.juego.limpiar_casilla_seleccionada()
                    
                #posicion_seleccionada.imprimir()
        #print ("clicked at", event.x, event.y)
        return

    # def mostrarAyuda(self):
    #     Ayuda.Ayuda()
