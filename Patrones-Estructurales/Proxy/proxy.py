from abc import ABC, abstractmethod
import time

# --- PASO 1: Interfaz de Servicio (El Contrato) ---
class Video(ABC):
    """
    Define la interfaz común para el objeto real y el proxy.
    """
    @abstractmethod
    def play(self):
        pass

# --- PASO 2: Objeto Real (Pesado) ---
class RealVideoService(Video):
    """
    Realiza la tarea pesada y costosa (descargar un video).
    Ahora hereda de la interfaz común.
    """
    def __init__(self, video_id):
        self.video_id = video_id
        # La descarga ocurre inmediatamente en el constructor del objeto real
        self._download_video()

    def _download_video(self):
        print(f"--- [RECURSO PESADO] Descargando video '{self.video_id}' de un servidor remoto... ---")
        time.sleep(2) # Simulación de latencia de red
        print(f"--- Descarga de '{self.video_id}' completada. ---")

    def play(self):
        print(f"Reproduciendo video: {self.video_id}")

# --- PASO 3: El Proxy (Ligero) ---
class ProxyVideoService(Video):
    """
    Sustituto ligero del servicio real. 
    Controla el acceso y pospone la creación del objeto pesado (Lazy Loading).
    """
    def __init__(self, video_id):
        self.video_id = video_id
        # Inicialmente NO existe el objeto real (es barato de crear)
        self._real_video_service = None

    def play(self):
        """
        Intercepta la llamada. Si el video no ha sido descargado,
        lo descarga ahora. Si ya existe, lo reutiliza.
        """
        if self._real_video_service is None:
            print(f"[PROXY] El video '{self.video_id}' no está en caché. Iniciando carga perezosa...")
            # Aquí es donde realmente se paga el costo de creación
            self._real_video_service = RealVideoService(self.video_id)
        
        # Delega la petición al objeto real
        self._real_video_service.play()

# --- SIMULACIÓN DE EJECUCIÓN (Refactorizada) ---
if __name__ == "__main__":
    print("--- INICIANDO APLICACIÓN DE STREAMING (CON PROXY) ---")
    
    start_time = time.time()

    # Ahora creamos Proxys en lugar de los servicios reales.
    # Esta operación es instantánea.
    video_1 = ProxyVideoService("Cachorros_Divertidos.mp4")
    video_2 = ProxyVideoService("Tutorial_Python_Avanzado.mp4")

    end_time = time.time()
    print(f"\nLista de videos cargada en {end_time - start_time:.4f} segundos.")
    print("(Antes tardaba 4 segundos. ¡Ganancia de rendimiento del 100%!)")

    print("\nEl usuario decide ver solo el primer video:")
    # La descarga solo ocurre para el video_1 en este momento
    video_1.play()

    print("\nEl usuario decide ver el primer video OTRA VEZ:")
    # Ya está en caché del proxy, no se vuelve a descargar
    video_1.play()

    print("\nANÁLISIS FINAL:")
    print(f"1. El video 2 ('Tutorial_Python_Avanzado.mp4') NUNCA se descargó.")
    print(f"2. Se ahorró ancho de banda y tiempo de CPU.")
    print(f"3. El cliente trató al Proxy exactamente como si fuera el Video Real.")
