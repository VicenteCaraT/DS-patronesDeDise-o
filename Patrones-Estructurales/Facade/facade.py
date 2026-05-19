class Lights:
    def dim(self, level):
        print(f"Luces: Ajustando intensidad a {level}%")
    def on(self):
        print("Luces: Encendidas al 100%")

class Projector:
    def on(self):
        print("Proyector: Encendido")
    def off(self):
        print("Proyector: Apagado")
    def set_input(self, dvd):
        print(f"Proyector: Entrada configurada a {dvd}")

class Screen:
    def lower(self):
        print("Pantalla: Bajando...")
    def raise_screen(self):
        print("Pantalla: Subiendo...")

class SoundSystem:
    def on(self):
        print("Sistema de Sonido: Encendido")
    def off(self):
        print("Sistema de Sonido: Apagado")
    def set_volume(self, level):
        print(f"Sistema de Sonido: Volumen en {level}")

class DVDPlayer:
    def on(self):
        print("Reproductor DVD: Encendido")
    def off(self):
        print("Reproductor DVD: Apagado")
    def play(self, movie):
        print(f"Reproductor DVD: Reproduciendo '{movie}'")

# --- PASO 1 y 2: La Fachada ---
class HomeTheaterFacade:
    """
    Esta clase actúa como un Punto de Entrada Único.
    Oculta toda la complejidad de orquestar 5 componentes distintos.
    """
    def __init__(self, lights, projector, screen, sound_system, dvd_player):
        self.lights = lights
        self.projector = projector
        self.screen = screen
        self.sound_system = sound_system
        self.dvd_player = dvd_player

    def watch_movie(self, movie: str):
        """
        Operación de alto nivel que el cliente quiere ejecutar.
        La Fachada sabe exactamente en qué orden hacer las cosas.
        """
        print(f"\n--- [FACHADA] Preparando el sistema para ver '{movie}' ---")
        self.lights.dim(10)
        self.screen.lower()
        self.projector.on()
        self.projector.set_input("DVD Player")
        self.sound_system.on()
        self.sound_system.set_volume(20)
        self.dvd_player.on()
        self.dvd_player.play(movie)

    def end_movie(self):
        """
        Otra operación de alto nivel para apagar todo ordenadamente.
        """
        print("\n--- [FACHADA] Apagando el sistema de cine en casa ---")
        self.lights.on()
        self.screen.raise_screen()
        self.projector.off()
        self.sound_system.off()
        self.dvd_player.off()

# --- SIMULACIÓN DE EJECUCIÓN (Refactorizada) ---
if __name__ == "__main__":
    # 1. El cliente (o un inyector de dependencias) crea los componentes
    luces = Lights()
    proyector = Projector()
    pantalla = Screen()
    sonido = SoundSystem()
    dvd = DVDPlayer()

    # 2. Creamos la Fachada pasándole los componentes
    home_theater = HomeTheaterFacade(luces, proyector, pantalla, sonido, dvd)

    # 3. El Cliente ahora tiene una vida muy fácil
    # ¡Un solo botón para encender todo!
    home_theater.watch_movie("Inception")
    
    # ¡Un solo botón para apagar todo!
    home_theater.end_movie()

    # --- ANÁLISIS ARQUITECTÓNICO ---
    # 1. Bajo Acoplamiento: El cliente (el 'main') ya no llama a métodos de Screen o Projector.
    # 2. Mantenibilidad: Si cambiamos el orden de encendido, solo modificamos la clase Facade.
    # 3. Principio de Menor Conocimiento: El cliente "habla con menos amigos".
