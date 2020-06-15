
import time
import copy

##Import de TKinter
import tkinter as tk
from tkinter import ttk

##Import de Main
from Main import centrar

##Imports de Juego
from Juego.Movimiento import Movimiento
from Juego.Posicion import Posicion
from Juego.Tipos import Turno
from Juego.Tipos import Pieza as TipoPieza
from Juego.Tipos import Turno
from Juego.Tipos import Casilla as TCasilla


##Imports de GUI
#from GUI.Configuracion import Configuracion
from GUI.Label_IMG import Label_IMG
from GUI.Casilla import Casilla
from GUI.Pieza import Pieza
from GUI import Configuracion


##Interfaz del Tablero
class TableroGUI(tk.Frame):

    def __init__(self,master):
        
        self.master = master ##Instancia del master
        tk.Frame.__init__(self, self.master) ##instancia el frame
        self.master.title("Instituto Tecnológico de Costa Rica")
        self.master.geometry("1400x900") # Tamaño de la ventana de inicio.

        centrar(self.master)

        ## ***** Variables de los componentes *****
        self.__posicion_inicial_tablero = Posicion(50,50)
        self.__posicion_final_tablero = Posicion(850,850)
        self.__largo_casilla = Posicion(100,100) ##Largo de fila, largo de columna

        self.__piezas = [] ##Guarda las imagenes de las piezas en pantalla
        self.__casillas = [] ##Guarda los dibujos de las casillas
        self.__casillas_mov_anterior = [] ##Guarda los dibujos de las casillas que marcan el movimiento anterior

        self.__ultima_posicion = None
        self.__esperando_movimiento = False

        self.__posiciones_de_captura = {
            Turno.BLANCAS: {
                TipoPieza.PEON : [
                    Posicion(195 , 993),
                    Posicion(195 , 1023),
                    Posicion(195 , 1051),
                    Posicion(230 , 1005),
                    Posicion(230 , 1041),
                    Posicion(265 , 993),
                    Posicion(265 , 1023),
                    Posicion(265 , 1051)
                ],
                TipoPieza.CABALLO : [
                    Posicion(125 , 993),
                    Posicion(125 , 1051)
                ],
                TipoPieza.ALFIL : [
                    Posicion(160 , 1005),
                    Posicion(160 , 1041)
                ],
                TipoPieza.TORRE : [
                    Posicion(90 , 1005),
                    Posicion(90 , 1041)
                ],
                TipoPieza.DAMA : [ Posicion(125 , 1020) ]
            },
            Turno.NEGRAS: {
                TipoPieza.PEON : [
                    Posicion(865 , 993),
                    Posicion(865 , 1023),
                    Posicion(865 , 1051),
                    Posicion(900 , 1005),
                    Posicion(900 , 1041),
                    Posicion(935 , 993),
                    Posicion(935 , 1023),
                    Posicion(935 , 1051),
                ],
                TipoPieza.CABALLO : [
                    Posicion(795 , 993),
                    Posicion(795 , 1051)
                ],
                TipoPieza.ALFIL : [
                    Posicion(830 , 1005),
                    Posicion(830 ,  1041)
                ],
                TipoPieza.TORRE : [
                    Posicion(760 , 1005),
                    Posicion(760 ,  1041)
                ],
                TipoPieza.DAMA : [ Posicion(795 , 1020) ]
            } 
        }

        self.__cantidad_de_capturas = {
            Turno.BLANCAS: {
                TipoPieza.PEON: 8,
                TipoPieza.CABALLO: 2,
                TipoPieza.ALFIL: 2,
                TipoPieza.TORRE: 2,
                TipoPieza.DAMA: 1,
            },
            Turno.NEGRAS: {
                TipoPieza.PEON: 8,
                TipoPieza.CABALLO: 2,
                TipoPieza.ALFIL: 2,
                TipoPieza.TORRE: 2,
                TipoPieza.DAMA: 1,
            }
        }
        posicion_lbl_img_turno = Posicion(0,0)

        ## ***** Componentes de la pantalla *****

        self.__main_canvas = tk.Canvas(self, height=1024, width=1400, bg = "black") ## Main canvas
        ##Imagen de fondo
        self._lbl_img_fondo = tk.PhotoImage(file="./Imagenes/tablero_nuevo.gif")
        ##Crea la imagen en el main canvas
        self.__main_canvas.create_image(0, 0, anchor=tk.NW, image=self._lbl_img_fondo)

        

        lbl_img_leyenda_turno = self.__turno_to_string()
        print("turno leyenda %s" % lbl_img_leyenda_turno)

        posicion_lbl_img_leyenda_superior = Posicion(25,425)
        self.__lbl_img_leyenda_superior = Label_IMG(self.__main_canvas,lbl_img_leyenda_turno+"_leyenda_superior")
        self.__lbl_img_leyenda_superior.colocar_posicion_en_tablero(posicion_lbl_img_leyenda_superior)
        
        posicion_lbl_img_leyenda_inferior = Posicion(875,425)
        self.__lbl_img_leyenda_inferior = Label_IMG(self.__main_canvas,lbl_img_leyenda_turno+"_leyenda_inferior")
        self.__lbl_img_leyenda_inferior.colocar_posicion_en_tablero(posicion_lbl_img_leyenda_inferior)

        posicion_lbl_img_leyenda_izquierda = Posicion(425,25)
        self.__lbl_img_leyenda_izquierda = Label_IMG(self.__main_canvas,lbl_img_leyenda_turno+"_leyenda_lateral_izq")
        self.__lbl_img_leyenda_izquierda.colocar_posicion_en_tablero(posicion_lbl_img_leyenda_izquierda)

        posicion_lbl_img_leyenda_derecha = Posicion(425,875)
        self.__lbl_img_leyenda_derecha = Label_IMG(self.__main_canvas,lbl_img_leyenda_turno+"_leyenda_lateral_der")
        self.__lbl_img_leyenda_derecha.colocar_posicion_en_tablero(posicion_lbl_img_leyenda_derecha)
        
        self.__colocar_lbl_img(self.__lbl_img_leyenda_superior)
        self.__colocar_lbl_img(self.__lbl_img_leyenda_inferior)
        self.__colocar_lbl_img(self.__lbl_img_leyenda_izquierda)
        self.__colocar_lbl_img(self.__lbl_img_leyenda_derecha)

        self.__lbl_img_jugadores_posiciones = {
            Turno.BLANCAS: Posicion(190,1080),
            Turno.NEGRAS: Posicion(715,1080)
        }
        self.__lbl_img_jugador_1 = None
        self.__lbl_img_jugador_2 = None
        self.__cargar_lbl_img_jugadores() #
        self.__colocar_lbl_img_jugadores() #

        lbl_img_jaque_posicion = Posicion(305,1270)
        self.__lbl_img_jaque = Label_IMG(self.__main_canvas,"jaque")
        self.__lbl_img_jaque.resize(4,4)
        self.__lbl_img_jaque.colocar_posicion_en_tablero(lbl_img_jaque_posicion)

        self.__lbl_img_jaque_mate = Label_IMG(self.__main_canvas,"jaque_mate")
        self.__lbl_img_jaque_mate.colocar_posicion_en_tablero(lbl_img_jaque_posicion)
        self.__lbl_img_jaque_mate.resize(4,4)   

        self.__lbl_img_tablas = None
        self.__lbl_img_estado = None
    
        self.__colocar_lbl_img_jaque() #
        
        lbl_img_turno_posicion = Posicion(325,1030)
        
        self.__lbl_img_turno_blancas = Label_IMG(self.__main_canvas,"turno_blancas")
        self.__lbl_img_turno_blancas.resize(3,3)
        self.__lbl_img_turno_blancas.colocar_posicion_en_tablero(lbl_img_turno_posicion)
        
        self.__lbl_img_turno_negras = Label_IMG(self.__main_canvas,"turno_negras")
        self.__lbl_img_turno_negras.colocar_posicion_en_tablero(lbl_img_turno_posicion)
        self.__lbl_img_turno_negras.resize(3,3)

        self.__lbl_img_turno = None
        
        self.__colocar_lbl_img_turno() #
        self.__colocar_piezas() #
        self.__colocar_piezas_capturadas() #

        #460.270
        ##Text Box Historial de movimientos
        self.__txt_historial = tk.Text(self.__main_canvas,height=15, width=55)
        self.__txt_historial.place(x=932,y=400)
        
        ##Botones
        self.btn_finalizar = tk.Button(self,text = "SALIR",command= self.__salir,bd=0,bg="grey60",width=20,height=5)
        self.btn_finalizar.place(x=1225,y=800)

        self.btn_finalizar = tk.Button(self,text = "REGRESAR",command= self.__regresar,bd=0,bg="grey60",width=20,height=5)
        self.btn_finalizar.place(x=1025,y=800)
        ##Events
        self.__main_canvas.bind("<Button-1>",self.__on_click_callback)
        self.__main_canvas.bind("<B1-Motion>",self.__on_motion_callback)
        self.__main_canvas.bind("<ButtonRelease-1>",self.__on_release_callback)

        self.pack()
        self.__main_canvas.pack()
    
    def __regresar(self):
        self.master.juego.guardar_log()
        self.destroy()
        Configuracion.Configuracion(self.master)
    
    def __salir(self):
        self.master.juego.guardar_log()
        self.master.destroy()
        
    def __eliminar_lbl_img(self,imagen):
        imagen.delete_image()
        
    def __colocar_lbl_img(self,imagen):
        imagen.colocar_imagen_en_tablero()

    def __turno_to_string(self):
        turno = self.__get_turno(self.master.juego.J1)
        if turno == Turno.BLANCAS:
            return 'b'
        elif turno == Turno.NEGRAS:
            return 'n'
        else:
            print("error lblimg leyenda superior")

    def __get_turno(self,turno):
        print("get turno :", turno)
        if turno == "B":
            return Turno.BLANCAS
        elif turno == "N":
            return Turno.NEGRAS
        else:
            print("error get turno")

    def __cargar_lbl_img_jugadores(self):
        if self.master.juego.tipo_de_juego == 1:
            self.__lbl_img_jugador_1 = Label_IMG(self.__main_canvas,"jugador1")
            self.__lbl_img_jugador_2 = Label_IMG(self.__main_canvas,"jugador2")
            
        elif self.master.juego.tipo_de_juego == 2:
            self.__lbl_img_jugador_1 = Label_IMG(self.__main_canvas,"jugador")
            self.__lbl_img_jugador_2 = Label_IMG(self.__main_canvas,"pc")
            
        elif self.master.juego.tipo_de_juego == 3:
            self.__lbl_img_jugador_1 = Label_IMG(self.__main_canvas,"pc1")
            self.__lbl_img_jugador_2 = Label_IMG(self.__main_canvas,"pc2")
        else:
            print("error con cargar lbl img jugadores")  

    def __colocar_lbl_img_jugadores(self):
        self.__lbl_img_jugador_1.resize(4,4)
        self.__lbl_img_jugador_2.resize(4,4)
        if self.master.juego.J1 == "B":
            self.__lbl_img_jugador_1.colocar_posicion_en_tablero(self.__lbl_img_jugadores_posiciones[Turno.BLANCAS])
            self.__lbl_img_jugador_2.colocar_posicion_en_tablero(self.__lbl_img_jugadores_posiciones[Turno.NEGRAS])
        else:
            self.__lbl_img_jugador_1.colocar_posicion_en_tablero(self.__lbl_img_jugadores_posiciones[Turno.NEGRAS])
            self.__lbl_img_jugador_2.colocar_posicion_en_tablero(self.__lbl_img_jugadores_posiciones[Turno.BLANCAS])
        
        self.__colocar_lbl_img(self.__lbl_img_jugador_1)
        self.__colocar_lbl_img(self.__lbl_img_jugador_2)

    def __colocar_lbl_img_turno(self):
        turno = self.__get_turno(self.master.juego.turno)

        if self.__lbl_img_turno != None:
            self.__eliminar_lbl_img(self.__lbl_img_turno)
            self.__lbl_img_turno = None

        if turno == Turno.BLANCAS:
            self.__lbl_img_turno = self.__lbl_img_turno_blancas

        elif turno == Turno.NEGRAS:
            self.__lbl_img_turno = self.__lbl_img_turno_negras
        
        self.__colocar_lbl_img(self.__lbl_img_turno)

    def __colocar_lbl_img_jaque(self):
        ##falta agregar tablas
        if self.__lbl_img_estado != None:
            self.__eliminar_lbl_img(self.__lbl_img_estado)
            self.__lbl_img_estado = None

        if self.master.juego.es_jaque == True:
            
            if self.master.juego.jaque_mate == True:
                self.__lbl_img_estado = self.__lbl_img_jaque_mate
            else:
                self.__lbl_img_estado = self.__lbl_img_jaque

            self.__colocar_lbl_img(self.__lbl_img_estado)
        elif self.master.juego.es_tablas == True:
            ## self.__lbl_img_estado = self.__lbl_img_tablas
            ## self.colocar_lbl_img(self.__lbl_img_estado)
            print("Tablas no implementado")

    def __colocar_piezas(self):
        
        for fila in range(0,8):
            for columna in range(0,8):
                tmp_posicion = Posicion(fila,columna)
                pieza_actual = self.master.juego.tablero.obtener_pieza_de_casilla(tmp_posicion)
                if pieza_actual == 0:
                    self.__piezas.append(None)
                else:
                    tmp_pieza = self.__obtener_tipo_de_pieza(pieza_actual)
                    tmp_color = self.__obtener_color_de_pieza(pieza_actual)
                    if tmp_pieza != TipoPieza.REY:
                        self.__cantidad_de_capturas[tmp_color][tmp_pieza] -= 1

                    pieza = Pieza(self.__main_canvas,pieza_actual)
                    pieza.calcular_posicion_en_tablero(tmp_posicion)
                    pieza.colocar_imagen_en_tablero()
                    self.__piezas.append(pieza)
    
    def __obtener_tipo_de_pieza(self,pieza):
        pieza = abs(pieza)
        if pieza == 1:
            return TipoPieza.PEON
        elif pieza == 2:
            return TipoPieza.CABALLO
        elif pieza == 3:
            return TipoPieza.ALFIL
        elif pieza == 4:
            return TipoPieza.TORRE
        elif pieza == 5:
            return TipoPieza.DAMA
        elif pieza == 6:
            return TipoPieza.REY
        else:
            return None
    
    def __obtener_color_de_pieza(self,pieza):
        if pieza > 0:
            return Turno.BLANCAS
        elif pieza < 0:
            return Turno.NEGRAS
        else:
            return None

    def __colocar_piezas_capturadas(self):

        for color in self.__cantidad_de_capturas.keys():
            for pieza in self.__cantidad_de_capturas[color].keys():
                tmp_cantidad_de_capturas = self.__cantidad_de_capturas[color][pieza]
                if tmp_cantidad_de_capturas > 0:
                    for index in range(0,tmp_cantidad_de_capturas):
                        
                        img_pieza = Pieza(self.canvas,self.__convertir_tipo_y_color_de_pieza_a_pieza(color,pieza))
                        posicion_de_captura = self.__posiciones_de_captura[color][pieza][index]
                        img_pieza.colocar_posicion_en_tablero(posicion_de_captura)
                        img_pieza.colocar_imagen_en_tablero()
                        self.__posiciones_de_captura[color][pieza] = img_pieza
    
    def __realizar_movimiento(self):
        self.master.juego.queue.put(self.master.juego.movimiento_a_realizar)
        self.master.after(100, self.master.juego.process_queue)

    ####
    ## ***** Callbacks *****
    ####

    ## On Click
    ##Selecciona un espacio del tablero, 
    ##Si se selecciona una pieza del color del turno que mueve,
    ##Se verifica que sea una pieza con al menos un movimiento valido,
    ##Si cumple, se coloca como casilla inicial y se marcan los posibles movimientos en el tablero
    ##Si se selecciona una pieza del color contrario al turno, una casilla vacia o una pieza del color del turno sin movimientos legales,
    ##No se realiza ninguna accion
    ##Si ya se encuentra seleccionada una casilla, y la casilla seleccionada se encuentra como la casilla objetivo de un movimiento valido
    ##junto con la casilla previamente seleccionada, se procede a realizar el movimiento
    def __on_click_callback(self,event):
        print ("clicked at", event.x, event.y)
       
        if self.master.juego.tipo_de_juego == 1 or (self.master.juego.tipo_de_juego == 2 and not self.master.juego.es_turno_pc):
            fila = event.y
            columna = event.x
            if self.__validar_posicion_de_tablero_en_pantalla(fila, columna):
                posicion_seleccionada = self.__generar_posicion_de_tablero(fila, columna)
                print("Posicion valida del tablero")
                posicion_seleccionada.imprimir()
                if self.master.juego.casilla_inicial == None:
                    print("casilla inicial vacia, set casilla inicial")
                    self.master.juego.set_casilla_inicial(posicion_seleccionada)
                    self.__ultima_posicion = Posicion(fila,columna)
                    if not ( self.master.juego.es_casilla_inicial_permitida() ) :
                        self.master.juego.limpiar_casilla_inicial()
                        self.limpiar_casillas()
                        print("casilla inicial no permitida, clear casilla inicial")
                        return
                    else:
                        self.marcar_movimientos_de_pieza(posicion_seleccionada)
                else:
                    print("casilla inicial seteada, set casilla objetivo")
                    self.master.juego.set_casilla_objetivo(posicion_seleccionada)
                    if self.master.juego.es_movimiento_a_realizar_legal():
                        self.__realizar_movimiento()
                    self.limpiar_casillas()
                    self.master.juego.limpiar_casilla_inicial()
                    self.master.juego.limpiar_casilla_objetivo()
                    self.master.juego.limpiar_movimiento_a_realizar()
                    return
   

    def __on_motion_callback(self,event):
        self.__esperando_movimiento = True
        tmp_casilla_inicial = self.master.juego.casilla_inicial
        if  tmp_casilla_inicial != None:
            tmp_img = self.__piezas[tmp_casilla_inicial.calcular_posicion_tablero()]
            self.__main_canvas.move(tk.CURRENT,event.x - self.__ultima_posicion.columna,event.y - self.__ultima_posicion.fila)
            self.__ultima_posicion = Posicion(event.y,event.x)
            #self.master.update()
        return

    def __on_release_callback(self,event):
        
        if not self.__esperando_movimiento:
            return
        print("on release")
        tmp_casilla_inicial = self.master.juego.casilla_inicial
        if  tmp_casilla_inicial == None:
            return

        fila = event.y
        columna = event.x
        movimiento_invalido = False
        if self.__validar_posicion_de_tablero_en_pantalla(fila, columna):
            posicion_seleccionada = self.__generar_posicion_de_tablero(fila, columna)
            self.master.juego.set_casilla_objetivo(posicion_seleccionada)
            if self.master.juego.es_movimiento_a_realizar_legal():
                tmp_img = self.__piezas[ self.master.juego.casilla_inicial.calcular_posicion_tablero() ]
                tmp_img.calcular_posicion_en_tablero(self.master.juego.casilla_objetivo)
                self.__realizar_movimiento()                
            else:
                movimiento_invalido = True
        else:
            movimiento_invalido = True
        
        if movimiento_invalido:
            tmp_img = self.__piezas[self.master.juego.casilla_inicial.calcular_posicion_tablero()]
            tmp_img.calcular_posicion_en_tablero(self.master.juego.casilla_inicial)
            tmp_img.mover_pieza()
            self.master.update()
        
        self.limpiar_casillas()
        self.master.juego.limpiar_casilla_inicial()
        self.master.juego.limpiar_casilla_objetivo()
        self.master.juego.limpiar_movimiento_a_realizar()
        self.__esperando_movimiento = False
        self.__ultima_posicion = None

    ##Funcion tmp que convierte un enum de tipo de pieza a su correspondiente valor
    ##numerico mientras actualizo el resto de clases.
    def __convertir_tipo_y_color_de_pieza_a_pieza(self,color,pieza):
        tmp_pieza = 0
        if pieza == TipoPieza.PEON:
            tmp_pieza = 1
        elif pieza == TipoPieza.CABALLO:
            tmp_pieza = 2
        elif pieza == TipoPieza.ALFIL:
            tmp_pieza = 3
        elif pieza == TipoPieza.TORRE:
            tmp_pieza = 4
        elif pieza == TipoPieza.DAMA:
            tmp_pieza = 5
        elif pieza == TipoPieza.REY:
            tmp_pieza = 6
        
        if color == Turno.NEGRAS:
            tmp_pieza *= -1
        
        return tmp_pieza
        

    def __generar_posicion_de_tablero(self,fila,columna):
        largo_filas = self.__posicion_final_tablero.fila - self.__posicion_inicial_tablero.fila
        largo_columnas = self.__posicion_final_tablero.columna - self.__posicion_inicial_tablero.columna
        print("generar posicion largo fila: %d, largo columna: %d" % (largo_filas,largo_columnas))
        posicion_seleccionada = Posicion(int((fila-self.__posicion_inicial_tablero.fila)//self.__largo_casilla.fila),int((columna-self.__posicion_inicial_tablero.columna)//self.__largo_casilla.columna))
        return posicion_seleccionada

    def __validar_posicion_de_tablero_en_pantalla(self,fila,columna):
        return (self.__number_between_range(fila,self.__posicion_inicial_tablero.fila,self.__posicion_final_tablero.fila) and self.__number_between_range(columna,self.__posicion_inicial_tablero.columna,self.__posicion_final_tablero.columna))

    def __number_between_range(self,number,first,last):
        #print("validar numero %d, inicio %d, final %d",(number,first,last))
        return (number >= first and number <= last)

    def __animacion_de_movimiento(self,movimiento):

        pieza = self.__obtener_tipo_de_pieza(self.master.juego.tablero.obtener_pieza_de_casilla(movimiento.casilla_inicial))
        if pieza == None:
            return

        casilla_inicial = copy.deepcopy(movimiento.casilla_inicial)
        casilla_objetivo = copy.deepcopy(movimiento.casilla_objetivo)
        tmp_imagen = self.__piezas[movimiento.casilla_inicial.calcular_posicion_tablero()]
        direccion_fila = self.__obtener_direccion_de_movimiento(movimiento,True)
        direccion_columna = self.__obtener_direccion_de_movimiento(movimiento,False)

        if pieza == TipoPieza.CABALLO:
            while (not casilla_inicial.fila == casilla_objetivo.fila):
                self.__animacion_mover_una_casilla(tmp_imagen,direccion_fila,0)
                casilla_inicial.avanzar_casilla(direccion_fila,0)
            while (not casilla_inicial.columna == casilla_objetivo.columna):
                self.__animacion_mover_una_casilla(tmp_imagen,0,direccion_columna)
                casilla_inicial.avanzar_casilla(0,direccion_columna)
        else:
            while (not casilla_inicial.equals(casilla_objetivo) ):
                print("casilla inicial")
                casilla_inicial.imprimir()
                print("casilla objetivo")
                casilla_objetivo.imprimir()
                self.__animacion_mover_una_casilla(tmp_imagen,direccion_fila,direccion_columna)
                casilla_inicial.avanzar_casilla(direccion_fila,direccion_columna)
                

    def __animacion_mover_una_casilla(self,img_pieza,direccion_fila,direccion_columna):
        fila = img_pieza.posicion_en_tablero.fila
        columna = img_pieza.posicion_en_tablero.columna
        duracion_de_animacion = 100
        desplazamiento = 100
        iteraciones = 5
        wait = int((duracion_de_animacion / iteraciones)*1000)
        for desplazamiento in range (0,iteraciones):
            print("mov")
            # self.__mover_espacio(img_pieza,desplazamiento,iteraciones,direccion_columna,direccion_fila)
            # time.sleep(duracion_de_animacion / iteraciones)
            # self.__main_canvas.update()
        #self.master.after(0,lambda: self.__mover_espacio(img_pieza,desplazamiento,iteraciones,direccion_columna,direccion_fila,cantidad_de_espacios,wait))            

    def __mover_espacio(self,img_pieza,desplazamiento,iteraciones,direccion_columna,direccion_fila,cantidad_de_espacios,wait):
        if cantidad_de_espacios == 0:
            return
        self.__main_canvas.move(img_pieza,(desplazamiento / iteraciones) * direccion_columna, (desplazamiento / iteraciones) * direccion_fila)
        
        self.master.after(wait,lambda: self.__mover_espacio(img_pieza,desplazamiento,iteraciones,direccion_columna,direccion_fila,cantidad_de_espacios,wait))            
        
    ##Devuelve la direccion del movimiento en fila o columna, pasar True como ultimo parametro para fila, False para columna
    def __obtener_direccion_de_movimiento(self,movimiento,fila):
        if fila:
            diferencia = movimiento.casilla_objetivo.fila - movimiento.casilla_inicial.fila
        else:
            diferencia = movimiento.casilla_objetivo.columna - movimiento.casilla_inicial.columna
        if diferencia == 0:
            return 0
        elif diferencia > 0:
            return 1
        else:
            return -1

    def mover_pieza(self,movimiento):
        casilla_inicial = movimiento.casilla_inicial
        casilla_objetivo = movimiento.casilla_objetivo
        pieza_a_mover = self.__piezas[casilla_inicial.calcular_posicion_tablero()]

        tmp_posicion_pantalla_actual = pieza_a_mover.get_posicion_en_tablero()
        tmp_posicion_pantalla_objetivo = Posicion(movimiento.casilla_objetivo.fila,movimiento.casilla_objetivo.columna)
        tmp_posicion_pantalla_objetivo.calcular_posicion_en_pantalla()
        print("pieza posicion en tablero")
        tmp_posicion_pantalla_actual.imprimir()
        print(" posicion en tablero objetivo")
        tmp_posicion_pantalla_objetivo.imprimir()
        if not tmp_posicion_pantalla_actual.equals(tmp_posicion_pantalla_objetivo):
            print("lanza animacion")
            self.__animacion_de_movimiento(movimiento)
            pieza_a_mover.calcular_posicion_en_tablero(casilla_objetivo)
            pieza_a_mover.mover_pieza()
        
        pieza_objetivo = self.__piezas[casilla_objetivo.calcular_posicion_tablero()]
        if pieza_objetivo != None:
            self.__mover_captura_a_pozo(casilla_objetivo)
        self.__piezas[casilla_objetivo.calcular_posicion_tablero()] = pieza_a_mover
        self.__piezas[casilla_inicial.calcular_posicion_tablero()] = None

    def colocar_coronamiento(self,movimiento,pieza_de_coronamiento):
        casilla_inicial = movimiento.casilla_inicial
        casilla_objetivo = movimiento.casilla_objetivo
        color_de_pieza = self.master.juego.tablero.obtener_color_de_pieza(casilla_inicial)
        pieza_a_mover = self.__piezas[casilla_inicial.calcular_posicion_tablero()]

        tmp_posicion_pantalla_actual = pieza_a_mover.get_posicion_en_tablero()
        tmp_posicion_pantalla_objetivo = Posicion(movimiento.casilla_objetivo.fila,movimiento.casilla_objetivo.columna)
        tmp_posicion_pantalla_objetivo.calcular_posicion_en_pantalla()
        if not tmp_posicion_pantalla_actual.equals(tmp_posicion_pantalla_objetivo):
            self.__animacion_de_movimiento(movimiento)
            pieza_a_mover.calcular_posicion_en_tablero(casilla_objetivo)
            pieza_a_mover.mover_pieza()

        pieza_objetivo = self.__piezas[casilla_objetivo.calcular_posicion_tablero()]
        if pieza_objetivo != None:
            self.__mover_captura_a_pozo(casilla_objetivo)
        self.__mover_captura_a_pozo(casilla_inicial)
        self.__piezas[casilla_inicial.calcular_posicion_tablero()] = None
        pieza_coronamiento = Pieza(self.canvas,pieza_de_coronamiento)
        pieza_coronamiento.calcular_posicion_en_tablero(casilla_objetivo)
        pieza_coronamiento.colocar_imagen_en_tablero()
        self.__piezas[casilla_objetivo.calcular_posicion_tablero()] = pieza_coronamiento
    
    def colocar_enrroque(self,movimiento):
        casilla_inicial = movimiento.casilla_inicial
        casilla_objetivo = movimiento.casilla_objetivo
        pieza_a_mover = self.__piezas[casilla_inicial.calcular_posicion_tablero()]

        tmp_posicion_pantalla_actual = pieza_a_mover.get_posicion_en_tablero()
        tmp_posicion_pantalla_objetivo = Posicion(movimiento.casilla_objetivo.fila,movimiento.casilla_objetivo.columna)
        tmp_posicion_pantalla_objetivo.calcular_posicion_en_pantalla()
        if not tmp_posicion_pantalla_actual.equals(tmp_posicion_pantalla_objetivo):
            self.__animacion_de_movimiento(movimiento)
            pieza_a_mover.calcular_posicion_en_tablero(casilla_objetivo)
            pieza_a_mover.mover_pieza()
        
        
        pieza_objetivo = self.__piezas[casilla_objetivo.calcular_posicion_tablero()]
        self.__piezas[casilla_inicial.calcular_posicion_tablero()] = None
        
        if casilla_objetivo.columna == 2:
            posicion_torre = Posicion(casilla_inicial.fila,0)
            torre = self.__piezas[posicion_torre.calcular_posicion_tablero()]
            
            self.__piezas[posicion_torre.calcular_posicion_tablero()] = None
            posicion_torre.columna = 3

            movimiento_torre = Movimiento(Posicion(posicion_torre.fila,0),Posicion(posicion_torre.fila,posicion_torre.columna))
            self.__animacion_de_movimiento(movimiento_torre)
            torre.calcular_posicion_en_tablero(posicion_torre)
            torre.mover_pieza()
            self.__piezas[posicion_torre.calcular_posicion_tablero()] = torre
           
        elif casilla_objetivo.columna == 6:
            posicion_torre = Posicion(casilla_inicial.fila,7)
            torre = self.__piezas[posicion_torre.calcular_posicion_tablero()]

            self.__piezas[posicion_torre.calcular_posicion_tablero()] = None
            posicion_torre.columna = 5

            movimiento_torre = Movimiento(Posicion(posicion_torre.fila,7),Posicion(posicion_torre.fila,posicion_torre.columna))
            self.__animacion_de_movimiento(movimiento_torre)
            torre.calcular_posicion_en_tablero(posicion_torre)
            torre.mover_pieza()
            self.__piezas[posicion_torre.calcular_posicion_tablero()] = torre
            

        self.__piezas[casilla_objetivo.calcular_posicion_tablero()] = pieza_a_mover

    def actualizar_estado_de_pantalla(self):
        self.__colocar_lbl_img_turno()
        self.__colocar_lbl_img_jaque()
        
    def __mover_captura_a_pozo(self,posicion):
        img_pieza = self.__piezas[posicion.calcular_posicion_tablero()]

        color = self.__obtener_color_de_pieza(img_pieza.pieza)
        pieza = self.__obtener_tipo_de_pieza(img_pieza.pieza)

        for tmp_posicion_pozo in self.__posiciones_de_captura[color][pieza]:
            if type(tmp_posicion_pozo) == type(Posicion(0,0)):
                img_pieza.eliminar_pieza()
                img_pieza.resize(3,3)
                img_pieza.colocar_posicion_en_tablero(tmp_posicion_pozo)
                img_pieza.colocar_imagen_en_tablero()
                self.__main_canvas.update()

                index = self.__posiciones_de_captura[color][pieza].index(tmp_posicion_pozo)
                self.__posiciones_de_captura[color][pieza][index] = img_pieza
                break
            else:
                continue


    # para crear cuadrados 
    def marcar_movimiento_anterior(self,movimiento):
        tmp_casilla = Casilla(self.__main_canvas,movimiento.casilla_inicial,None)
        self.__casillas_mov_anterior.append(tmp_casilla)
        tmp_casilla = Casilla(self.__main_canvas,movimiento.casilla_objetivo,None)
        self.__casillas_mov_anterior.append(tmp_casilla)

    def marcar_movimientos_de_pieza(self,posicion):
        tmp_casilla = Casilla(self.__main_canvas,posicion,TCasilla.DEFENDIDA)
        self.__casillas.append(tmp_casilla)
        for tmp_movimiento in self.master.juego.movimientos_legales:
            if (posicion.equals(tmp_movimiento.casilla_inicial)):
                pieza = self.master.juego.tablero.get_pieza(tmp_movimiento.casilla_objetivo)
                if pieza == None:
                    tipo = TCasilla.AMENAZADA
                else:
                    tipo = TCasilla.ATACADA
                tmp_casilla = Casilla(self.__main_canvas,tmp_movimiento.casilla_objetivo,tipo)
                self.__casillas.append(tmp_casilla)

    def limpiar_casillas_mov_anterior(self):
        while (len(self.__casillas_mov_anterior) > 0):
            tmp_casilla = self.__casillas_mov_anterior.pop()
            tmp_casilla.eliminar_lineas()
            
    def limpiar_casillas(self):
        while (len(self.__casillas) > 0):
            tmp_casilla = self.__casillas.pop()
            tmp_casilla.eliminar_lineas()