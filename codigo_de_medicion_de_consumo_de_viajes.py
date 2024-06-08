import requests

# Función para geocodificación
def geocode(location, api_key):
    url = f"https://graphhopper.com/api/1/geocode?q={location}&limit=1&key={api_key}"
    response = requests.get(url)
    data = response.json()
    if data['hits']:
        lat = data['hits'][0]['point']['lat']
        lon = data['hits'][0]['point']['lng']
        return lat, lon
    else:
        return None

# Función para calcular la ruta
def get_route(start, end, vehicle, api_key):
    url = f"https://graphhopper.com/api/1/route?key={api_key}&vehicle={vehicle}&point={start[0]},{start[1]}&point={end[0]},{end[1]}"
    response = requests.get(url)
    data = response.json()
    if 'paths' in data:
        distance = data['paths'][0]['distance'] / 1000  # Convertir metros a kilómetros
        time = data['paths'][0]['time'] / 1000  # Convertir milisegundos a segundos
        return distance, time, data['paths'][0]['instructions']
    else:
        return None, None, None

# Función para calcular el combustible requerido
def calculate_fuel(distance, fuel_efficiency):
    return distance / fuel_efficiency

# Función principal del programa
def main():
    api_key = "1b0b4563-7931-4097-bb51-e6771a4023bd"  # Reemplaza con tu propia API key de Graphhopper
    fuel_efficiency = 15  # Consumo de combustible en km por litro

    while True:
        print("+++++++++++++++++++++++++++++++++++++++++++++")
        print("sistema de calculo de distancia y consumo entre ciudades")
        print("+++++++++++++++++++++++++++++++++++++++++++++")
        print("ingrese una ciudad de origen y una de destino")
        print("para salir del programa precione la letra q mas enter 2 veces q+ tecla enter ")
        print("+++++++++++++++++++++++++++++++++++++++++++++")


        start_city = input("Ciudad de Origen: ").strip()
        end_city = input("Ciudad de Destino: ").strip()

        if start_city.lower() == 'q' or end_city.lower() == 'q':
            print("Saliendo del programa.")
            break

        start_coords = geocode(start_city, api_key)
        end_coords = geocode(end_city, api_key)

        if start_coords and end_coords:
            vehicle = "car"  # Solo usamos autos
            distance, duration, instructions = get_route(start_coords, end_coords, vehicle, api_key)
            if distance and duration:
                fuel_needed = calculate_fuel(distance, fuel_efficiency)
                hours, rem = divmod(duration, 3600)
                minutes, seconds = divmod(rem, 60)

                print("=================================================")
                print(f"Direcciones desde {start_city} hasta {end_city} en coche")
                print("=================================================")
                print(f"Distancia recorrida: {distance:.2f} km")
                print(f"Duración del viaje: {int(hours):02} horas, {int(minutes):02} minutos, {int(seconds):02} segundos")
                print(f"Combustible requerido: {fuel_needed:.2f} litros")
                print("=================================================")
                
                for instruction in instructions:
                    distance_segment = instruction['distance'] / 1000  # Convertir metros a kilómetros
                    print(f"{instruction['text']} ( {distance_segment:.2f} km )")
                
                print("=============================================")
            else:
                print("Error al calcular la ruta. Por favor, intente nuevamente.")
        else:
            print("Error al geocodificar una de las ubicaciones. Por favor, intente nuevamente.")

if __name__ == "__main__":
    main()