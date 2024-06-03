import requests

def obtener_coordenadas(ciudad):
    endpoint = "https://graphhopper.com/api/1/geocode"
    params = {
        "q": ciudad,
        "key": "81afb162-1b7a-4011-bbe0-73c214a2f746"
    }
    response = requests.get(endpoint, params=params)
    data = response.json()
    return data["hits"][0]["point"]

def obtener_ruta(ciudad_origen, ciudad_destino):
    try:
        origen = obtener_coordenadas(ciudad_origen)
        destino = obtener_coordenadas(ciudad_destino)
        endpoint = "https://graphhopper.com/api/1/route"
        params = {
            "point": [f"{origen['lat']},{origen['lng']}", f"{destino['lat']},{destino['lng']}"],
            "vehicle": "car",
            "locale": "es",
            "key": "81afb162-1b7a-4011-bbe0-73c214a2f746"
        }
        response = requests.get(endpoint, params=params)
        data = response.json()
        
        if "paths" in data and len(data["paths"]) > 0:
            return data["paths"][0]
        else:
            print("No se encontró una ruta válida.")
            return None
    except Exception as e:
        print(f"Error al obtener la ruta: {e}")
        return None

def calcular_combustible(distancia_km):
    consumo_litros = distancia_km * 8 / 100
    return round(consumo_litros, 2)

def convertir_tiempo(segundos):
    horas = segundos // 3600
    minutos = (segundos % 3600) // 60
    segundos = segundos % 60
    return horas, minutos, segundos

def imprimir_resultados(ciudad_origen, ciudad_destino, distancia, duracion, combustible, ruta):
    horas, minutos, segundos = convertir_tiempo(duracion)
    print(f"Viaje desde {ciudad_origen} a {ciudad_destino}:")
    print(f"Distancia: {distancia:.2f} km")
    print(f"Duración: {horas} horas, {minutos} minutos, {segundos} segundos")
    print(f"Combustible requerido: {combustible:.2f} litros")
    print("Narrativa del viaje:")
    for step in ruta["instructions"]:
        print(step["text"])

def main():
    while True:
        print("\nMenú:")
        print("1. Medir distancia entre Santiago y Puerto Varas")
        print("2. Calcular ruta entre dos ciudades")
        print("q. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            ruta = obtener_ruta("Santiago", "Puerto Varas")
            distancia = ruta["distance"] / 1000
            duracion = ruta["time"] / 1000
            combustible = calcular_combustible(distancia)
            imprimir_resultados("Santiago", "Puerto Varas", distancia, duracion, combustible, ruta)
        elif opcion == "2":
            origen = input("Ingrese la ciudad de origen: ")
            destino = input("Ingrese la ciudad de destino: ")
            ruta = obtener_ruta(origen, destino)
            distancia = ruta["distance"] / 1000
            duracion = ruta["time"] / 1000
            combustible = calcular_combustible(distancia)
            imprimir_resultados(origen, destino, distancia, duracion, combustible, ruta)
        elif opcion.lower() == "q":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Por favor, seleccione una opción válida.")

if __name__ == "__main__":
    main()