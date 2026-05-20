from abc import ABC, abstractmethod

# --- PASO 1: Interfaz del Visitante ---
# Define un método para cada tipo de elemento que puede ser visitado.
class InsuranceVisitor(ABC):
    @abstractmethod
    def visit_life(self, policy): pass
    
    @abstractmethod
    def visit_health(self, policy): pass
    
    @abstractmethod
    def visit_property(self, policy): pass


# --- PASO 2: Interfaz del Elemento (Contrato de Aceptación) ---
class Insurance(ABC):
    @abstractmethod
    def accept(self, visitor: InsuranceVisitor):
        """
        Este es el núcleo del patrón: el Doble Despacho (Double Dispatch).
        El elemento acepta al visitante y le dice exactamente qué método llamar.
        """
        pass


# --- PASO 3: Elementos Concretos (Solo contienen DATOS) ---

class LifeInsurance(Insurance):
    def __init__(self, coverage):
        self.coverage = coverage

    def accept(self, visitor: InsuranceVisitor):
        # El objeto sabe que es de tipo 'Life', por eso llama a 'visit_life'
        visitor.visit_life(self)

class HealthInsurance(Insurance):
    def __init__(self, age):
        self.age = age

    def accept(self, visitor: InsuranceVisitor):
        visitor.visit_health(self)

class PropertyInsurance(Insurance):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor: InsuranceVisitor):
        visitor.visit_property(self)


# --- PASO 4: Visitantes Concretos (Algoritmos Externalizados) ---

class RiskCalculator(InsuranceVisitor):
    """Primer algoritmo: Calcula el riesgo de cada póliza."""
    def visit_life(self, policy: LifeInsurance):
        risk = policy.coverage * 0.05
        print(f"[CÁLCULO RIESGO] Vida: {risk}")

    def visit_health(self, policy: HealthInsurance):
        risk = policy.age * 10
        print(f"[CÁLCULO RIESGO] Salud: {risk}")

    def visit_property(self, policy: PropertyInsurance):
        risk = policy.value * 0.01
        print(f"[CÁLCULO RIESGO] Propiedad: {risk}")


class ReportGenerator(InsuranceVisitor):
    """Segundo algoritmo: Genera reportes textuales."""
    def visit_life(self, policy: LifeInsurance):
        print(f"[REPORTE] Póliza de Vida. Cobertura: ${policy.coverage}")

    def visit_health(self, policy: HealthInsurance):
        print(f"[REPORTE] Póliza de Salud. Edad asegurado: {policy.age} años")

    def visit_property(self, policy: PropertyInsurance):
        print(f"[REPORTE] Póliza de Propiedad. Valor del inmueble: ${policy.value}")


# --- SIMULACIÓN DE EJECUCIÓN (Refactorizada) ---
if __name__ == "__main__":
    # 1. Tenemos nuestra estructura de objetos (Pólizas)
    polizas = [
        LifeInsurance(100000),
        HealthInsurance(45),
        PropertyInsurance(250000)
    ]

    # 2. Queremos ejecutar el cálculo de riesgos
    print("--- INICIANDO CÁLCULO DE RIESGOS ---")
    calculator = RiskCalculator()
    for p in polizas:
        p.accept(calculator)

    print("\n" + "-"*40 + "\n")

    # 3. Ahora queremos generar reportes (Misma estructura, distinta operación)
    print("--- GENERANDO REPORTES ---")
    reporter = ReportGenerator()
    for p in polizas:
        p.accept(reporter)

    # --- ANÁLISIS ARQUITECTÓNICO ---
    # 1. SRP: Las pólizas solo tienen datos. Los algoritmos viven en los Visitantes.
    # 2. OCP: Si queremos añadir un algoritmo 'TaxCalculator', solo creamos la clase 
    #    sin tocar ninguna póliza ni los visitantes anteriores.
    # 3. Double Dispatch: Fíjate que el bucle 'for' trata a todos como 'Insurance',
    #    pero gracias al método 'accept', se ejecuta la lógica específica correcta.
    
    print("\nÉXITO: Algoritmos desacoplados de la estructura de datos.")
