# --- PASO 1: El Iterador Concreto ---
class BookIterator:
    """
    Este objeto es el único que conoce el secreto de cómo navegar
    por la estructura de diccionario anidado.
    """
    def __init__(self, books_by_genre):
        # Guardamos la estructura
        self._books_by_genre = books_by_genre
        # Sacamos los géneros como una lista para poder indexarlos
        self._genres = list(books_by_genre.keys())
        
        # Estado interno de la navegación
        self._genre_index = 0
        self._book_index = 0

    def __next__(self):
        """
        Método mágico de Python que devuelve el siguiente elemento.
        Si no hay más, lanza StopIteration.
        """
        # Si ya no quedan géneros por recorrer
        if self._genre_index >= len(self._genres):
            raise StopIteration

        current_genre = self._genres[self._genre_index]
        books_in_genre = self._books_by_genre[current_genre]

        # Si ya terminamos con los libros del género actual
        if self._book_index >= len(books_in_genre):
            # Saltamos al siguiente género
            self._genre_index += 1
            # Reseteamos el contador de libros
            self._book_index = 0
            # Llamada recursiva para procesar el siguiente género
            return self.__next__()

        # Obtenemos el libro y avanzamos el contador
        book = books_in_genre[self._book_index]
        self._book_index += 1
        return f"{book} ({current_genre})"

    def __iter__(self):
        # Por convención, un iterador debe poder devolverse a sí mismo
        return self


# --- PASO 2: La Colección Concreta ---
class BookCollection:
    """
    Representa la colección de datos. No enseña su diccionario al mundo,
    solo entrega un iterador para que caminen sobre él.
    """
    def __init__(self):
        self._books_by_genre = {
            "Fantasía": ["El Señor de los Anillos", "Harry Potter"],
            "Ciencia Ficción": ["Dune", "Fundación"],
            "Terror": ["It", "Drácula"]
        }

    def __iter__(self):
        """
        Método mágico que le dice a Python: 
        'Si alguien hace un bucle for sobre mí, dale este iterador'.
        """
        return BookIterator(self._books_by_genre)


# --- SIMULACIÓN DE EJECUCIÓN (Refactorizada) ---
if __name__ == "__main__":
    biblioteca = BookCollection()

    print("--- MOSTRANDO TODOS LOS LIBROS (CON PATRÓN ITERATOR) ---")
    
    # ¡MAGIA!: El cliente ya no ve el diccionario ni hace dobles bucles.
    # El código es limpio, legible y agnóstico a la estructura.
    for book in biblioteca:
        print(f"- {book}")

    # --- ANÁLISIS ARQUITECTÓNICO ---
    # 1. Encapsulamiento: Si mañana cambiamos el diccionario por una lista simple,
    #    solo hay que modificar BookIterator. El bucle for del cliente NO cambia.
    # 2. Responsabilidad Única: BookCollection guarda datos, BookIterator navega.
    # 3. Interfaz Uniforme: El cliente usa la misma sintaxis para cualquier colección.
    
    print("\nÉXITO: La complejidad del recorrido quedó oculta tras el Iterador.")
