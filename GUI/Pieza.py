import tkinter as tk

from Juego.Posicion import Posicion
from Juego.Movimiento import Movimiento

class Pieza():

    def __init__(self,canvas,pieza):
        self.canvas = canvas
        self.pieza = pieza
        self.cargar_imagen()

        ##Propiedades para realizar una animacion de movimiento
        self.direccion_fila = None
        self.direccion_columna = None
        self.posicion_limite = None


    ##Crea el path para la imagen de la pieza y carga la imagen
    def cargar_imagen(self):
        self.path = './Imagenes/'
        tipo = '.gif'
        if self.pieza > 0:
            color_de_pieza = 'B'
        else:
            color_de_pieza = 'N'

        if abs(self.pieza) == 1:
            self.path += color_de_pieza+'P'+tipo
            #self.posicion_inicial = Posicion.Posicion(125,49.32)
        elif abs(self.pieza) == 2:
            self.path += color_de_pieza+'C'+tipo
            #self.posicion_inicial = Posicion.Posicion(126,50.4)
        elif abs(self.pieza) == 3:
            self.path += color_de_pieza+'A'+tipo
            #self.posicion_inicial = Posicion.Posicion(126,50.3)
        elif abs(self.pieza) == 4:
            self.path += color_de_pieza+'T'+tipo
            #self.posicion_inicial = Posicion.Posicion(126,50.3)
        elif abs(self.pieza) == 5:
            self.path += color_de_pieza+'D'+tipo
            #self.posicion_inicial = Posicion.Posicion(126,50.5)
        else:
            self.path += color_de_pieza+'R'+tipo
            #self.posicion_inicial = Posicion.Posicion(127,50.5)
        self.posicion_inicial = Posicion(100,100)
        self.imagen = tk.PhotoImage(file=self.path)
        #self.imagen = self.imagen.subsample(2,2)
    
    def calcular_posicion_en_tablero(self,posicion):
        self.posicion_en_tablero = Posicion(self.posicion_inicial.fila + (posicion.fila * 100),self.posicion_inicial.columna + (posicion.columna*100))

    def colocar_posicion_en_tablero(self,posicion):
        self.posicion_en_tablero = Posicion(posicion.fila,posicion.columna)
        
    def colocar_imagen_en_tablero(self):
        self.id_canvas = self.canvas.create_image(self.posicion_en_tablero.columna,self.posicion_en_tablero.fila,image = self.imagen)
        self.canvas.pack()
    
    def resize(self,escala_fila, escala_columna):
        self.imagen = self.imagen.subsample(escala_fila,escala_columna)

    def mover_pieza(self):
        self.canvas.coords(self.id_canvas,(self.posicion_en_tablero.columna,self.posicion_en_tablero.fila))
  
    def get_posicion_en_tablero(self):
        return self.posicion_en_tablero

    def mover_casilla_en_tablero(self,direccion_fila,direccion_columna):
        self.posicion_en_tablero = Posicion(self.posicion_en_tablero.fila+100*direccion_fila,self.posicion_en_tablero.columna+100*direccion_columna)
    
    def eliminar_pieza(self):
        self.canvas.delete(self.id_canvas)

    def get_focus(self):
        self.id_canvas.configure(takefocus=True)

    def realizar_animacion(self):
        columna_actual,fila_actual = self.canvas.coords(self.id_canvas)
        if abs(self.pieza) == 2:
            if self.posicion_limite.columna != columna_actual:
                self.canvas.move(self.id_canvas, self.direccion_columna, 0)
                self.canvas.after(self.espera_de_movimiento, self.realizar_animacion)

            elif self.posicion_limite.fila != fila_actual:
                self.canvas.move(self.id_canvas, 0, self.direccion_fila)
                self.canvas.after(self.espera_de_movimiento, self.realizar_animacion)
            else:
                self.mover_pieza()
        else:
            if self.direccion_fila == 1 and self.direccion_columna == 1:
                if fila_actual < self.posicion_limite.fila or columna_actual < self.posicion_limite.columna:
                    self.canvas.move(self.id_canvas, self.direccion_columna, self.direccion_fila)
                    self.canvas.after(self.espera_de_movimiento, self.realizar_animacion)
                else:
                    self.mover_pieza()
                    
            elif self.direccion_fila == 1 and self.direccion_columna == 0:
                if fila_actual < self.posicion_limite.fila:
                    self.canvas.move(self.id_canvas, self.direccion_columna, self.direccion_fila)
                    self.canvas.after(self.espera_de_movimiento, self.realizar_animacion)
                else:
                    self.mover_pieza()

            elif self.direccion_fila == 0 and self.direccion_columna == 1:
                if columna_actual < self.posicion_limite.columna:
                    self.canvas.move(self.id_canvas, self.direccion_columna, self.direccion_fila)
                    self.canvas.after(self.espera_de_movimiento, self.realizar_animacion)
                else:
                    self.mover_pieza()

            elif self.direccion_fila == -1 and self.direccion_columna == -1:
                if fila_actual > self.posicion_limite.fila or columna_actual > self.posicion_limite.columna:
                    self.canvas.move(self.id_canvas, self.direccion_columna, self.direccion_fila)
                    self.canvas.after(self.espera_de_movimiento, self.realizar_animacion)
                else:
                    self.mover_pieza()

            elif self.direccion_fila == -1 and self.direccion_columna == 0:
                if fila_actual > self.posicion_limite.fila:
                    self.canvas.move(self.id_canvas, self.direccion_columna, self.direccion_fila)
                    self.canvas.after(self.espera_de_movimiento, self.realizar_animacion)
                else:
                    self.mover_pieza()
            elif self.direccion_fila == 0 and self.direccion_columna == -1:
                if columna_actual > self.posicion_limite.columna:
                    self.canvas.move(self.id_canvas, self.direccion_columna, self.direccion_fila)
                    self.canvas.after(self.espera_de_movimiento, self.realizar_animacion)
                else:
                    self.mover_pieza()
            elif self.direccion_fila == -1 and self.direccion_columna == 1:
                if fila_actual > self.posicion_limite.fila or columna_actual < self.posicion_limite.columna:
                    self.canvas.move(self.id_canvas, self.direccion_columna, self.direccion_fila)
                    self.canvas.after(self.espera_de_movimiento, self.realizar_animacion)
                else:
                    self.mover_pieza()
            elif self.direccion_fila == 1 and self.direccion_columna == -1:
                if fila_actual < self.posicion_limite.fila or columna_actual > self.posicion_limite.columna:
                    self.canvas.move(self.id_canvas, self.direccion_columna, self.direccion_fila)
                    self.canvas.after(self.espera_de_movimiento, self.realizar_animacion)
                else:
                    self.mover_pieza()
            else:
                return

            

    def preparar_animacion(self,movimiento):
        ##establecer las variables que definen el movimiento
        self.canvas.lift(self.id_canvas)
        self.direccion_fila = self.__obtener_direccion_de_movimiento(movimiento,True)
        self.direccion_columna = self.__obtener_direccion_de_movimiento(movimiento,False)
        self.posicion_limite = movimiento.casilla_objetivo.calcular_posicion_en_pantalla()
        self.espera_de_movimiento = 3
        
        if self.direccion_fila == 1 or self.direccion_fila == -1:
            self.posicion_limite.fila = self.posicion_limite.fila + 50

        if self.direccion_columna == 1 or self.direccion_columna == -1:
            self.posicion_limite.columna = self.posicion_limite.columna + 50
        
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

    # def move_object(obj_id):
    # can.move(obj_id, 0, 1)
    # x0,y0,x1,y1 = can.coords(obj_id)
    # if y0 < yCan: 
    #     can.after(5, move_obj, obj_id)
    #movX = posXTablero + (col-1) * 48
    #movY = posYTablero + (fila-1) * 46        

