from abc import ABC, abstractmethod

# --- PASO 1: Interfaz del Producto ---
# Definimos una clase abstracta que servirá como contrato. 
# Todas las notificaciones deben tener el método 'send'.
class Notification(ABC):
    @abstractmethod
    def send(self, message):
        pass

# --- PASO 2: Productos Concretos ---
# Implementan la interfaz Notification.
class EmailNotification(Notification):
    def send(self, message):
        print(f"Enviando Email: {message}")

class SMSNotification(Notification):
    def send(self, message):
        print(f"Enviando SMS: {message}")

# --- PASO 3: El Creador (Clase Abstracta) ---
# Esta clase contiene la lógica de negocio principal.
# Su responsabilidad NO es crear el objeto, sino usarlo.
class NotificationCreator(ABC):
    
    # Este es el FACTORY METHOD real.
    # Es abstracto porque delegamos la creación a las subclases.
    @abstractmethod
    def create_notification(self) -> Notification:
        pass

    # Lógica de negocio que utiliza el producto.
    # Observa que NO sabe si es un Email o un SMS, solo sabe que es una 'Notification'.
    def send_notification(self, message):
        # Llamamos al factory method para obtener el objeto
        notification = self.create_notification()
        # Usamos el objeto (Polimorfismo)
        notification.send(message)

# --- PASO 4: Creadores Concretos ---
# Cada subclase decide qué tipo de notificación instanciar.
class EmailCreator(NotificationCreator):
    def create_notification(self) -> Notification:
        # Aquí es donde se hace el 'new' (instanciación)
        return EmailNotification()

class SMSCreator(NotificationCreator):
    def create_notification(self) -> Notification:
        return SMSNotification()

# --- SIMULACIÓN DE EJECUCIÓN ---
if __name__ == "__main__":
    print("Iniciando sistema de notificaciones con Factory Method...\n")

    # Si queremos enviar un Email, usamos el creador de Emails
    app_email = EmailCreator()
    app_email.send_notification("Bienvenido a la plataforma")

    # Si queremos enviar un SMS, usamos el creador de SMS
    app_sms = SMSCreator()
    app_sms.send_notification("Tu código de verificación es 1234")

    # ¿Por qué esto es mejor? 
    # Si queremos añadir WhatsApp, NO tocamos NotificationCreator.
    # Solo crearíamos: class WhatsAppNotification(Notification) 
    # y class WhatsAppCreator(NotificationCreator).
    # Esto cumple con el principio Abierto/Cerrado (OCP).
