from abc import ABC, abstractmethod

# --- PASO 1: El Componente (Interfaz) ---
# Todos los cafés (el básico y los decorados) deben seguir este contrato.
class Coffee(ABC):
    @abstractmethod
    def get_cost(self):
        pass
    
    @abstractmethod
    def get_description(self):
        pass

# --- PASO 2: Componente Concreto ---
# El objeto básico al que le añadiremos funcionalidades.
class BasicCoffee(Coffee):
    def get_cost(self):
        return 5.0
    
    def get_description(self):
        return "Café Básico"

# --- PASO 3: Decorador Base ---
# Esta clase es la clave: es un café (hereda de Coffee) 
# y a la vez contiene un café (composición).
class CoffeeDecorator(Coffee):
    def __init__(self, coffee: Coffee):
        self._decorated_coffee = coffee

    def get_cost(self):
        # Por defecto, delega la llamada al objeto envuelto
        return self._decorated_coffee.get_cost()

    def get_description(self):
        # Por defecto, delega la llamada al objeto envuelto
        return self._decorated_coffee.get_description()

# --- PASO 4: Decoradores Concretos ---
# Cada uno añade su propia lógica antes o después de delegar.
class MilkDecorator(CoffeeDecorator):
    def get_cost(self):
        # Sumamos el costo de la leche al costo del café que ya tenemos
        return self._decorated_coffee.get_cost() + 2.0
    
    def get_description(self):
        return self._decorated_coffee.get_description() + ", con Leche"

class SugarDecorator(CoffeeDecorator):
    def get_cost(self):
        return self._decorated_coffee.get_cost() + 1.0
    
    def get_description(self):
        return self._decorated_coffee.get_description() + ", con Azúcar"

class VanillaDecorator(CoffeeDecorator):
    def get_cost(self):
        return self._decorated_coffee.get_cost() + 3.0
    
    def get_description(self):
        return self._decorated_coffee.get_description() + ", con Vainilla"

# --- SIMULACIÓN DE EJECUCIÓN (Poder del Decorator) ---
if __name__ == "__main__":
    print("--- BIENVENIDO A LA CAFETERÍA ARQUITECTÓNICA ---")
    
    # 1. Empezamos con un café básico
    pedido = BasicCoffee()
    
    # 2. El cliente quiere añadirle leche (lo envolvemos)
    pedido = MilkDecorator(pedido)
    
    # 3. El cliente también quiere azúcar (lo volvemos a envolver)
    pedido = SugarDecorator(pedido)
    
    # 4. Y por qué no, ¡un toque de vainilla! (tercer envoltorio)
    pedido = VanillaDecorator(pedido)

    # Cuando llamamos a los métodos, la llamada atraviesa todas las capas (la cebolla)
    print(f"\nTu pedido: {pedido.get_description()}")
    print(f"Costo Total: ${pedido.get_cost()}")

    # --- PRUEBA DE FLEXIBILIDAD ---
    # Podemos crear combinaciones raras sin haber definido clases para ellas
    cafe_raro = MilkDecorator(MilkDecorator(BasicCoffee())) # ¡Doble leche!
    print(f"\nPedido Raro: {cafe_raro.get_description()}")
    print(f"Costo Raro: ${cafe_raro.get_cost()}")

    print("\nÉXITO ARQUITECTÓNICO:")
    print("1. No hay explosión de clases. Con 3 decoradores hacemos infinitas combinaciones.")
    print("2. Podemos añadir ingredientes en tiempo de ejecución de forma dinámica.")
