from abc import ABC, abstractmethod

# --- PASO 1: La Clase Abstracta (El Esqueleto) ---
class ReportGenerator(ABC):
    """
    Define el Template Method que contiene el esqueleto del algoritmo.
    La estructura del proceso de reporte es FIJA, pero los detalles 
    son delegados a las subclases.
    """
    
    def generate_report(self):
        """
        Este es el MÉTODO PLANTILLA. 
        Controla el flujo de ejecución de principio a fin.
        """
        print(f"--- [SISTEMA] Iniciando generación de reporte ---")
        
        # 1. Paso Común (Lógica centralizada)
        self._validate_data()
        
        # 2. Pasos Abstractos (Delegados a los hijos)
        self.create_header()
        self.create_content()
        
        # 3. Hook (Gancho opcional)
        if self.should_add_footer():
            self.create_footer()
            
        print(f"--- [SISTEMA] Proceso finalizado con éxito ---\n")

    def _validate_data(self):
        """Paso común implementado en el padre para evitar duplicación."""
        print("[COMÚN] Validando integridad de los datos...")

    @abstractmethod
    def create_header(self): pass

    @abstractmethod
    def create_content(self): pass

    @abstractmethod
    def create_footer(self): pass

    def should_add_footer(self):
        """
        Esto es un HOOK. Las subclases pueden sobrescribirlo para 
        alterar el algoritmo, pero no es obligatorio.
        """
        return True


# --- PASO 2: Implementaciones Concretas ---

class PDFReportGenerator(ReportGenerator):
    """Especialista en formato PDF."""
    def create_header(self):
        print("[PDF] Dibujando encabezado con logo vectorial.")

    def create_content(self):
        print("[PDF] Insertando tablas y texto en formato de página fijo.")

    def create_footer(self):
        print("[PDF] Añadiendo numeración de páginas y marca de agua.")


class HTMLReportGenerator(ReportGenerator):
    """Especialista en formato HTML."""
    def create_header(self):
        print("[HTML] Creando etiqueta <header> con estilos CSS inline.")

    def create_content(self):
        print("[HTML] Insertando etiquetas <div> y <p> con datos dinámicos.")

    def create_footer(self):
        print("[HTML] Creando etiqueta <footer> con links de redes sociales.")

    def should_add_footer(self):
        # El reporte HTML decide NO incluir pie de página esta vez
        return False


# --- SIMULACIÓN DE EJECUCIÓN (Refactorizada) ---
if __name__ == "__main__":
    # Generando PDF
    print("EJECUTANDO REPORTE PDF:")
    pdf = PDFReportGenerator()
    pdf.generate_report()

    # Generando HTML
    print("EJECUTANDO REPORTE HTML:")
    html = HTMLReportGenerator()
    html.generate_report()

    # --- ANÁLISIS ARQUITECTÓNICO ---
    # 1. Eliminación de Duplicación: El flujo (Header -> Content -> Footer) vive solo en la base.
    # 2. Control de Proceso: El padre asegura que siempre se valide la data antes de empezar.
    # 3. Flexibilidad (Hooks): El generador HTML pudo quitar el footer sin romper la estructura.
    # 4. Hollywood Principle: Los hijos no llaman al padre, el padre decide cuándo llamar a los hijos.
