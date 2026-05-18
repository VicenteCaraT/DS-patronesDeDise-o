import uuid

class DatabaseConnector:
    """
    Clase que simula una conexión a una base de datos.
    Refactorizada para ser un Singleton usando el método __new__.
    """
    # 1. Atributos de clase (compartidos por toda la clase)
    _instance = None           # Aquí guardaremos la única instancia
    _is_initialized = False    # Bandera para evitar que __init__ se ejecute múltiples veces

    def __new__(cls, *args, **kwargs):
        """
        __new__ es el verdadero constructor en Python. Se llama antes de __init__.
        Aquí controlamos si creamos un nuevo objeto o devolvemos el existente.
        """
        # Si aún no existe la instancia, la creamos llamando al __new__ padre (object)
        if cls._instance is None:
            # Creamos la instancia en memoria
            cls._instance = super(DatabaseConnector, cls).__new__(cls)
        
        # Devolvemos la instancia (ya sea la recién creada o la que ya existía)
        return cls._instance

    def __init__(self):
        """
        __init__ inicializa el objeto. Como __new__ devuelve siempre la instancia,
        Python intentará ejecutar __init__ cada vez que hagamos `DatabaseConnector()`.
        Debemos controlarlo para que la conexión costosa solo ocurra una vez.
        """
        # Verificamos si ya fue inicializado
        if not self.__class__._is_initialized:
            self.id = str(uuid.uuid4())
            print("--- ESTABLECIENDO CONEXIÓN COSTOSA ---")
            print(f"Conexión establecida con ID: {self.id}")
            
            # Marcamos la clase como inicializada para las futuras llamadas
            self.__class__._is_initialized = True

    def ejecutar_consulta(self, sql):
        print(f"Ejecutando [{sql}] usando conexión ID: {self.id}")

class UsuarioService:
    def login(self):
        # Al hacer esto, __new__ detecta que ya hay una instancia y la devuelve.
        db = DatabaseConnector()
        db.ejecutar_consulta("SELECT * FROM usuarios WHERE id = 1")

class ProductoService:
    def listar(self):
        # Al hacer esto de nuevo, se devuelve exactamente el mismo objeto.
        db = DatabaseConnector()
        db.ejecutar_consulta("SELECT * FROM productos")

# --- SIMULACIÓN DE EJECUCIÓN ---
if __name__ == "__main__":
    print("Iniciando aplicación...\n")
    
    u = UsuarioService()
    p = ProductoService()

    u.login()
    p.listar()

    print("\nÉXITO: Ambas consultas utilizan el mismo ID de conexión.")
    
    # Verificación final de identidad en memoria
    db1 = DatabaseConnector()
    db2 = DatabaseConnector()
    print(f"\n¿db1 y db2 son el mismo objeto en memoria?: {db1 is db2}")
