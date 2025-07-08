import requests
import json

# APIs
directions_api = "https://api.openrouteservice.org/v2/directions/driving-car"
geocode_api = "https://api.openrouteservice.org/geocode/search?"

key = "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6IjE2OThjNDUzMDRkMzRkMGJiNDZkOTJkNGMxMzczYjE5IiwiaCI6Im11cm11cjY0In0="

def geocode_address(address):
    url = f"{geocode_api}api_key={key}&text={address}"
    response = requests.get(url)
    if response.status_code == 200:
        json_data = response.json()
        if json_data["features"]:
            coords = json_data["features"][0]["geometry"]["coordinates"]
            print(f"Geocoded coordinates for '{address}': {coords}")
            return coords
        else:
            print(f"Error: No results found for address '{address}'")
    else:
        print(f"Error: {response.status_code} - {response.text}")
    return None

while True:
    orig = input("Starting Location (or 'q' to quit): ")
    if orig.lower() in ["q", "quit"]:
        break
    dest = input("Destination (or 'q' to quit): ")
    if dest.lower() in ["q", "quit"]:
        break

    # Geocode
    orig_coords = geocode_address(orig)
    dest_coords = geocode_address(dest)

    if not orig_coords or not dest_coords:
        print("Unable to geocode one or both addresses. Please try again.\n")
        continue

    # Crear body para POST
    body = {
        "coordinates": [orig_coords, dest_coords]
    }

    headers = {
        "Authorization": key,
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(directions_api, headers=headers, json=body)
        json_data = response.json()

        if response.status_code == 200:
            if 'routes' in json_data and json_data['routes']:
                route = json_data['routes'][0]
                segment = route['segments'][0]

                print("\nAPI Status: Successful route call.\n")
                print("=============================================")
                print(f"Directions from {orig} to {dest}")
                print(f"Trip Duration: {segment['duration']} seconds")
                print(f"Distance: {segment['distance']} meters")
                print("=============================================")

                for step in segment['steps']:
                    print(f"{step['instruction']} ({step['distance']} meters)")
                print("=============================================\n")
            else:
                print("No routes found.")
        else:
            print(f"API Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"An error occurred: {e}")
