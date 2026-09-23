"""
02_geocode_places.py
Geocode the curated places from "Blue Lotus" using Nominatim (OpenStreetMap).
Produces a CSV ready for mapping.
"""

from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import pandas as pd
from pathlib import Path
import time

ROOT = Path(__file__).resolve().parent.parent
OUT_PATH = ROOT / "output" / "places_geocoded.csv"

# Curated place list with reliable queries
PLACE_DATA = [
    {
        "name": "Pamba River",
        "query": "Pamba River, Kerala, India",
        "section": "I",
        "type": "ancestral",
        "notes": "Sacred river in Kerala; ancestral homeland"
    },
    {
        "name": "Grandmother’s garden / house",
        "query": "Pathanamthitta, Kerala, India",  # approximate region near Pamba
        "section": "I / IV",
        "type": "ancestral",
        "notes": "Implied ancestral domestic space"
    },
    {
        "name": "Island where towers blazed",
        "query": "Lower Manhattan, New York, USA",
        "section": "IV",
        "type": "present",
        "notes": "Post-9/11 site; World Trade Center vicinity"
    },
    {
        "name": "Riverbank (ash trees)",
        "query": "Hudson River, Manhattan, New York, USA",
        "section": "IV",
        "type": "present",
        "notes": "Site of the 'long way home' / bald rock"
    },
    {
        "name": "New York City (nervous empire)",
        "query": "New York City, New York, USA",
        "section": "IV",
        "type": "present",
        "notes": "Conceived imperial space"
    },
    {
        "name": "Kerala (ancestral region)",
        "query": "Kerala, India",
        "section": "I–IV",
        "type": "ancestral",
        "notes": "Broader homeland reference"
    },
]

def main():
    geolocator = Nominatim(user_agent="blue_lotus_spatial_analysis_v1")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1.5)

    rows = []
    for item in PLACE_DATA:
        print(f"Geocoding: {item['name']} ...")
        location = geocode(item["query"])
        if location:
            rows.append({
                "name": item["name"],
                "query": item["query"],
                "section": item["section"],
                "type": item["type"],
                "notes": item["notes"],
                "latitude": location.latitude,
                "longitude": location.longitude,
                "address": location.address,
                "success": True
            })
            print(f"  → {location.latitude:.5f}, {location.longitude:.5f}")
        else:
            rows.append({
                "name": item["name"],
                "query": item["query"],
                "section": item["section"],
                "type": item["type"],
                "notes": item["notes"],
                "latitude": None,
                "longitude": None,
                "address": None,
                "success": False
            })
            print("  → FAILED")
        time.sleep(0.5)

    df = pd.DataFrame(rows)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_PATH, index=False)
    print(f"\nSaved → {OUT_PATH}")
    print(df[["name", "latitude", "longitude", "success"]].to_string())

if __name__ == "__main__":
    main()
