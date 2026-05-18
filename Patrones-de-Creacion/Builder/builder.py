from abc import ABC, abstractmethod

# --- PASO 1: El Producto ---
class Computer:
    """
    Representa el objeto complejo a construir. 
    Ahora es un contenedor simple de datos.
    """
    def __init__(self):
        self.cpu = None
        self.ram = None
        self.storage = None
        self.gpu = None
        self.screen = None
        self.keyboard = None

    def __str__(self):
        return (f"Computadora [CPU: {self.cpu}, RAM: {self.ram}, "
                f"Almacenamiento: {self.storage}, GPU: {self.gpu}, "
                f"Pantalla: {self.screen}, Teclado: {self.keyboard}]")

# --- PASO 2: Interfaz del Builder ---
class ComputerBuilder(ABC):
    @abstractmethod
    def reset(self): pass

    @abstractmethod
    def configure_cpu(self, cpu): pass
    
    @abstractmethod
    def configure_ram(self, ram): pass
    
    @abstractmethod
    def configure_storage(self, storage): pass
    
    @abstractmethod
    def configure_gpu(self, gpu): pass
    
    @abstractmethod
    def configure_screen(self, screen): pass
    
    @abstractmethod
    def configure_keyboard(self, keyboard): pass
    
    @abstractmethod
    def get_result(self) -> Computer: pass    

# --- PASO 3: Builders Concretos ---
class GamingBuilder(ComputerBuilder):
    def __init__(self):
        self.reset()

    def reset(self):
        self._computer = Computer()

    def configure_cpu(self, cpu): self._computer.cpu = cpu
    def configure_ram(self, ram): self._computer.ram = ram
    def configure_storage(self, storage): self._computer.storage = storage
    def configure_gpu(self, gpu): self._computer.gpu = gpu
    def configure_screen(self, screen): self._computer.screen = screen
    def configure_keyboard(self, keyboard): self._computer.keyboard = keyboard
    
    def get_result(self) -> Computer:
        product = self._computer
        self.reset() # El builder queda listo para otra construcción
        return product

class OfficeBuilder(ComputerBuilder):
    def __init__(self):
        self.reset()

    def reset(self):
        self._computer = Computer()

    def configure_cpu(self, cpu): self._computer.cpu = cpu
    def configure_ram(self, ram): self._computer.ram = ram
    def configure_storage(self, storage): self._computer.storage = storage
    def configure_gpu(self, gpu): pass # Las PC de oficina no suelen tener GPU dedicada
    def configure_screen(self, screen): self._computer.screen = screen
    def configure_keyboard(self, keyboard): self._computer.keyboard = keyboard
    
    def get_result(self) -> Computer:
        return self._computer

# --- PASO 4: El Director (Opcional pero Recomendado) ---
class Director:
    """
    El Director sabe en qué orden ejecutar los pasos para configuraciones famosas.
    """
    def __init__(self):
        self._builder = None

    @property
    def builder(self) -> ComputerBuilder:
        return self._builder

    @builder.setter
    def builder(self, builder: ComputerBuilder):
        self._builder = builder

    def build_minimal_pc(self):
        self.builder.configure_cpu("Intel i3")
        self.builder.configure_ram("8GB")
        self.builder.configure_storage("256GB SSD")

    def build_pro_gaming_pc(self):
        self.builder.configure_cpu("Ryzen 9")
        self.builder.configure_ram("64GB")
        self.builder.configure_storage("2TB NVMe")
        self.builder.configure_gpu("RTX 4090")
        self.builder.configure_screen("4K OLED")
        self.builder.configure_keyboard("Mecánico Mecánico")

# --- SIMULACIÓN DE EJECUCIÓN ---
if __name__ == "__main__":
    director = Director()
    
    # 1. Construcción usando el Director (Receta predefinida)
    print("--- Construyendo PC Gamer Pro vía Director ---")
    gaming_builder = GamingBuilder()
    director.builder = gaming_builder
    director.build_pro_gaming_pc()
    pc_pro = gaming_builder.get_result()
    print(pc_pro)

    # 2. Construcción personalizada (El cliente usa el Builder directamente)
    print("\n--- Construyendo PC personalizada vía Builder ---")
    office_builder = OfficeBuilder()
    office_builder.configure_cpu("Intel i5")
    office_builder.configure_ram("16GB")
    office_builder.configure_storage("500GB SSD")
    office_builder.configure_keyboard("Teclado Ergonómico")
    # No configuramos GPU ni Pantalla, el Builder maneja los valores por defecto
    pc_custom = office_builder.get_result()
    print(pc_custom)

    print("\nÉXITO: Se eliminó el constructor telescópico y el proceso es claro.")
