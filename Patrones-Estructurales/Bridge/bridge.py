from abc import ABC, abstractmethod

# --- JERARQUÍA DE IMPLEMENTACIÓN (El "Cómo") ---
class Color(ABC):
    @abstractmethod
    def get_name(self):
        pass

class RedColor(Color):
    def get_name(self):
        return "ROJO"

class BlueColor(Color):
    def get_name(self):
        return "AZUL"

class GreenColor(Color): # ¡Añadir un color es ahora trivial!
    def get_name(self):
        return "VERDE"

# --- JERARQUÍA DE ABSTRACCIÓN (El "Qué") ---
class Shape(ABC):
    def __init__(self, color: Color):
        # Aquí está el PUENTE (Bridge)
        # La forma NO hereda del color, LO TIENE (Composición)
        self.color = color

    @abstractmethod
    def draw(self):
        pass

class Circle(Shape):
    def draw(self):
        print(f"Dibujando Círculo de color {self.color.get_name()}")

class Square(Shape):
    def draw(self):
        print(f"Dibujando Cuadrado de color {self.color.get_name()}")

# --- SIMULACIÓN DE EJECUCIÓN (Refactorizada) ---
if __name__ == "__main__":
    print("Iniciando renderizado con el patrón Bridge...\n")
    
    # 1. Creamos los colores
    rojo = RedColor()
    azul = BlueColor()
    verde = GreenColor()

    # 2. Creamos las formas inyectando el color (El puente en acción)
    # Ya no necesitamos clases como 'CircleRed' o 'SquareBlue'
    circulo_rojo = Circle(rojo)
    cuadrado_azul = Square(azul)
    circulo_verde = Circle(verde) # Funciona sin haber creado una clase CircleGreen

    circulo_rojo.draw()
    cuadrado_azul.draw()
    circulo_verde.draw()

    print("\nÉXITO ARQUITECTÓNICO:")
    print("- Hemos pasado de tener N*M clases a tener N+M clases.")
    print("- Las formas y los colores pueden crecer independientemente.")
