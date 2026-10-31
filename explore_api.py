import requests

BASE_URL = "https://velib-metropole-opendata.smovengo.cloud/opendata/Velib_Metropole"

response = requests.get(f"{BASE_URL}/station_status.json", timeout=30)
response.raise_for_status()  # plante si l'API renvoie une erreur (404, 500…)
data = response.json()

stations = data["data"]["stations"]
print(f"Nombre de stations : {len(stations)}")
print("Exemple :", stations[0])


print("Nombre total de vélos disponibles")
total_bikes = sum(station["num_bikes_available"] for station in stations)
print(total_bikes)

print("Nombre de stations vides")
empty_stations = sum(1 for station in stations if station["num_bikes_available"] == 0)
print(empty_stations)

electric_bikes = 0
for station in stations:
    for bike_type in station["num_bikes_available_types"]:
        if "ebike" in bike_type:           
            electric_bikes += bike_type["ebike"]       
print("Nombre total de vélos électriques")
print(electric_bikes)


print("Nombre de vélos mécaniques")
mechanical_bikes = 0
for station in stations:
    for bike_type in station["num_bikes_available_types"]:
        if "mechanical" in bike_type:
            mechanical_bikes += bike_type["mechanical"]
print(mechanical_bikes)

print("Vérification : mécaniques + électriques")
somme = mechanical_bikes + electric_bikes
print(somme)

if somme == total_bikes:
    print("✅ Cohérent : la somme correspond au total")
else:
    print(f"❌ Écart de {total_bikes - somme} vélos")