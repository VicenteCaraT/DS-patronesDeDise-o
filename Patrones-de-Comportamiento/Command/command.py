from abc import ABC, abstractmethod

# --- RECEPTOR (El que sabe hacer el trabajo real) ---
class TextEditor:
    def __init__(self):
        self.text = "Hola Mundo"
        self.clipboard = ""

    def copy(self):
        self.clipboard = self.text
        print(f"[EDITOR] Texto copiado: '{self.clipboard}'")

    def paste(self):
        self.text += self.clipboard
        print(f"[EDITOR] Texto pegado. Contenido actual: '{self.text}'")


# --- PASO 1: Interfaz del Comando ---
class Command(ABC):
    """
    La interfaz común para todas las acciones.
    Añadimos 'undo' para demostrar el poder del patrón.
    """
    @abstractmethod
    def execute(self): pass
    
    @abstractmethod
    def undo(self): pass


# --- PASO 2: Comandos Concretos ---
class CopyCommand(Command):
    def __init__(self, editor: TextEditor):
        self.editor = editor
        self._backup_clipboard = ""

    def execute(self):
        # Guardamos el estado anterior antes de actuar (para el undo)
        self._backup_clipboard = self.editor.clipboard
        self.editor.copy()

    def undo(self):
        self.editor.clipboard = self._backup_clipboard
        print(f"[UNDO] Portapapeles restaurado a: '{self.editor.clipboard}'")


class PasteCommand(Command):
    def __init__(self, editor: TextEditor):
        self.editor = editor
        self._backup_text = ""

    def execute(self):
        # Guardamos el estado anterior antes de actuar (para el undo)
        self._backup_text = self.editor.text
        self.editor.paste()

    def undo(self):
        self.editor.text = self._backup_text
        print(f"[UNDO] Texto restaurado a: '{self.editor.text}'")


# --- PASO 3: Invocador (El botón genérico) ---
class Button:
    """
    El botón ahora es 100% genérico. No sabe NADA del TextEditor.
    Solo sabe que tiene un objeto 'Command' al que puede llamar.
    """
    def __init__(self, name: str, command: Command):
        self.name = name
        self.command = command

    def click(self):
        print(f"\n--- Botón '{self.name}' presionado ---")
        self.command.execute()
        return self.command # Retornamos el comando para guardarlo en el historial


# --- PASO 4: El Historial (Ventaja Arquitectónica) ---
class CommandHistory:
    def __init__(self):
        self._history = []

    def push(self, command: Command):
        self._history.append(command)

    def undo(self):
        print("\n--- Deshaciendo última acción ---")
        if self._history:
            last_command = self._history.pop()
            last_command.undo()
        else:
            print("Nada que deshacer.")


# --- SIMULACIÓN DE EJECUCIÓN (Refactorizada) ---
if __name__ == "__main__":
    editor = TextEditor()
    historial = CommandHistory()

    # Configuramos los comandos conectándolos al editor
    cmd_copy = CopyCommand(editor)
    cmd_paste = PasteCommand(editor)

    # Inyectamos los comandos en los botones (Invocadores)
    btn_copy = Button("Copiar", cmd_copy)
    btn_paste = Button("Pegar", cmd_paste)

    # Usuario interactúa con la UI
    print(f"Estado Inicial: {editor.text}")
    
    c1 = btn_copy.click()
    historial.push(c1)
    
    c2 = btn_paste.click()
    historial.push(c2)

    # ¡LA MAGIA DEL PATRÓN! Podemos deshacer las acciones en orden inverso
    historial.undo() # Deshace el pegar
    historial.undo() # Deshace el copiar

    # --- ANÁLISIS ARQUITECTÓNICO ---
    # 1. Desacoplamiento total: El botón no sabe cómo funciona el editor.
    # 2. Reutilización: Podemos asignar el mismo 'CopyCommand' a un atajo de teclado (Ctrl+C).
    # 3. Superpoderes: Logramos un sistema "Deshacer" (Undo) de forma limpia porque
    #    cada comando recuerda el estado exacto antes de ejecutarse.
