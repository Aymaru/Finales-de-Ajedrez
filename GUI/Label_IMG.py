import tkinter as tk

from Juego import Posicion

class Label_IMG():

    def __init__(self,canvas,imagen):
        self.canvas = canvas
        self.lbl_imagen = imagen
        self.cargar_imagen()
        self.resize_img()



    def cargar_imagen(self):
        self.path = './Imagenes/'
        tipo = '.gif'
        
        self.path += self.lbl_imagen+tipo
        
        self.imagen = tk.PhotoImage(file=self.path)

    def resize_img(self):
        self.imagen = self.imagen.subsample(7,7)
       
    def colocar_posicion_en_tablero(self,posicion):
        self.posicion_en_tablero = Posicion.Posicion(posicion.fila,posicion.columna)
        
      
    def colocar_imagen_en_tablero(self):
        self.id_canvas = self.canvas.create_image(self.posicion_en_tablero.columna,self.posicion_en_tablero.fila,image = self.imagen)
        self.canvas.pack()

    def delete_image(self):
        self.canvas.delete(self.id_canvas)
        #self.d


    
