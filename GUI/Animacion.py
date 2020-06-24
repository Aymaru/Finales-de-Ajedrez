
import threading

class Animacion(threading.Thread):
    
    def __init__(self, pieza):
        threading.Thread.__init__(self)
        self.pieza = pieza
        
    
    def run(self):
        self.pieza.realizar_animacion()