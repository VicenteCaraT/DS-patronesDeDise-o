from abc import ABC, abstractmethod

# --- PASO 1: Interfaz del Mediador ---
class Mediator(ABC):
    """
    Define el contrato para la comunicación. 
    Cualquier componente (colega) usará este método para avisar que algo pasó.
    """
    @abstractmethod
    def notify(self, sender, event: str):
        pass


# --- PASO 2: Componentes (Colegas) ---
# Fíjate que ahora solo conocen al Mediador, no se conocen entre sí.

class Component:
    """Clase base para todos los componentes de la interfaz."""
    def __init__(self, mediator: Mediator = None):
        self.mediator = mediator

class TextBox(Component):
    def __init__(self, name, mediator=None):
        super().__init__(mediator)
        self.name = name
        self.text = ""

    def set_text(self, text):
        self.text = text
        print(f"[UI] TextBox '{self.name}' cambió a: '{self.text}'")
        # Avisamos al mediador del cambio
        self.mediator.notify(self, "text_changed")

class Checkbox(Component):
    def __init__(self, name, mediator=None):
        super().__init__(mediator)
        self.name = name
        self.is_checked = False

    def toggle(self):
        self.is_checked = not self.is_checked
        print(f"[UI] Checkbox '{self.name}' marcado: {self.is_checked}")
        # Avisamos al mediador del cambio
        self.mediator.notify(self, "checkbox_toggled")

class SubmitButton(Component):
    def __init__(self, mediator=None):
        super().__init__(mediator)
        self.is_enabled = False

    def enable(self):
        self.is_enabled = True
        print("[UI] Botón 'Enviar' HABILITADO.")

    def disable(self):
        self.is_enabled = False
        print("[UI] Botón 'Enviar' DESHABILITADO.")

    def click(self):
        if self.is_enabled:
            print("[SISTEMA] ¡Formulario enviado con éxito!")
        else:
            print("[SISTEMA] Error: Formulario incompleto.")


# --- PASO 3: Mediador Concreto (El Cerebro) ---
class RegistrationMediator(Mediator):
    """
    Aquí reside toda la lógica de negocio de la interfaz.
    Sabe cómo deben interactuar los componentes entre sí.
    """
    def __init__(self):
        # El mediador tiene referencias a todos los componentes
        self.name_box = None
        self.terms_checkbox = None
        self.submit_btn = None

    def notify(self, sender, event):
        """
        Lógica de orquestación centralizada.
        """
        # Regla: El botón solo se habilita si hay nombre Y términos aceptados.
        if event in ["text_changed", "checkbox_toggled"]:
            if self.name_box.text != "" and self.terms_checkbox.is_checked:
                self.submit_btn.enable()
            else:
                self.submit_btn.disable()


# --- SIMULACIÓN DE EJECUCIÓN (Refactorizada) ---
if __name__ == "__main__":
    # 1. Instanciamos el mediador
    mediador = RegistrationMediator()

    # 2. Creamos los componentes pasándoles el mediador
    # Notar que ya no le pasamos el Botón al Checkbox.
    txt_nombre = TextBox("Nombre Usuario", mediador)
    chk_terminos = Checkbox("Términos y Condiciones", mediador)
    btn_enviar = SubmitButton(mediador)

    # 3. Conectamos los componentes al mediador
    mediador.name_box = txt_nombre
    mediador.terms_checkbox = chk_terminos
    mediador.submit_btn = btn_enviar

    print("--- INICIANDO FORMULARIO CON MEDIADOR ---\n")
    
    print("Paso 1: Usuario escribe su nombre...")
    txt_nombre.set_text("Vicente")
    btn_enviar.click() # Todavía falla (falta checkbox)

    print("\nPaso 2: Usuario marca los términos...")
    chk_terminos.toggle() # El mediador detecta esto y habilita el botón automáticamente
    btn_enviar.click() # ¡Éxito!

    print("\nPaso 3: Usuario borra su nombre...")
    txt_nombre.set_text("") # El mediador detecta el cambio y DESHABILITA el botón
    btn_enviar.click() # Falla de nuevo

    # --- ANÁLISIS ARQUITECTÓNICO ---
    # 1. Centralización: La lógica de habilitar/deshabilitar está en un solo lugar (Mediador).
    # 2. Reutilización: TextBox y Checkbox son genéricos y no conocen el botón.
    # 3. Mantenibilidad: Si añadimos un campo 'Email', solo modificamos el Mediador.
    
    print("\nÉXITO: Se eliminaron las dependencias caóticas.")
