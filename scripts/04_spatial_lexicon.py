"""
04_spatial_lexicon.py
Quantify spatial, rupture, reconstitution, and home-related vocabulary
across the four sections of "Blue Lotus".
Produces a bar chart and CSV summary.
"""

import re
from collections import Counter
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parent.parent
POEM_PATH = ROOT / "data" / "poem.txt"
OUT_CSV = ROOT / "output" / "lexicon_by_section.csv"
OUT_PNG = ROOT / "output" / "lexicon_by_section.png"

# Lexicon categories aligned with the qualitative reading
LEXICON = {
    "movement": [
        "stroll", "lift", "climb", "climbed", "cleared", "fetch", "fetches",
        "float", "reach", "scattering", "gathering", "rise", "resurrects"
    ],
    "rupture": [
        "split", "stump", "cracked", "broken", "blazed", "abolished",
        "mist", "fitful", "burns", "desolation", "ghost"
    ],
    "reconstitution": [
        "set", "kiss", "resurrects", "learning", "incantation",
        "tongues", "purify", "new", "comfort", "home"
    ],
    "home_belonging": [
        "garden", "house", "home", "tribe", "riverbank", "grandmother",
        "pamba", "mountain", "rock", "stones"
    ],
    "violence_empire": [
        "empire", "arms", "blood", "bones", "flint", "nervous",
        "small arms", "ground rules"
    ]
}

def split_sections(text):
    """Split the poem into the four numbered movements."""
    # Simple and robust split on section markers
    parts = re.split(r'\n\s*(I{1,3}|IV)\s*\n', text)
    sections = {}
    # parts[0] is title + preamble, then pairs of (marker, content)
    i = 1
    while i < len(parts) - 1:
        marker = parts[i].strip()
        content = parts[i + 1]
        sections[marker] = content
        i += 2
    return sections

def count_lexicon(text, lexicon):
    tokens = re.findall(r'\b\w+\b', text.lower())
    counts = {}
    for category, words in lexicon.items():
        counts[category] = sum(1 for t in tokens if t in words)
    return counts

def main():
    text = POEM_PATH.read_text(encoding="utf-8")
    sections = split_sections(text)

    if not sections:
        print("Could not split sections. Check poem formatting.")
        return

    print("Sections found:", list(sections.keys()))

    results = {}
    for sec, content in sections.items():
        results[sec] = count_lexicon(content, LEXICON)

    df = pd.DataFrame(results).T
    df.index.name = "section"
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_CSV)
    print("\nLexicon counts by section:")
    print(df)

    # Plot
    plt.figure(figsize=(10, 6))
    df.plot(kind="bar", ax=plt.gca(), width=0.8)
    plt.title("Spatial & Thematic Lexicon by Section – Blue Lotus")
    plt.ylabel("Word count")
    plt.xlabel("Section")
    plt.xticks(rotation=0)
    plt.legend(title="Category", bbox_to_anchor=(1.02, 1), loc="upper left")
    plt.tight_layout()
    plt.savefig(OUT_PNG, dpi=300, bbox_inches="tight")
    print(f"\nChart saved → {OUT_PNG}")
    print(f"CSV saved  → {OUT_CSV}")

if __name__ == "__main__":
    main()
