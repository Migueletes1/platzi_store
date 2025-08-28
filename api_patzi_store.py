import requests
import json

base_url = "https://api.escuelajs.co/api/v1/"


def get_all_products():
    """Consulta y muestra todos los productos."""
    try:
        response = requests.get(f"{base_url}products/")
        response.raise_for_status()  # Lanza una excepción para errores HTTP
        products = response.json()
        print("\n--- LISTA DE PRODUCTOS ---")
        if not products:
            print("No hay productos disponibles.")
        else:
            for product in products:
                print(
                    f"ID: {product.get('id')}, Título: {product.get('title')}, Precio: ${product.get('price')}"
                )
        print("--------------------------\n")
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener los productos: {e}")


def get_specific_product():
    """Consulta un producto específico por ID."""
    product_id = input("Ingresa el ID del producto que quieres consultar: ")
    url = f"{base_url}products/{product_id}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            product = response.json()
            print("\n--- PRODUCTO ENCONTRADO ---")
            print(json.dumps(product, indent=4))
            print("----------------------------\n")
        elif response.status_code in [400, 404]:
            print(f"❌ El producto con ID {product_id} no existe en la tienda.")
        else:
            print(f"⚠️ Error inesperado: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {e}")


def create_product():
    """Crea un nuevo producto con datos ingresados por el usuario."""
    try:
        print("\n--- CREAR NUEVO PRODUCTO ---")
        title = input("Título del producto: ")
        price = int(input("Precio: "))
        description = input("Descripción: ")
        category_id = int(input("ID de la categoría: "))
        images = input("URL de la imagen (o déjalo en blanco): ")
        if not images:
            images = "https://via.placeholder.com/150"

        new_product = {
            "title": title,
            "price": price,
            "description": description,
            "categoryId": category_id,
            "images": [images] if images else [],
        }

        response = requests.post(f"{base_url}products/", json=new_product)
        response.raise_for_status()
        created_product = response.json()
        print("\n--- PRODUCTO CREADO EXITOSAMENTE ---")
        print(json.dumps(created_product, indent=4))
        print("------------------------------------\n")
    except requests.exceptions.RequestException as e:
        print(f"Error al crear el producto: {e}")
    except ValueError:
        print(
            "Entrada inválida. Asegúrate de ingresar números para el precio y la categoría."
        )


def update_product():
    """Actualiza un producto existente por ID."""
    try:
        product_id = input("Ingresa el ID del producto que quieres actualizar: ")
        print("\n--- ACTUALIZAR PRODUCTO ---")
        title = input("Nuevo título (o déjalo en blanco): ")
        price_input = input("Nuevo precio (o déjalo en blanco): ")
        description = input("Nueva descripción (o déjalo en blanco): ")

        product_updated = {}
        if title:
            product_updated["title"] = title
        if price_input:
            product_updated["price"] = int(price_input)
        if description:
            product_updated["description"] = description

        if not product_updated:
            print("No se ingresaron datos para actualizar.")
            return

        response = requests.put(
            f"{base_url}products/{product_id}", json=product_updated
        )
        response.raise_for_status()
        updated_data = response.json()
        print("\n--- PRODUCTO ACTUALIZADO EXITOSAMENTE ---")
        print(json.dumps(updated_data, indent=4))
        print("------------------------------------------\n")
    except requests.exceptions.RequestException as e:
        print(f"Error al actualizar el producto: {e}")
    except ValueError:
        print("Entrada inválida. Asegúrate de ingresar un número para el precio.")


def delete_product():
    """Elimina un producto por ID."""
    try:
        product_id = input("Ingresa el ID del producto que quieres eliminar: ")
        response = requests.delete(f"{base_url}products/{product_id}")
        response.raise_for_status()
        print(f"\n--- PRODUCTO CON ID {product_id} ELIMINADO EXITOSAMENTE ---")
        print("Respuesta:", response.json())
        print("-----------------------------------------------------------\n")
    except requests.exceptions.RequestException as e:
        print(f"Error al eliminar el producto: {e}")


def main_menu():
    """Muestra el menú principal y maneja la selección del usuario."""
    while True:
        print("=" * 30)
        print("   API PLATZI FAKE STORE - CRUD")
        print("=" * 30)
        print("1. GET - Consultar todos los productos")
        print("2. GET - Consultar producto específico")
        print("3. POST - Crear nuevo producto")
        print("4. PUT - Actualizar producto existente")
        print("5. DELETE - Eliminar producto")
        print("6. Salir")
        print("=" * 30)

        choice = input("Selecciona una opción (1-6): ")

        if choice == "1":
            get_all_products()
        elif choice == "2":
            get_specific_product()
        elif choice == "3":
            create_product()
        elif choice == "4":
            update_product()
        elif choice == "5":
            delete_product()
        elif choice == "6":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción inválida. Por favor, selecciona un número entre 1 y 6.")


if __name__ == "__main__":
    main_menu()
