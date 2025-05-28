from enum import Enum
from nodes import Node, ProdRank, RevRank, ProbeSlot, Probe, ProbeType, Connection

def load_game_data():
    # In-game data for each node
    node_data = {
        "Primordia": [
            ("fn_site_101", "FN Site 101", ProdRank.C, RevRank.S, "S"),
            ("fn_site_102", "FN Site 102", ProdRank.C, RevRank.F, "B"),
            ("fn_site_103", "FN Site 103", ProdRank.C, RevRank.E, "A"),
            ("fn_site_104", "FN Site 104", ProdRank.C, RevRank.S, "B"),
            ("fn_site_105", "FN Site 105", ProdRank.A, RevRank.F, "B"),
            ("fn_site_106", "FN Site 106", ProdRank.B, RevRank.E, "B"),
            ("fn_site_107", "FN Site 107", ProdRank.A, RevRank.F, "B"),
            ("fn_site_108", "FN Site 108", ProdRank.C, RevRank.F, "B"),
            ("fn_site_109", "FN Site 109", ProdRank.C, RevRank.D, "B"),
            ("fn_site_110", "FN Site 110", ProdRank.C, RevRank.E, "B"),
            ("fn_site_111", "FN Site 111", ProdRank.C, RevRank.F, "B"),
            ("fn_site_112", "FN Site 112", ProdRank.A, RevRank.F, "A"),
            ("fn_site_113", "FN Site 113", ProdRank.C, RevRank.C, "B"),
            ("fn_site_114", "FN Site 114", ProdRank.C, RevRank.E, "B"),
            ("fn_site_115", "FN Site 115", ProdRank.C, RevRank.D, "B"),
            ("fn_site_116", "FN Site 116", ProdRank.A, RevRank.D, "B"),
            ("fn_site_117", "FN Site 117", ProdRank.A, RevRank.D, "A"),
            ("fn_site_118", "FN Site 118", ProdRank.C, RevRank.E, "B"),
            ("fn_site_119", "FN Site 119", ProdRank.C, RevRank.E, "B"),
            ("fn_site_120", "FN Site 120", ProdRank.B, RevRank.B, "B"),
            ("fn_site_121", "FN Site 121", ProdRank.A, RevRank.E, "B"),
        ],
        "Noctilum": [
            # Need to do Noctilum nodes (2xx)
        ],
        "Oblivia": [
            # Need to do Oblivia nodes (3xx)
        ],
        "Sylvalum": [
            # Need to do Sylvalum nodes (4xx)
        ],
        "Cauldros": [
            # Need to do Cauldros nodes (5xx)
        ]
    }

    # Creates a nodes dictionary
    nodes = {}
    for region, region_nodes_data in node_data.items():
        nodes[region] = {}
        for node_id, name, prod_rank, rev_rank, combat_rank in region_nodes_data:
            nodes[region][node_id] = Node(name, prod_rank, rev_rank, combat_rank)

    # Creates connections between nodes which are connected in game for adjacent bonuses
    connections = [
        # Need to do all the connections between nodes
    ]

    # Creates a probe slot for each node
    slots = {}
    for region, region_nodes in nodes.items():
        slots[region] = {}
        for node_id, node in region_nodes.items():
            slots[region][node_id] = ProbeSlot(node)

    # Creates all possible probes in the game
    probe_types_and_gens = {
        "basic": None,
        "mining": 10, 
        "research": 10, 
        "booster": 2, 
        "duplicator": None, 
        "storage": None, 
        "combat": None
    }

    # Basic, duplicator, storage, and combat nodes only have a single version each,
    # meaning they essentially have no generations that will be used for calculations

    probes = {}
    for probe_type, max_gen in probe_types_and_gens.items():
        probes[probe_type] = {}
        probe_name = f"{probe_type.capitalize()}"

        try:
            enum_type = getattr(ProbeType, probe_type.upper())
        except AttributeError:
            print(f"Warning: ProbeType.{probe_type.upper()} does not exist in the ProbeType enum!")
            continue

        if max_gen is None:
            # Use key 0 for probes with no generations
            probe_name_new = probe_name + " Probe"
            probes[probe_type] = {0: Probe(enum_type, None, probe_name_new)}
        else:
            for gen in range(1, max_gen + 1):
                probe_name_new = probe_name + f" G{gen} Probe"
                probes[probe_type][gen] = Probe(enum_type, gen, probe_name_new)
