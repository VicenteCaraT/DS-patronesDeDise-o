import sys

# --- PASO 1: El Flyweight (Estado Intrínseco) ---
class TreeType:
    """
    Contiene el estado compartido (pesado y constante).
    Muchos árboles apuntarán a una sola instancia de esta clase.
    """
    def __init__(self, name, color, texture_data):
        self.name = name
        self.color = color
        self.texture_data = texture_data # Objeto pesado

    def draw(self, x, y):
        # El Flyweight recibe el estado extrínseco (x, y) para actuar
        # print(f"Dibujando {self.name} {self.color} en ({x}, {y})")
        pass

# --- PASO 2: La Fábrica de Flyweights ---
class TreeFactory:
    """
    Gestiona la creación y reutilización de los tipos de árboles.
    Asegura que no se creen duplicados del mismo tipo pesado.
    """
    _tree_types = {}

    @classmethod
    def get_tree_type(cls, name, color, texture_data):
        # Creamos una clave única para identificar el tipo
        key = f"{name}_{color}"
        
        if key not in cls._tree_types:
            print(f"[FÁBRICA] Creando nuevo tipo de árbol pesado: {key}")
            cls._tree_types[key] = TreeType(name, color, texture_data)
        else:
            # print(f"[FÁBRICA] Reutilizando tipo existente: {key}")
            pass
            
        return cls._tree_types[key]

# --- PASO 3: El Contexto (Estado Extrínseco) ---
class Tree:
    """
    Representa el objeto ligero que el cliente maneja en masa.
    Solo guarda sus coordenadas únicas y una referencia al Flyweight.
    """
    def __init__(self, x, y, tree_type: TreeType):
        self.x = x
        self.y = y
        self.tree_type = tree_type # Referencia al objeto compartido

    def draw(self):
        # Delegamos el dibujado al objeto pesado pasándole nuestra posición
        self.tree_type.draw(self.x, self.y)

# --- SIMULACIÓN DE EJECUCIÓN (Refactorizada con Flyweight) ---
if __name__ == "__main__":
    print("--- SIMULACIÓN DE BOSQUE OPTIMIZADO (Con Flyweight) ---\n")
    
    # 1. Creamos la textura pesada una sola vez
    heavy_texture = "X" * 1024 * 1024 # 1MB de datos
    
    bosque = []
    
    # 2. Plantamos 10,000 árboles
    for i in range(10000):
        # La fábrica asegura que la textura de 1MB solo se guarde UNA VEZ en RAM
        tipo = TreeFactory.get_tree_type("Pino", "Verde Oscuro", heavy_texture)
        
        # El objeto 'arbol' es muy ligero (solo 2 ints y 1 referencia)
        arbol = Tree(i, i, tipo)
        bosque.append(arbol)

    print(f"\nCantidad de árboles en el bosque: {len(bosque)}")
    
    # --- ANÁLISIS ARQUITECTÓNICO ---
    # Sin Flyweight: 10,000 árboles * 1MB = 10,000 MB (10 GB)
    # Con Flyweight: 1 textura * 1MB + 10,000 punteros = ~1.5 MB
    
    print(f"Instancias de TreeType creadas: {len(TreeFactory._tree_types)}")
    print(f"Memoria RAM ocupada por texturas: {len(TreeFactory._tree_types) * 1} MB")
    
    print("\nÉXITO ARQUITECTÓNICO:")
    print("1. El ahorro de memoria es del 99.99%.")
    print("2. Los datos intrínsecos (textura, nombre) están centralizados e inmutables.")
    print("3. Podemos escalar el bosque a millones de árboles sin colapsar la RAM.")
