from abc import ABC, abstractmethod

# --- PASO 1: El Componente (Interfaz Común) ---
class OrganizationComponent(ABC):
    """
    Esta interfaz unifica el trato entre elementos simples (hojas)
    y elementos complejos (contenedores).
    """
    @abstractmethod
    def get_salary(self) -> float:
        pass

# --- PASO 2: La Hoja (Leaf) ---
class Employee(OrganizationComponent):
    """
    Representa un objeto simple sin hijos.
    Hace el trabajo real (en este caso, devolver su salario).
    """
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def get_salary(self) -> float:
        return self.salary

# --- PASO 3: El Compuesto (Composite) ---
class Department(OrganizationComponent):
    """
    Representa un contenedor complejo.
    No le importa qué tipo de hijos tiene, siempre y cuando 
    cumplan con la interfaz 'OrganizationComponent'.
    """
    def __init__(self, name):
        self.name = name
        # ¡Magia del patrón!: Una sola lista unificada para todo
        self._children = []

    def add(self, component: OrganizationComponent):
        """Método unificado para agregar componentes"""
        self._children.append(component)

    def remove(self, component: OrganizationComponent):
        self._children.remove(component)

    def get_salary(self) -> float:
        """
        Delega el trabajo a los hijos y recolecta los resultados.
        Aquí ocurre la recursividad natural sin usar condicionales.
        """
        total = 0
        for child in self._children:
            # Polimorfismo: child puede ser un Employee o un Department
            total += child.get_salary() 
        return total

# --- SIMULACIÓN DE EJECUCIÓN (Refactorizada) ---
if __name__ == "__main__":
    print("--- Creando estructura organizacional ---")
    
    # 1. Hojas (Empleados)
    juan = Employee("Juan (Ventas INT)", 1000)
    maria = Employee("Maria (Ventas INT)", 1200)
    pedro = Employee("Pedro (Ventas LOC)", 800)
    ana = Employee("Ana (Directora)", 3000)

    # 2. Compuestos (Departamentos)
    ventas_internacional = Department("Ventas Internacional")
    ventas_internacional.add(juan)
    ventas_internacional.add(maria)

    ventas_local = Department("Ventas Local")
    ventas_local.add(pedro)

    # 3. Compuesto Raíz
    empresa_general = Department("Sede Central")
    empresa_general.add(ana) # Empleado directo a nivel global
    empresa_general.add(ventas_internacional) # Sub-departamento
    empresa_general.add(ventas_local)         # Sub-departamento

    # --- TRANSPARENCIA EN ACCIÓN ---
    print("\n--- Calculando Salarios ---")
    print(f"Salario de una persona sola (Juan): {juan.get_salary()}")
    print(f"Salario de un sub-departamento (Internacional): {ventas_internacional.get_salary()}")
    print(f"Salario TOTAL de la Empresa (Raíz): {empresa_general.get_salary()}")

    print("\nÉXITO ARQUITECTÓNICO:")
    print("1. El cliente trató a objetos individuales (Employee) y grupos (Department) exactamente igual (usando get_salary()).")
    print("2. Desaparecieron las múltiples listas y la necesidad de usar 'isinstance'.")
