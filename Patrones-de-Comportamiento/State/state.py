from abc import ABC, abstractmethod

# --- PASO 1: Interfaz del Estado (El Contrato) ---
class State(ABC):
    """
    Define los comportamientos que dependen del estado.
    Cada método recibe el 'contexto' (VendingMachine) para poder 
    alterar su estado interno (transición).
    """
    @abstractmethod
    def insert_coin(self, machine): pass
    
    @abstractmethod
    def eject_coin(self, machine): pass
    
    @abstractmethod
    def press_button(self, machine): pass
    
    @abstractmethod
    def dispense(self, machine): pass


# --- PASO 2: Estados Concretos ---

class IdleState(State):
    """Estado: Esperando moneda."""
    def insert_coin(self, machine):
        print("[IDLE] Moneda insertada con éxito.")
        machine.set_state(machine.has_coin_state) # Transición a 'Tiene Moneda'

    def eject_coin(self, machine):
        print("[IDLE] No hay ninguna moneda que devolver.")

    def press_button(self, machine):
        print("[IDLE] Botón presionado, pero no hay moneda.")

    def dispense(self, machine):
        print("[IDLE] Pago requerido primero.")


class HasCoinState(State):
    """Estado: Moneda aceptada, esperando selección."""
    def insert_coin(self, machine):
        print("[HAS_COIN] Error: Ya existe una moneda en la ranura.")

    def eject_coin(self, machine):
        print("[HAS_COIN] Moneda devuelta.")
        machine.set_state(machine.idle_state) # Transición de regreso a 'Esperando'

    def press_button(self, machine):
        print("[HAS_COIN] Selección aceptada. Procesando...")
        machine.set_state(machine.sold_state) # Transición a 'Vendido'
        machine.dispense() # Llamada automática al siguiente paso

    def dispense(self, machine):
        print("[HAS_COIN] Operación no permitida en este paso.")


class SoldState(State):
    """Estado: Entregando producto."""
    def insert_coin(self, machine):
        print("[SOLD] Espere, estamos entregando su producto.")

    def eject_coin(self, machine):
        print("[SOLD] Lo siento, ya presionó el botón. No hay devolución.")

    def press_button(self, machine):
        print("[SOLD] Ya estamos procesando su pedido.")

    def dispense(self, machine):
        machine.release_product() # Acción real del contexto
        if machine.count > 0:
            machine.set_state(machine.idle_state)
        else:
            print("[SOLD] ¡Agotado!")
            machine.set_state(machine.out_of_stock_state)


class OutOfStockState(State):
    """Estado: Sin existencias."""
    def insert_coin(self, machine):
        print("[OUT_OF_STOCK] No aceptamos monedas, no hay stock.")

    def eject_coin(self, machine):
        print("[OUT_OF_STOCK] No hay moneda que devolver.")

    def press_button(self, machine):
        print("[OUT_OF_STOCK] Botón presionado, pero no hay productos.")

    def dispense(self, machine):
        print("[OUT_OF_STOCK] Error crítico de dispensado.")


# --- PASO 3: El Contexto (La Máquina de Vending) ---
class VendingMachine:
    """
    La máquina ya no tiene 'if/else'. 
    Simplemente delega todo al objeto estado actual.
    """
    def __init__(self, count):
        self.count = count
        
        # Inicializamos los objetos de estado (para no recrearlos)
        self.idle_state = IdleState()
        self.has_coin_state = HasCoinState()
        self.sold_state = SoldState()
        self.out_of_stock_state = OutOfStockState()

        # Estado inicial
        if self.count > 0:
            self.current_state = self.idle_state
        else:
            self.current_state = self.out_of_stock_state

    def set_state(self, state: State):
        """Método para cambiar de estado (usado por los propios estados)"""
        self.current_state = state

    # Métodos delegados (La "Fachada" hacia los estados)
    def insert_coin(self): self.current_state.insert_coin(self)
    def eject_coin(self): self.current_state.eject_coin(self)
    def press_button(self): self.current_state.press_button(self)
    def dispense(self): self.current_state.dispense(self)

    def release_product(self):
        """Acción de bajo nivel que solo la máquina sabe hacer"""
        if self.count > 0:
            self.count -= 1
            print(f"--- [MÁQUINA] Soltando producto... (Quedan: {self.count}) ---")


# --- SIMULACIÓN DE EJECUCIÓN (Refactorizada) ---
if __name__ == "__main__":
    print("--- INICIANDO MÁQUINA DE VENDING CON PATRÓN STATE ---")
    maquina = VendingMachine(count=1)

    # Flujo normal:
    maquina.insert_coin()
    maquina.press_button()

    # Intentar comprar sin stock:
    print("\n--- INTENTANDO COMPRA EXTRA ---")
    maquina.insert_coin()
    maquina.press_button()

    # --- ANÁLISIS ARQUITECTÓNICO ---
    # 1. Adiós condicionales: El flujo está encapsulado en clases independientes.
    # 2. OCP: Si queremos un 'Modo Mantenimiento', solo creamos 'MaintenanceState' 
    #    sin tocar la lógica de los otros estados.
    # 3. Transiciones Explícitas: Es fácil seguir el camino que recorre el objeto.
