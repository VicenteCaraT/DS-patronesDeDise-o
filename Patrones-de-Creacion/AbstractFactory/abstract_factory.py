from abc import ABC, abstractmethod

# --- PASO 1: Interfaces de Productos (Abstracciones) ---
# Definimos los contratos que todos los componentes de la misma familia deben seguir.
class Button(ABC):
    @abstractmethod
    def paint(self):
        pass
    
class Checkbox(ABC):
    @abstractmethod
    def check(self):
        pass

# --- PASO 2: Productos Concretos (Variante CLARA) ---
class LightButton(Button):
    def paint(self):
        print("Pintando Botón en modo CLARO")

class LightCheckbox(Checkbox):
    def check(self):
        print("Pintando Checkbox en modo CLARO")

# --- PASO 2: Productos Concretos (Variante OSCURA) ---
class DarkButton(Button):
    def paint(self):
        print("Pintando Botón en modo OSCURO")

class DarkCheckbox(Checkbox):
    def check(self):
        print("Pintando Checkbox en modo OSCURO")

# --- PASO 3: Interfaz de la Fábrica Abstracta ---
# Este es el contrato para crear familias de objetos. 
# Nota que NO sabe si los objetos serán claros u oscuros.
class UIFactory(ABC):
    @abstractmethod
    def create_button(self) -> Button:
        pass
    
    @abstractmethod
    def create_checkbox(self) -> Checkbox:
        pass
    
# --- PASO 4: Fábricas Concretas ---
# Cada fábrica se especializa en una familia (un tema).
class LightUIFactory(UIFactory):
    def create_button(self) -> Button:
        return LightButton() # Retornamos instancia, no la clase
    
    def create_checkbox(self) -> Checkbox:
        return LightCheckbox()

class DarkUIFactory(UIFactory):
    def create_button(self) -> Button:
        return DarkButton()
    
    def create_checkbox(self) -> Checkbox:
        return DarkCheckbox()
    

# --- PASO 5: El Cliente (Application) ---
class Application:
    """
    La aplicación está totalmente desacoplada. 
    Solo conoce interfaces (UIFactory, Button, Checkbox).
    No sabe si los componentes son claros u oscuros.
    """
    def __init__(self, factory: UIFactory):
        # La fábrica nos entrega objetos de la misma familia automáticamente
        self.button = factory.create_button()
        self.checkbox = factory.create_checkbox()

    def render(self):
        self.button.paint()
        self.checkbox.check()

# --- SIMULACIÓN DE EJECUCIÓN (Arreglada) ---
if __name__ == "__main__":
    # 1. Queremos ejecutar la app en modo CLARO
    print("Configurando Sistema en modo CLARO...")
    factory_claro = LightUIFactory()
    app_clara = Application(factory_claro)
    app_clara.render()

    print("-" * 30)

    # 2. Queremos ejecutar la app en modo OSCURO
    print("Configurando Sistema en modo OSCURO...")
    factory_oscuro = DarkUIFactory()
    app_oscura = Application(factory_oscuro)
    app_oscura.render()

    # --- CONCLUSIÓN ARQUITECTÓNICA ---
    # 1. Consistencia: Es IMPOSIBLE mezclar un LightButton con un DarkCheckbox.
    # 2. OCP: Si quieres un tema 'Retro', creas RetroFactory y RetroProducts sin tocar Application.
    # 3. DIP: Application depende de abstracciones, no de clases concretas.
