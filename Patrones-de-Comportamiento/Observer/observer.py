from abc import ABC, abstractmethod

# --- PASO 1: Interfaz del Observador (El Contrato) ---
class Subscriber(ABC):
    """
    Cualquier sistema que quiera ser avisado por un canal de YouTube
    debe implementar esta interfaz.
    """
    @abstractmethod
    def update(self, video_title: str):
        pass

# --- PASO 2: Observadores Concretos ---
# Ahora estas clases son "hijas" de la abstracción Subscriber.
class EmailNotifier(Subscriber):
    def update(self, video_title: str):
        print(f"[Email] Enviando correo: ¡Nuevo video '{video_title}' publicado!")

class MobileAppNotifier(Subscriber):
    def update(self, video_title: str):
        print(f"[App] Notificación Push: ¡Nuevo video '{video_title}' disponible!")

# Podemos añadir nuevos observadores fácilmente
class FanPageNotifier(Subscriber):
    def update(self, video_title: str):
        print(f"[Facebook] Posteando link del video '{video_title}' en la FanPage.")


# --- PASO 3: El Sujeto (Observable) ---
class YouTubeChannel:
    """
    El canal ya NO conoce las clases EmailNotifier o MobileAppNotifier.
    Solo sabe que tiene una lista de 'Subscribers'.
    """
    def __init__(self, channel_name):
        self.name = channel_name
        # Aquí guardamos a los interesados dinámicamente
        self._subscribers = []

    def subscribe(self, subscriber: Subscriber):
        """Añade un interesado a la lista."""
        if subscriber not in self._subscribers:
            self._subscribers.append(subscriber)

    def unsubscribe(self, subscriber: Subscriber):
        """Elimina un interesado de la lista."""
        self._subscribers.remove(subscriber)

    def notify(self, video_title: str):
        """
        Recorre la lista y avisa a todos los suscriptores.
        Este es el núcleo del patrón.
        """
        for subscriber in self._subscribers:
            # Polimorfismo: no sabemos qué es, solo que tiene 'update'
            subscriber.update(video_title)

    def upload_video(self, title: str):
        print(f"--- [LOG] Canal '{self.name}' subiendo video: {title} ---")
        # Al terminar de subir, avisamos a los interesados
        self.notify(title)


# --- SIMULACIÓN DE EJECUCIÓN (Refactorizada) ---
if __name__ == "__main__":
    # 1. Creamos el canal
    canal = YouTubeChannel("Arquitectura de Software")
    
    # 2. Creamos los sistemas de notificación
    email = EmailNotifier()
    app = MobileAppNotifier()
    fb = FanPageNotifier()

    # 3. Los sistemas se suscriben (Dinamismo en tiempo de ejecución)
    print("--- REGISTRANDO SUSCRIPTORES ---")
    canal.subscribe(email)
    canal.subscribe(app)
    canal.subscribe(fb)

    # 4. Subimos un video: todos reciben aviso
    canal.upload_video("Patrón Observer en Python")

    print("\n" + "-"*40 + "\n")

    # 5. El usuario se cansa de los correos y se desuscribe
    print("--- ELIMINANDO SUSCRIPTOR DE EMAIL ---")
    canal.unsubscribe(email)

    # 6. Subimos otro video: el email ya no recibe nada, los demás sí
    canal.upload_video("Introducción a SOLID")

    # --- ANÁLISIS ARQUITECTÓNICO ---
    # 1. Desacoplamiento: El canal es totalmente ignorante de quiénes son sus suscriptores.
    # 2. OCP: Añadimos 'FanPageNotifier' sin tocar el código de YouTubeChannel.
    # 3. Flexibilidad: Los observadores entran y salen de la lista "al vuelo".
