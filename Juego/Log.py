import datetime

from Juego import LogMov
from Juego import TipoDeJuego
from Juego import Turno

class Log:

    def __init__(self):
        ##Configuracion del log
        self.file_name = self.generar_nombre_log()
        self.piezas_iniciales = []
        self.tipo_de_juego = 0
        self.J1 = ""
        self.J2 = ""
        self.turno_inicial = ""

        ##Historial
        self.historial_de_movimientos = []

        ##Resultados
        self.juego_finalizado = False
        self.resultado = ""       
        self.time_stamp = ""

        ##Configuracion de archivo
        self.path = "/Logs/"
        self.ext = ".log"
        

    def generar_nombre_log(self):
        date = datetime.datetime().isoformat()
        date.replace(".",":")
        self.file_name = self.path+date+self.ext

    def agregar_log(self,log_mov):
        self.historial_de_movimientos.append(log_mov)

    ##Ejemplo de log
    ##timestamp: datetime.datetime().isoformat()
    ##tipo de juego: self.tipo de juego
    ##J1 v J2: Blancas v Negras
    ##mueven: Blancas
    ##resultado: Ganan Blancas/Ganan Negras/Tablas
    ##tablero inicial: NDd8,NRe8,NTh8,NPd7,NPe7,NPf7,NPg7,BAc6,NAb5,BPh5,NPa4,BPe4,NCh3,BPa2,BPb2,BPd2,BPf2,BPg2,BCb1,BRe1,BAf1,BCg1
    ##historial de movimientos:
    ##1. mov
    ##2. mov
    ##...
    ##n. mov
   
    def registrar_log(self):
        endline = "\n"
        tipo_de_juego = self.tipo_de_juego_toString()
        blancas = self.jugador_blancas_toString()
        negras = self.jugador_negras_toString()
        mueven = self.turno_inicial_toString()
        resultado = self.resultado_toString()
        contador_de_movimientos = 1

        file = open(self.file_name,"x+")
        file.write("timestamp: " + datetime.datetime().isoformat() + endline)
        file.write("tipo de juego: " + tipo_de_juego + endline)
        file.write("blancas: " + blancas + endline)
        file.write("negras: " + negras + endline)
        file.write("mueven: " + mueven + endline)
        file.write("resultado: " + resultado + endline)
        file.write("tablero inicial: ")
        file.write("historial de movimientos: \n")

        for log_mov in self.historial_de_movimientos:
            file.write(str(contador_de_movimientos) + ". " + log_mov.log_movimiento + endline)
            contador_de_movimientos += 1                 
        
        file.close()
        return 
 
    def tipo_de_juego_toString(self):
        if self.tipo_de_juego == TipoDeJuego.TipoDeJuego.Jugador_v_Jugador:
            return "Jugador vs Jugador"
        elif self.tipo_de_juego == TipoDeJuego.TipoDeJuego.Jugador_v_PC:
            return "Jugador vs PC"
        elif self.tipo_de_juego == TipoDeJuego.TipoDeJuego.PC_v_PC:
            return "PC vs PC"
    
    def jugador_blancas_toString(self):
        if self.J1 == Turno.Turno.BLANCAS:
            if self.tipo_de_juego == TipoDeJuego.TipoDeJuego.Jugador_v_Jugador:
                return "Jugador1"
            elif self.tipo_de_juego == TipoDeJuego.TipoDeJuego.Jugador_v_PC:
                return "Jugador"
            elif self.tipo_de_juego == TipoDeJuego.TipoDeJuego.PC_v_PC:
                return "PC1"
        else:
            if self.tipo_de_juego == TipoDeJuego.TipoDeJuego.Jugador_v_Jugador:
                return "Jugador2"
            elif self.tipo_de_juego == TipoDeJuego.TipoDeJuego.Jugador_v_PC:
                return "PC"
            elif self.tipo_de_juego == TipoDeJuego.TipoDeJuego.PC_v_PC:
                return "PC2"
            
    def jugador_negras_toString(self):
        if self.J1 == Turno.Turno.NEGRAS:
            if self.tipo_de_juego == TipoDeJuego.TipoDeJuego.Jugador_v_Jugador:
                return "Jugador1"
            elif self.tipo_de_juego == TipoDeJuego.TipoDeJuego.Jugador_v_PC:
                return "Jugador"
            elif self.tipo_de_juego == TipoDeJuego.TipoDeJuego.PC_v_PC:
                return "PC1"
        else:
            if self.tipo_de_juego == TipoDeJuego.TipoDeJuego.Jugador_v_Jugador:
                return "Jugador2"
            elif self.tipo_de_juego == TipoDeJuego.TipoDeJuego.Jugador_v_PC:
                return "PC"
            elif self.tipo_de_juego == TipoDeJuego.TipoDeJuego.PC_v_PC:
                return "PC2"

    def turno_inicial_toString(self):
        if self.turno_inicial == Turno.Turno.BLANCAS:
            return "Blancas"
        else:
            return "Negras"

    def resultado_toString(self):
        if self.juego_finalizado:
            if self.resultado == None:
                return "Tablas"
            elif self.resultado == Turno.Turno.Blancas:
                return "Ganan las Blancas"
            elif self.resultado == Turno.Turno.Negras:
                return "Ganan las Negras"
        else:
            return "Juego Incompleto"
