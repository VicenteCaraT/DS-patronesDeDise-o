import copy

# --- PASO 1: El Memento (El Recuerdo) ---
class HeroMemento:
    """
    Objeto inmutable que guarda una 'foto' del estado del Hero.
    Solo debe ser leído por el Hero.
    """
    def __init__(self, level, hp, inventory):
        # Guardamos copias para evitar que el Hero y el Memento
        # compartan referencias a objetos mutables (como listas).
        self._level = level
        self._hp = hp
        self._inventory = copy.deepcopy(inventory)

    # El Memento es básicamente una caja negra con datos de solo lectura
    @property
    def level(self): return self._level
    @property
    def hp(self): return self._hp
    @property
    def inventory(self): return self._inventory


# --- PASO 2: El Originador (El Hero) ---
class Hero:
    """
    Es el dueño de su estado. Él decide qué se guarda y qué se restaura.
    """
    def __init__(self, name):
        self.name = name
        self._level = 1
        self._hp = 100
        self._inventory = ["Espada de madera"]

    def take_damage(self, amount):
        self._hp -= amount
        print(f"--- [HERO] {self.name} recibió daño. HP actual: {self._hp} ---")

    def add_item(self, item):
        self._inventory.append(item)

    # CREAR EL MEMENTO
    def save(self) -> HeroMemento:
        print(f"[HERO] Guardando estado interno...")
        return HeroMemento(self._level, self._hp, self._inventory)

    # RESTAURAR DESDE EL MEMENTO
    def restore(self, memento: HeroMemento):
        self._level = memento.level
        self._hp = memento.hp
        self._inventory = copy.deepcopy(memento.inventory)
        print(f"[HERO] Estado restaurado con éxito.")

    def __str__(self):
        return f"Hero: {self.name} | Nivel: {self._level} | HP: {self._hp} | Items: {self._inventory}"


# --- PASO 3: El Cuidador (Caretaker - Historial) ---
class GameHistory:
    """
    Se encarga de guardar los mementos, pero no sabe qué hay dentro.
    """
    def __init__(self):
        self._checkpoints = []

    def push(self, memento: HeroMemento):
        self._checkpoints.append(memento)

    def pop(self) -> HeroMemento:
        if not self._checkpoints:
            return None
        return self._checkpoints.pop()


# --- SIMULACIÓN DE EJECUCIÓN (Refactorizada) ---
if __name__ == "__main__":
    link = Hero("Link")
    history = GameHistory()

    # 1. Guardamos el estado inicial
    history.push(link.save())
    print(f"Inicio: {link}")

    # 2. Link progresa y luego sufre daño
    link.add_item("Escudo Hyliano")
    link.take_damage(50)
    print(f"Después de batalla 1: {link}")
    
    # 3. Guardamos otro punto de control
    history.push(link.save())

    # 4. Desastre total
    link.take_damage(60)
    link.add_item("Botas de hierro (pesadas)")
    print(f"Estado crítico: {link}")

    # 5. El jugador decide volver al último guardado
    print("\n--- [SISTEMA] Cargando último Checkpoint... ---")
    ultimo_memento = history.pop()
    link.restore(ultimo_memento)
    print(f"Resultado: {link}")

    # 6. ¿Y si queremos volver al inicio de todo?
    print("\n--- [SISTEMA] Cargando primer Checkpoint... ---")
    primer_memento = history.pop()
    link.restore(primer_memento)
    print(f"Resultado Final: {link}")

    # --- ANÁLISIS ARQUITECTÓNICO ---
    # 1. Encapsulamiento: El motor del juego (este main) ya no sabe que Hero tiene '_hp'.
    # 2. SRP: El Hero gestiona su vida, el GameHistory gestiona el historial.
    # 3. Flexibilidad: Si el Hero añade nuevos campos, solo modificamos la clase Hero y HeroMemento.
    #    La clase GameHistory y el código cliente quedan intactos.
