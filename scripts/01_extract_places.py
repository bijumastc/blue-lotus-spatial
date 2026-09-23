"""
01_extract_places.py
Extract named places and spatial referents from Meena Alexander's "Blue Lotus"
using spaCy NER (optional) + curated poetic terms.
"""

import re
import pandas as pd
from pathlib import Path

# Paths
ROOT = Path(__file__).resolve().parent.parent
POEM_PATH = ROOT / "data" / "poem.txt"
OUT_PATH = ROOT / "output" / "places_extracted.csv"

def load_poem():
    return POEM_PATH.read_text(encoding="utf-8")

def extract_with_spacy(text):
    """Try to load spaCy. Falls back gracefully if model is missing."""
    try:
        import spacy
        # Prefer the small model – much more reliable on Windows / Python 3.13
        try:
            nlp = spacy.load("en_core_web_sm")
        except OSError:
            nlp = spacy.load("en_core_web_trf")
        doc = nlp(text)
        places = []
        for ent in doc.ents:
            if ent.label_ in ("GPE", "LOC", "FAC"):
                places.append({
                    "text": ent.text,
                    "label": ent.label_,
                    "start": ent.start_char,
                    "end": ent.end_char,
                    "source": "spacy"
                })
        return places
    except Exception as e:
        print(f"spaCy not available or model missing → skipping NER ({e})")
        return []

def extract_curated(text):
    """Manually curated terms that spaCy often misses in poetic language."""
    patterns = [
        (r"Pamba River", "Pamba River", "ancestral"),
        (r"grandmother[’']s garden", "Grandmother’s garden", "ancestral"),
        (r"grandmother[’']s house", "Grandmother’s house", "ancestral"),
        (r"island where towers blazed", "Island where towers blazed (Lower Manhattan)", "present"),
        (r"ash trees on the riverbank", "Ash trees / riverbank (NY)", "present"),
        (r"riverbank", "Riverbank", "present"),
        (r"\bmountain\b", "Mountain (symbolic)", "symbolic"),
        (r"stubble fields", "Stubble fields", "ancestral"),
        (r"red soil", "Red soil (Pamba)", "ancestral"),
        (r"rock houses", "Rock houses", "symbolic"),
        (r"cliff[’']s edge", "Cliff’s edge", "symbolic"),
        (r"bald rock", "Bald rock", "present"),
        (r"nervous empire", "Nervous empire (NY)", "present"),
    ]
    curated = []
    for pattern, name, ptype in patterns:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            curated.append({
                "text": match.group(0),
                "canonical_name": name,
                "type": ptype,
                "start": match.start(),
                "end": match.end(),
                "source": "curated"
            })
    return curated

def main():
    text = load_poem()
    print("Poem loaded. Length:", len(text), "characters")

    # spaCy extraction (optional)
    spacy_places = extract_with_spacy(text)
    print(f"spaCy found {len(spacy_places)} entities")

    curated = extract_curated(text)
    print(f"Curated extraction found {len(curated)} spatial referents")

    # Combine and save
    rows = []
    for p in curated:
        rows.append({
            "text": p["text"],
            "canonical_name": p["canonical_name"],
            "type": p["type"],
            "source": p["source"],
            "start_char": p["start"],
            "end_char": p["end"]
        })
    for p in spacy_places:
        rows.append({
            "text": p["text"],
            "canonical_name": p["text"],
            "type": "spacy",
            "source": p["source"],
            "start_char": p["start"],
            "end_char": p["end"]
        })

    df = pd.DataFrame(rows)
    df = df.drop_duplicates(subset=["text", "start_char"])
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_PATH, index=False)
    print(f"\nSaved → {OUT_PATH}")
    print(df.to_string())

if __name__ == "__main__":
    main()