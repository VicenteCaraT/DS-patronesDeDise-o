from abc import ABC, abstractmethod

# --- PASO 1: Interfaz de la Estrategia (El Contrato) ---
class RouteStrategy(ABC):
    """
    Define la interfaz común que todos los algoritmos de enrutamiento
    deben implementar. El Navigator usará esta interfaz.
    """
    @abstractmethod
    def build_route(self, start: str, destination: str):
        pass

# --- PASO 2: Estrategias Concretas (Los algoritmos aislados) ---
# Cada clase tiene UNA sola responsabilidad: calcular una ruta específica.
class WalkingStrategy(RouteStrategy):
    def build_route(self, start: str, destination: str):
        print(f"  -> [A PIE] Calculando ruta {start} -> {destination} (evitando autopistas).")
        print("  -> Tiempo estimado: 45 minutos.")

class DrivingStrategy(RouteStrategy):
    def build_route(self, start: str, destination: str):
        print(f"  -> [AUTO] Calculando ruta {start} -> {destination} (calculando tráfico rápido).")
        print("  -> Tiempo estimado: 15 minutos.")

class TransitStrategy(RouteStrategy):
    def build_route(self, start: str, destination: str):
        print(f"  -> [TREN/BUS] Calculando ruta {start} -> {destination} (buscando paradas).")
        print("  -> Tiempo estimado: 30 minutos.")

# ¡Podemos añadir nuevas estrategias sin tocar el código existente!
class BikeStrategy(RouteStrategy):
    def build_route(self, start: str, destination: str):
        print(f"  -> [BICI] Calculando ruta {start} -> {destination} (buscando ciclovías).")
        print("  -> Tiempo estimado: 25 minutos.")


# --- PASO 3: El Contexto (La clase principal refactorizada) ---
class Navigator:
    """
    El Navigator ya no sabe cómo calcular rutas. 
    Solo mantiene una referencia a una Estrategia y delega el trabajo.
    """
    def __init__(self, strategy: RouteStrategy = None):
        self._strategy = strategy

    def set_strategy(self, strategy: RouteStrategy):
        """
        Permite cambiar el comportamiento del Navigator en tiempo de ejecución.
        """
        self._strategy = strategy

    def calculate_route(self, start: str, destination: str):
        print(f"\nIniciando navegación...")
        
        if not self._strategy:
            print("  -> Error: No se ha configurado una estrategia de navegación.")
            return
            
        # ¡Magia pura! No hay 'if'. Solo delegamos al objeto que nos inyectaron.
        self._strategy.build_route(start, destination)


# --- SIMULACIÓN DE EJECUCIÓN (Refactorizada) ---
if __name__ == "__main__":
    # Creamos el navegador (inicialmente sin estrategia)
    app = Navigator()

    # El usuario elige "Caminar"
    print("--- USUARIO SELECCIONA: CAMINAR ---")
    app.set_strategy(WalkingStrategy())
    app.calculate_route("Casa", "Oficina")

    # El usuario cambia de opinión a mitad de camino y elige "Auto"
    print("\n--- USUARIO SELECCIONA: AUTO ---")
    app.set_strategy(DrivingStrategy())
    app.calculate_route("Casa", "Oficina")
    
    # El usuario descarga la actualización que incluye "Bicicleta"
    print("\n--- USUARIO SELECCIONA: BICICLETA ---")
    app.set_strategy(BikeStrategy())
    app.calculate_route("Casa", "Oficina")

    # --- ANÁLISIS ARQUITECTÓNICO ---
    # 1. Adiós condicionales: Eliminamos completamente los if/elif que ataban al Navigator.
    # 2. OCP cumplido: Añadimos 'BikeStrategy' sin modificar ni una coma de la clase Navigator.
    # 3. Intercambio Dinámico: Cambiamos el algoritmo en pleno vuelo usando 'set_strategy'.
