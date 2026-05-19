from abc import ABC, abstractmethod

# --- EL OBJETO DE SOLICITUD ---
class SupportTicket:
    def __init__(self, message, priority):
        self.message = message
        self.priority = priority # 1: Básico, 2: Intermedio, 3: Crítico

# --- PASO 1: Clase Base del Manejador (Handler) ---
class SupportHandler(ABC):
    """
    Define la interfaz para manejar peticiones y el enlace al siguiente.
    """
    def __init__(self):
        self._next_handler = None

    def set_next(self, handler):
        """
        Permite encadenar manejadores de forma fluida: h1.set_next(h2).set_next(h3)
        """
        self._next_handler = handler
        return handler

    @abstractmethod
    def handle(self, ticket: SupportTicket):
        """
        Si hay un sucesor, delega la petición por defecto.
        """
        if self._next_handler:
            return self._next_handler.handle(ticket)
        
        print(f"Fin de la cadena: Nadie pudo resolver el ticket '{ticket.message}'")
        return None

# --- PASO 2: Manejadores Concretos ---
class BotHandler(SupportHandler):
    def handle(self, ticket: SupportTicket):
        if ticket.priority == 1:
            print(f"[BOT] Resuelto automáticamente: '{ticket.message}'")
        else:
            # Si no es prioridad 1, pasa al siguiente eslabón
            print(f"[BOT] No puedo resolver '{ticket.message}'. Pasando al Nivel 2...")
            super().handle(ticket)

class AgentHandler(SupportHandler):
    def handle(self, ticket: SupportTicket):
        if ticket.priority == 2:
            print(f"[AGENTE] Resuelto por humano: '{ticket.message}'")
        else:
            print(f"[AGENTE] No puedo resolver '{ticket.message}'. Pasando al Nivel 3...")
            super().handle(ticket)

class EngineerHandler(SupportHandler):
    def handle(self, ticket: SupportTicket):
        if ticket.priority == 3:
            print(f"[INGENIERÍA] Resuelto por especialista: '{ticket.message}'")
        else:
            # Si llegamos aquí y no es prioridad 3, la base dirá que no hay más manejadores
            super().handle(ticket)

# --- SIMULACIÓN DE EJECUCIÓN (Refactorizada) ---
if __name__ == "__main__":
    # 1. Creamos los eslabones
    bot = BotHandler()
    agente = AgentHandler()
    ingeniero = EngineerHandler()

    # 2. Configuramos la cadena: Bot -> Agente -> Ingeniero
    bot.set_next(agente).set_next(ingeniero)

    # 3. Creamos tickets de diferentes prioridades
    tickets = [
        SupportTicket("Olvidé mi clave", 1),
        SupportTicket("Mi cuenta está bloqueada", 2),
        SupportTicket("Error 500 en producción", 3),
        SupportTicket("Sugerencia de nueva funcionalidad", 4) # Nadie lo maneja
    ]

    print("--- INICIANDO PROCESAMIENTO DE CADENA ---\n")
    for t in tickets:
        # Solo necesitamos hablar con el PRIMER eslabón
        bot.handle(t)
        print("-" * 30)

    # --- ANÁLISIS ARQUITECTÓNICO ---
    # 1. Desacoplamiento: El emisor (este main) no sabe quién resuelve cada ticket.
    # 2. SRP: Cada clase Handler tiene una única responsabilidad (un nivel de soporte).
    # 3. OCP: Si añadimos 'DirectorHandler', solo lo creamos y lo insertamos en la cadena 
    #    sin tocar Bot, Agente o Ingeniero.
