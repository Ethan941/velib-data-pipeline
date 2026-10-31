from datetime import datetime, timezone

import requests

BASE_URL = "https://velib-metropole-opendata.smovengo.cloud/opendata/Velib_Metropole"


def extract() -> list[dict]:
    """Récupère la liste des stations depuis l'API."""
    response = requests.get(f"{BASE_URL}/station_status.json", timeout=30)
    response.raise_for_status()
    return response.json()["data"]["stations"]


def transform(station: dict, snapshot_at: datetime) -> dict:
    """Transforme une station brute de l'API en une ligne pour raw.station_status."""
    # Piège 1 : la liste [{'mechanical': 11}, {'ebike': 2}] devient 2 nombres
    mechanical = 0
    ebike = 0
    for bike_type in station["num_bikes_available_types"]:
        if "mechanical" in bike_type:
            mechanical += bike_type["mechanical"]
        if "ebike" in bike_type:
            ebike += bike_type["ebike"]

    return {
        "station_id": station["station_id"],
        "snapshot_at": snapshot_at,
        "num_bikes_available": station["num_bikes_available"],
        "num_mechanical_available": mechanical,
        "num_ebike_available": ebike,
        "num_docks_available": station["num_docks_available"],
        # Piège 2 : 1/0 devient True/False
        "is_installed": bool(station["is_installed"]),
        "is_renting": bool(station["is_renting"]),
        "is_returning": bool(station["is_returning"]),
        # Piège 3 : le timestamp Unix devient une vraie date
        "last_reported": datetime.fromtimestamp(station["last_reported"], tz=timezone.utc),
    }
    # Piège 4 (champs en double comme numBikesAvailable) : réglé en ne les reprenant simplement pas


if __name__ == "__main__":
    snapshot_at = datetime.now(timezone.utc)
    stations = extract()
    print(f"{len(stations)} stations extraites")
    print("Avant :", stations[0])
    print("Après :", transform(stations[0], snapshot_at))