"""
03_create_map.py
Create an interactive Folium map of the places in "Blue Lotus"
showing ancestral vs present space and the diaspora trajectory.
"""

import pandas as pd
import folium
from folium import plugins
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GEO_CSV = ROOT / "output" / "places_geocoded.csv"
MAP_PATH = ROOT / "output" / "blue_lotus_map.html"

def main():
    df = pd.read_csv(GEO_CSV)
    df = df.dropna(subset=["latitude", "longitude"])

    # Centre the map between Kerala and New York
    m = folium.Map(
        location=[25, 20],
        zoom_start=2,
        tiles="CartoDB positron"
    )

    # Colour scheme matching the theoretical framework
    colors = {
        "ancestral": "#2ca02c",   # green – lived / homeland
        "present": "#d62728",     # red – nervous empire
        "symbolic": "#9467bd"     # purple – Thirdspace
    }

    # Add markers
    for _, row in df.iterrows():
        color = colors.get(row["type"], "#1f77b4")
        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=10,
            popup=folium.Popup(
                f"<b>{row['name']}</b><br>"
                f"Section: {row['section']}<br>"
                f"Type: {row['type']}<br>"
                f"{row['notes']}",
                max_width=300
            ),
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.75,
            weight=2
        ).add_to(m)

    # Diaspora trajectory: Kerala → New York
    kerala = df[df["name"].str.contains("Kerala|Pamba", case=False)]
    manhattan = df[df["name"].str.contains("Manhattan|New York City", case=False)]

    if not kerala.empty and not manhattan.empty:
        start = [kerala.iloc[0]["latitude"], kerala.iloc[0]["longitude"]]
        end = [manhattan.iloc[0]["latitude"], manhattan.iloc[0]["longitude"]]
        folium.PolyLine(
            locations=[start, end],
            color="#ff7f0e",
            weight=3,
            dash_array="8, 12",
            popup="Diaspora trajectory (ancestral → present)"
        ).add_to(m)

        # Midpoint marker for Thirdspace
        mid_lat = (start[0] + end[0]) / 2
        mid_lon = (start[1] + end[1]) / 2
        folium.Marker(
            location=[mid_lat, mid_lon],
            popup="Thirdspace / grafted lotus<br>(Soja / Bhabha)",
            icon=folium.Icon(color="purple", icon="info-sign")
        ).add_to(m)

    # Legend
    legend_html = """
    <div style="position: fixed; bottom: 30px; left: 30px; z-index: 1000;
                background: white; padding: 12px; border: 2px solid grey;
                border-radius: 6px; font-size: 14px;">
      <b>Blue Lotus – Spatial Layers</b><br>
      <i style="color:#2ca02c;">●</i> Ancestral (Kerala / Pamba)<br>
      <i style="color:#d62728;">●</i> Present (New York / nervous empire)<br>
      <i style="color:#9467bd;">●</i> Symbolic / Thirdspace<br>
      <span style="color:#ff7f0e;">— —</span> Diaspora trajectory
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))

    MAP_PATH.parent.mkdir(parents=True, exist_ok=True)
    m.save(str(MAP_PATH))
    print(f"Interactive map saved → {MAP_PATH}")
    print("Open the HTML file in any browser.")

if __name__ == "__main__":
    main()
