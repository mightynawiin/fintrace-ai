# backend/app/cycle_detector.py

import networkx as nx

def detect_cycles(G):
    raw_cycles = list(nx.simple_cycles(G))

    # Filter cycles length 3–5 only
    filtered_cycles = [
        cycle for cycle in raw_cycles
        if 3 <= len(cycle) <= 5
    ]

    rings = []
    ring_counter = 1

    for cycle in filtered_cycles:
        ring_id = f"RING_{ring_counter:03d}"

        rings.append({
            "ring_id": ring_id,
            "pattern_type": f"cycle_length_{len(cycle)}",
            "member_accounts": cycle
        })

        ring_counter += 1

    return rings
