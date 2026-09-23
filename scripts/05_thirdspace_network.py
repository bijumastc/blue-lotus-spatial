"""
05_thirdspace_network.py
Build a simple network graph that visualises the poem's
Firstspace / Secondspace / Thirdspace relations
(Soja) and the diasporic graft.
"""

import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_PNG = ROOT / "output" / "thirdspace_network.png"

def main():
    G = nx.Graph()

    # Nodes with attributes
    nodes = {
        "Pamba River\n(Kerala)": {"space": "First/Second", "type": "ancestral"},
        "Grandmother’s\ngarden": {"space": "Second", "type": "ancestral"},
        "Writing hand\n(split wrist)": {"space": "rupture", "type": "body"},
        "Lotus graft\n(Thirdspace)": {"space": "Thirdspace", "type": "hybrid"},
        "Mountain\n(resurrected)": {"space": "Thirdspace", "type": "symbolic"},
        "Gammadion\n(scattering)": {"space": "diaspora", "type": "sign"},
        "Lower Manhattan\n(towers blazed)": {"space": "First", "type": "present"},
        "Nervous empire": {"space": "Second (conceived)", "type": "present"},
        "Bald rock /\nriverbank": {"space": "lived home", "type": "present"},
        "Speaking stones\n(sibilant scattering)": {"space": "Thirdspace", "type": "voice"},
        "New speech\n(new tribe)": {"space": "Third Space of\nenunciation", "type": "language"},
    }

    for n, attrs in nodes.items():
        G.add_node(n, **attrs)

    # Edges that enact the poem’s logic
    edges = [
        ("Pamba River\n(Kerala)", "Writing hand\n(split wrist)", "dream of tribe"),
        ("Writing hand\n(split wrist)", "Lotus graft\n(Thirdspace)", "graft / kiss the stump"),
        ("Lotus graft\n(Thirdspace)", "Mountain\n(resurrected)", "petals whirl like mountain"),
        ("Mountain\n(resurrected)", "Gammadion\n(scattering)", "excavation"),
        ("Gammadion\n(scattering)", "Speaking stones\n(sibilant scattering)", "diaspora as utterance"),
        ("Lower Manhattan\n(towers blazed)", "Nervous empire", "conceived space"),
        ("Nervous empire", "Bald rock /\nriverbank", "homing desire"),
        ("Bald rock /\nriverbank", "Speaking stones\n(sibilant scattering)", "stones have tongues"),
        ("Lotus graft\n(Thirdspace)", "New speech\n(new tribe)", "creative organ"),
        ("New speech\n(new tribe)", "Speaking stones\n(sibilant scattering)", "hybrid lineage"),
        ("Grandmother’s\ngarden", "Lotus graft\n(Thirdspace)", "ancestral plant"),
    ]

    G.add_edges_from([(u, v) for u, v, _ in edges])

    # Layout
    pos = nx.spring_layout(G, seed=42, k=1.8)

    # Colour nodes by type
    color_map = {
        "ancestral": "#2ca02c",
        "present": "#d62728",
        "hybrid": "#9467bd",
        "symbolic": "#8c564b",
        "body": "#e377c2",
        "sign": "#7f7f7f",
        "voice": "#17becf",
        "language": "#bcbd22",
    }
    node_colors = [color_map.get(G.nodes[n]["type"], "#1f77b4") for n in G.nodes]

    plt.figure(figsize=(14, 10))
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=2200, alpha=0.9)
    nx.draw_networkx_edges(G, pos, width=1.8, alpha=0.6, edge_color="#555555")
    nx.draw_networkx_labels(G, pos, font_size=8, font_family="sans-serif")

    # Edge labels (selected)
    edge_labels = {(u, v): label for u, v, label in edges}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=6, label_pos=0.4)

    plt.title("Blue Lotus – Thirdspace Network\n(Soja / Bhabha / Brah)", fontsize=14)
    plt.axis("off")
    plt.tight_layout()

    OUT_PNG.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(OUT_PNG, dpi=300, bbox_inches="tight")
    print(f"Network graph saved → {OUT_PNG}")

if __name__ == "__main__":
    main()
