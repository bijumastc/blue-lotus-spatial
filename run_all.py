"""
run_all.py
Execute the full Blue Lotus spatial pipeline in sequence.
"""

import subprocess
import sys
from pathlib import Path

SCRIPTS = [
    "scripts/01_extract_places.py",
    "scripts/02_geocode_places.py",
    "scripts/03_create_map.py",
    "scripts/04_spatial_lexicon.py",
    "scripts/05_thirdspace_network.py",
]

def main():
    root = Path(__file__).resolve().parent
    print("=" * 60)
    print("Blue Lotus – Spatial Computational Pipeline")
    print("=" * 60)

    for script in SCRIPTS:
        path = root / script
        print(f"\n>>> Running {script} ...")
        result = subprocess.run([sys.executable, str(path)], cwd=root)
        if result.returncode != 0:
            print(f"ERROR in {script}. Stopping.")
            sys.exit(1)
        print(f"✓ {script} finished")

    print("\n" + "=" * 60)
    print("All pipelines completed successfully.")
    print("Results are in the output/ folder.")
    print("Open output/blue_lotus_map.html in a browser.")
    print("=" * 60)

if __name__ == "__main__":
    main()
