import copy
from abc import ABC, abstractmethod

# --- PASO 1: Interfaz Prototipo ---
class Prototype(ABC):
    @abstractmethod
    def clone(self):
        """
        Cada subclase debe saber cómo clonarse a sí misma.
        """
        pass

# --- PASO 2: Implementación del Prototipo Concreto ---
class Document(Prototype):
    """
    Representa un documento con contenido y metadatos.
    Ahora implementa Prototype para manejar su propia duplicación.
    """
    def __init__(self, title, content):
        self.title = title
        self.content = content
        # Atributo 'privado' y complejo (un diccionario)
        self._metadata = {"version": "1.0", "status": "Draft"} 
        self.tags = []
        
        # Simulación de un proceso de creación costoso (ej. consulta a BD)
        print(f"\n--- [LOG] Consultando Base de Datos para '{self.title}' ---")

    def add_tag(self, tag):
        self.tags.append(tag)

    def clone(self):
        """
        Implementación del clonado usando 'deepcopy'.
        'deepcopy' copia el objeto y TODO su contenido de forma recursiva.
        IMPORTANTE: deepcopy NO llama al método __init__, por lo que 
        evitamos el proceso costoso de creación.
        """
        print(f"--- [LOG] Clonando el documento: {self.title} ---")
        return copy.deepcopy(self)

    def __str__(self):
        return f"Doc: {self.title} | Tags: {self.tags} | Metadata: {self._metadata}"

# --- SIMULACIÓN DE EJECUCIÓN (Refactorizada) ---
if __name__ == "__main__":
    # 1. Creamos el documento original (paga el costo inicial)
    doc_original = Document("Reporte Anual", "Contenido confidencial...")
    doc_original.add_tag("Finanzas")
    print(f"Original Inicial: {doc_original}")

    # 2. El cliente clona el objeto sin saber cómo está construido por dentro
    # Ya no usamos 'new Document()', por lo que no se repite el proceso costoso.
    doc_v2 = doc_original.clone()
    
    # 3. Modificamos la copia para verificar independencia
    doc_v2.title = "Reporte Anual V2"
    doc_v2.add_tag("Revisado")
    doc_v2._metadata["version"] = "2.0" # Podemos modificar atributos internos de forma segura

    print("\n--- RESULTADOS FINALES ---")
    print(f"Original: {doc_original}")
    print(f"Copia V2 : {doc_v2}")

    # --- ANÁLISIS ARQUITECTÓNICO ---
    # 1. Eficiencia: El LOG de BD solo apareció UNA vez.
    # 2. Encapsulamiento: El cliente no tuvo que copiar los tags ni la metadata manualmente.
    # 3. Independencia: Los cambios en la V2 no afectaron al Original (gracias a deepcopy).
    print(f"\n¿Son el mismo objeto en memoria?: {doc_original is doc_v2}")
