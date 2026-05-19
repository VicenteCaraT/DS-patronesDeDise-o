class ModernReportingSystem:
    """
    El sistema moderno espera trabajar con objetos que tengan 
    un método llamado 'get_json_data'.
    """
    def generate_report(self, data_provider):
        print("--- [SISTEMA MODERNO] Iniciando proceso de reporte ---")
        data = data_provider.get_json_data()
        print(f"--- [SISTEMA MODERNO] Reporte finalizado con datos: {data}")

class LegacyAccountingSystem:
    """
    Librería antigua que no podemos modificar. 
    Sus datos están en XML y su método se llama 'fetch_xml_data'.
    """
    def fetch_xml_data(self):
        # Simulación de datos en formato XML
        return "<xml><monto>1500</monto><moneda>USD</moneda></xml>"

# --- PASO 1 y 2: El Adaptador ---
class AccountingAdapter:
    """
    Esta clase actúa como el PUENTE. 
    Implementa la interfaz que el cliente espera (get_json_data)
    y envuelve la clase que queremos adaptar.
    """
    def __init__(self, legacy_system: LegacyAccountingSystem):
        # Guardamos la instancia del sistema viejo (Composición)
        self.legacy_system = legacy_system

    def get_json_data(self):
        """
        Traducción de XML a JSON.
        """
        print("--- [ADAPTADOR] Traduciendo de XML a JSON... ---")
        
        # 1. Llamamos al método del sistema antiguo
        xml_data = self.legacy_system.fetch_xml_data()
        
        # 2. Lógica de conversión (Simulada)
        # En la vida real, aquí usarías una librería como xmltodict o json
        if "1500" in xml_data and "USD" in xml_data:
            json_data = '{"monto": 1500, "moneda": "USD"}'
        
        # 3. Retornamos lo que el sistema moderno espera
        return json_data

# --- SIMULACIÓN DE EJECUCIÓN (Refactorizada) ---
if __name__ == "__main__":
    # Instanciamos los dos mundos
    report_system = ModernReportingSystem()
    legacy_system = LegacyAccountingSystem()

    print("CASO 1: Usando el Adaptador para unir los dos sistemas")
    
    # Creamos el adaptador envolviendo al sistema viejo
    adapter = AccountingAdapter(legacy_system)

    # Ahora el sistema moderno acepta al adaptador porque este 
    # tiene el método 'get_json_data'
    report_system.generate_report(adapter)

    print("\nÉXITO: El sistema moderno ni siquiera se enteró que los datos venían de un XML viejo.")
