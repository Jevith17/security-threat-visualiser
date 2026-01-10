import requests


def ip_to_geo(ip: str):
    
    url = f"http://ip-api.com/json/{ip}"
    resp = requests.get(url, timeout=5)
    data = resp.json()

    if data.get("status") != "success":
        return None

    return {
        "lat": data.get("lat"),
        "lon": data.get("lon"),
        "country": data.get("countryCode"),
    }
