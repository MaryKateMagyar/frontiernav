from enum import Enum
from nodes import Node, ProdRank, RevRank, ProbeSlot, Probe, ProbeType, Connection

def load_game_data():
    # In-game data for each node
    node_data = {
        "Primordia": [
            # id, name, prod_rank, rev_rank, combat_rank, sightseeing, prec_resources, [connected_node_ids]
            ("fn101", "FN Site 101", ProdRank.C, RevRank.S, "S", ["Stonelattice Cavern"], None, ["fn105"]),
            ("fn102", "FN Site 102", ProdRank.C, RevRank.F, "B", None, None, ["fn104"]),
            ("fn103", "FN Site 103", ProdRank.C, RevRank.E, "A", ["Wonderment Bluff"], None, ["fn105", "fn106", "fn222"]),
            ("fn104", "FN Site 104", ProdRank.C, RevRank.S, "B", ["Headwater Cliff"], None, ["fn102", "fn106"]),
            ("fn105", "FN Site 105", ProdRank.A, RevRank.F, "B", None, None, ["fn101", "fn103", "fn109"]),
            ("fn106", "FN Site 106", ProdRank.B, RevRank.E, "B", ["Turtle Nest"], ["Arc Sand Ore"], ["fn103", "fn104", "fn107"]),
            ("fn107", "FN Site 107", ProdRank.A, RevRank.F, "B", None, None, ["fn106", "fn110"]),
            ("fn108", "FN Site 108", ProdRank.C, RevRank.F, "B", None, ["Arc Sand Ore", "Aurorite", "Foucaultium"], ["fn109"]),
            ("fn109", "FN Site 109", ProdRank.C, RevRank.D, "B", None, ["Dawnstone", "Foucaultium", "Lionbone Bort"], ["fn105", "fn108"]),
            ("fn110", "FN Site 110", ProdRank.C, RevRank.E, "B", ["Talon Rock Prominence"], ["Arc Sand Ore", "Aurorite", "Dawnstone", "White Cometite"], ["fn107", "fn111", "fn112"]),
            ("fn111", "FN Site 111", ProdRank.C, RevRank.F, "B", None, ["Foucaultium"], ["fn110", "fn113"]),
            ("fn112", "FN Site 112", ProdRank.A, RevRank.F, "A", None, None, ["fn110", "fn114", "fn115"]),
            ("fn113", "FN Site 113", ProdRank.C, RevRank.C, "B", None, None, ["fn111", "fn409"]),
            ("fn114", "FN Site 114", ProdRank.C, RevRank.E, "B", None, None, ["fn112", "fn116"]),
            ("fn115", "FN Site 115", ProdRank.C, RevRank.D, "B", None, ["Arc Sand Ore", "Lionbone Bort", "White Cometite"], ["fn112"]),
            ("fn116", "FN Site 116", ProdRank.A, RevRank.D, "B", None, None, ["fn114", "fn117"]),
            ("fn117", "FN Site 117", ProdRank.A, RevRank.D, "A", ["Rock Cavern"], None, ["fn116", "fn118", "fn120"]),
            ("fn118", "FN Site 118", ProdRank.C, RevRank.E, "B", None, ["Aurorite", "Dawnstone", "White Cometite"], ["fn117", "fn121"]),
            ("fn119", "FN Site 119", ProdRank.C, RevRank.E, "B", None, None, ["fn120"]),
            ("fn120", "FN Site 120", ProdRank.B, RevRank.B, "B", None, None, ["fn117", "fn119"]),
            ("fn121", "FN Site 121", ProdRank.A, RevRank.E, "B", None, None, ["fn118", "fn301"]),
        ],
        "Noctilum": [
            # id, name, prod_rank, rev_rank, combat_rank, sightseeing, prec_resources, [connected_node_ids]
            ("fn201", "FN Site 201", ProdRank.C, RevRank.B, "S", None, None, ["fn206"]),
            ("fn202", "FN Site 202", ProdRank.C, RevRank.C, "B", None, ["Cimmerian Cinnabar", "Everfreeze Ore"], ["fn203", "fn207", "fn208"]),
            ("fn203", "FN Site 203", ProdRank.C, RevRank.A, "B", None, ["Cimmerian Cinnabar"], ["fn202", "fn204"]),
            ("fn204", "FN Site 204", ProdRank.A, RevRank.C, "B", None, None, ["fn203", "fn205", "fn211", "fn212"]),
            ("fn205", "FN Site 205", ProdRank.A, RevRank.F, "B", None, None, ["fn204", "fn209"]),
            ("fn206", "FN Site 206", ProdRank.B, RevRank.A, "S", None, None, ["fn201", "fn207", "fn213"]),
            ("fn207", "FN Site 207", ProdRank.C, RevRank.C, "B", None, ["Cimmerian Cinnabar", "Foucaultium", "Infernium", "White Cometite"], ["fn202", "fn206"]),
            ("fn208", "FN Site 208", ProdRank.B, RevRank.D, "B", None, ["Foucaultium"], ["fn202"]),
            ("fn209", "FN Site 209", ProdRank.C, RevRank.F, "B", None, None, ["fn205"]),
            ("fn210", "FN Site 210", ProdRank.B, RevRank.D, "B", None, None, ["fn211"]),
            ("fn211", "FN Site 211", ProdRank.A, RevRank.D, "B", None, None, ["fn204","fn210"]),
            ("fn212", "FN Site 212", ProdRank.B, RevRank.E, "B", None, ["Aurorite", "Enduron Lead", "White Cometite"], ["fn204", "fn216"]),
            ("fn213", "FN Site 213", ProdRank.C, RevRank.S, "B", ["Sentinel's Nest"], None, ["fn206"]),
            ("fn214", "FN Site 214", ProdRank.C, RevRank.D, "B", ["Millstone Ridge", "Skygazer's Atrium"], None, ["fn215"]),
            ("fn215", "FN Site 215", ProdRank.C, RevRank.D, "B", None, ["Aurorite", "Enduron Lead", "Everfreeze Ore", "Foucaultium"], ["fn214", "fn218"]),
            ("fn216", "FN Site 216", ProdRank.C, RevRank.A, "A", ["Cascade Isle"], None, ["fn212", "fn218", "fn225"]),
            ("fn217", "FN Site 217", ProdRank.C, RevRank.C, "B", None, ["Aurorite", "Cimmerian Cinnabar", "Infernium"], ["fn222"]),
            ("fn218", "FN Site 218", ProdRank.C, RevRank.E, "B", None, ["Aurorite", "Enduron Lead", "White Cometite"], ["fn215", "fn216", "fn224"]),
            ("fn219", "FN Site 219", ProdRank.C, RevRank.E, "B", None, ["Enduron Lead", "White Cometite"], ["fn220"]),
            ("fn220", "FN Site 220", ProdRank.C, RevRank.C, "A", ["Orochi's Belly"], ["Everfreeze Ore", "Infernium"], ["fn219", "fn221", "fn225"]),
            ("fn221", "FN Site 221", ProdRank.C, RevRank.E, "B", ["Ensanguined Font", "Yagami's Vista"], None, ["fn220", "fn222"]),
            ("fn222", "FN Site 222", ProdRank.C, RevRank.D, "B", ["Whale's Weeper"], None, ["fn103", "fn217", "fn221"]),
            ("fn223", "FN Site 223", ProdRank.C, RevRank.F, "B", ["Idyll Beach"], None, ["fn224"]),
            ("fn224", "FN Site 224", ProdRank.C, RevRank.A, "B", None, None, ["fn218", "fn223"]),
            ("fn225", "FN Site 225", ProdRank.C, RevRank.A, "B", ["Decapotamon Vista"], None, ["fn216", "fn220"]),
        ],
        "Oblivia": [
            # Need to do Oblivia nodes (FN Site 3xx)
        ],
        "Sylvalum": [
            # Need to do Sylvalum nodes (FN Site 4xx)
        ],
        "Cauldros": [
            # Need to do Cauldros nodes (FN Site 5xx)
        ]
    }

    # Creates a nodes dictionary
    nodes = {}
    for region, region_nodes_data in node_data.items():
        nodes[region] = {}
        for node_id, name, prod_rank, rev_rank, combat_rank, sightseeing, prec_resources in region_nodes_data:
            nodes[region][node_id] = Node(name, prod_rank, rev_rank, combat_rank, sightseeing, prec_resources)

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
        "research": 6, 
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
