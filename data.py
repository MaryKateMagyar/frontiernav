from nodes import Node, ProdRank, RevRank, Connection
from probes import ProbeSlot, Probe, ProbeType

# In-game data for each node
# Later will need location data for the GUI
NODE_DATA = {
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
        ("fn121", "FN Site 121", ProdRank.A, RevRank.E, "B", None, None, ["fn118", "fn301"])
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
        ("fn225", "FN Site 225", ProdRank.C, RevRank.A, "B", ["Decapotamon Vista"], None, ["fn216", "fn220"])
    ],
    "Oblivia": [
        # id, name, prod_rank, rev_rank, combat_rank, sightseeing, prec_resources, [connected_node_ids]
        ("fn301", "FN Site 301", ProdRank.B, RevRank.D, "B", None, ["Arc Sand Ore", "Infernium", "Lionbone Bort"], ["fn121", "fn302", "fn303"]),
        ("fn302", "FN Site 302", ProdRank.C, RevRank.E, "B", None, None, ["fn301"]),
        ("fn303", "FN Site 303", ProdRank.C, RevRank.E, "B", None, ["Aurorite", "White Cometite"], ["fn301", "fn306"]),
        ("fn304", "FN Site 304", ProdRank.B, RevRank.A, "S", None, None, ["fn305", "fn306", "fn309"]),
        ("fn305", "FN Site 305", ProdRank.C, RevRank.E, "B", None, ["Arc Sand Ore", "Aurorite", "Enduron Lead"], ["fn304", "fn308"]),
        ("fn306", "FN Site 306", ProdRank.C, RevRank.D, "B", ["Cryptic Sign"], None, ["fn303", "fn304", "fn307"]),
        ("fn307", "FN Site 307", ProdRank.C, RevRank.B, "B", None, ["Arc Sand Ore", "Enduron Lead", "Infernium", "White Cometite"], ["fn306", "fn313"]),
        ("fn308", "FN Site 308", ProdRank.B, RevRank.C, "A", None, ["Ouroboros Crystal"], ["fn305"]),
        ("fn309", "FN Site 309", ProdRank.C, RevRank.C, "B", None, ["Enduron Lead", "Ouroboros Crystal"], ["fn304", "fn311"]),
        ("fn310", "FN Site 310", ProdRank.C, RevRank.A, "B", None, None, ["fn311"]),
        ("fn311", "FN Site 311", ProdRank.C, RevRank.B, "B", None, None, ["fn309", "fn310"]),
        ("fn312", "FN Site 312", ProdRank.C, RevRank.D, "B", None, ["Boiled-Egg Ore", "Infernium", "Lionbone Bort"], ["fn313", "fn315"]),
        ("fn313", "FN Site 313", ProdRank.C, RevRank.E, "A", ["Azure Lagoon", "Crater Oasis"], None, ["fn307", "fn312", "fn314"]),
        ("fn314", "FN Site 314", ProdRank.C, RevRank.B, "S", None, None, ["fn313"]),
        ("fn315", "FN Site 315", ProdRank.A, RevRank.S, "B", ["Kintrees", "Mount Edge Peak"], None, ["fn312", "fn316", "fn318", "fn321"]),
        ("fn316", "FN Site 316", ProdRank.C, RevRank.D, "B", None, None, ["fn315"]),
        ("fn317", "FN Site 317", ProdRank.C, RevRank.A, "B", ["Beachside Trove"], None, ["fn318", "fn319"]),
        ("fn318", "FN Site 318", ProdRank.C, RevRank.B, "B", ["Atop the Giant Ring", "Primeval Meadow"], ["Boiled-Egg Ore", "Lionbone Bort", "White Cometite"], ["fn315", "fn317"]),
        ("fn319", "FN Site 319", ProdRank.C, RevRank.D, "B", ["Great Washington Isle"], ["Boiled-Egg Ore", "Infernium"], ["fn317"]),
        ("fn320", "FN Site 320", ProdRank.C, RevRank.B, "B", None, ["Aurorite", "Ouroboros Crystal"], ["fn321"]),
        ("fn321", "FN Site 321", ProdRank.A, RevRank.D, "A", None, None, ["fn315", "fn320", "fn322"]),
        ("fn322", "FN Site 322", ProdRank.A, RevRank.A, "B", None, None, ["fn321"])
    ],
    "Sylvalum": [
        # id, name, prod_rank, rev_rank, combat_rank, sightseeing, prec_resources, [connected_node_ids]
        ("fn401", "FN Site 401", ProdRank.C, RevRank.B, "B", None, ["Marine Rutile", "Parhelion Platinum"], ["fn402", "fn404"]),
        ("fn402", "FN Site 402", ProdRank.A, RevRank.B, "B", None, None, ["fn401", "fn408"]),
        ("fn403", "FN Site 403", ProdRank.A, RevRank.C, "S", None, None, ["fn405"]),
        ("fn404", "FN Site 404", ProdRank.B, RevRank.S, "S", ["Abyss Reservoir"], None, ["fn401", "fn407"]),
        ("fn405", "FN Site 405", ProdRank.A, RevRank.E, "A", None, ["Arc Sand Ore"], ["fn403", "fn408", "fn409"]),
        ("fn406", "FN Site 406", ProdRank.C, RevRank.B, "B", None, None, ["fn408"]),
        ("fn407", "FN Site 407", ProdRank.A, RevRank.B, "B", None, None, ["fn404", "fn412"]),
        ("fn408", "FN Site 408", ProdRank.B, RevRank.D, "B", ["Sandsprint Cavity"], ["Arc Sand Ore", "Aurorite", "Everfreeze Ore"], ["fn402", "fn405", "fn406", "fn413"]),
        ("fn409", "FN Site 409", ProdRank.B, RevRank.S, "B", None, None, ["fn113", "fn405", "fn411"]),
        ("fn410", "FN Site 410", ProdRank.C, RevRank.S, "B", ["Arc Rock"], None, ["fn412"]),
        ("fn411", "FN Site 411", ProdRank.A, RevRank.A, "S", None, None, ["fn409", "fn414"]),
        ("fn412", "FN Site 412", ProdRank.A, RevRank.B, "A", None, None, ["fn407", "fn410", "fn415"]),
        ("fn413", "FN Site 413", ProdRank.C, RevRank.A, "B", ["Xanadu Overlook"], None, ["fn408", "fn416"]),
        ("fn414", "FN Site 414", ProdRank.C, RevRank.B, "B", ["Noctilucent Sphere Interior", "Quay Hollows"], ["Marine Rutile", "Perhelion Platinum"], ["fn411"]),
        ("fn415", "FN Site 415", ProdRank.C, RevRank.S, "B", None, None, ["fn412", "fn502"]),
        ("fn416", "FN Site 416", ProdRank.C, RevRank.B, "B", None, None, ["fn413", "fn418", "fn419"]),
        ("fn417", "FN Site 417", ProdRank.B, RevRank.D, "B", None, ["Boiled-Egg Ore", "Everfreeze Ore"], ["fn419"]),
        ("fn418", "FN Site 418", ProdRank.C, RevRank.C, "B", None, ["Arc Sand Ore", "Boiled-Egg Ore", "Everfreeze Ore", "Marine Rutile", "Parhelion Platinum"], ["fn416"]),
        ("fn419", "FN Site 419", ProdRank.C, RevRank.S, "S", ["Behemoth's Shadows"], None, ["fn416", "fn417", "fn420"]),
        ("fn420", "FN Site 420", ProdRank.B, RevRank.C, "B", None, ["Everfreeze Ore"], ["fn419"]),
    ],
    "Cauldros": [
        # id, name, prod_rank, rev_rank, combat_rank, sightseeing, prec_resources, [connected_node_ids]
        ("fn501", "FN Site 501", ProdRank.B, RevRank.F, "B", None, ["Arc Sand Ore"], ["fn502"]),
        ("fn502", "FN Site 502", ProdRank.A, RevRank.C, "B", ["Infernal Ledges"], ["Bonjelium"], ["fn415", "fn501", "fn503"]),
        ("fn503", "FN Site 503", ProdRank.C, RevRank.D, "B", ["M'gando Volcanic Crater", "White Phosphor Lake"], ["Enduron Lead"], ["fn502", "fn504"]),
        ("fn504", "FN Site 504", ProdRank.C, RevRank.C, "B", None, ["Arc Sand Ore", "Bonjelium", "Enduron Lead", "Marine Rutile"], ["fn503", "fn508"]),
        ("fn505", "FN Site 505", ProdRank.C, RevRank.B, "B", ["Beneath O'rrh Sim Keep", "Ganglion Antropolis"], None, ["fn506", "fn509"]),
        ("fn506", "FN Site 506", ProdRank.C, RevRank.B, "B", ["Forgotten Mining Frigate 1"], ["Arc Sand Ore", "Bonjelium"], ["fn505"]),
        ("fn507", "FN Site 507", ProdRank.C, RevRank.A, "B", ["Bandit's Refuge"], ["Bonjelium"], ["fn508"]),
        ("fn508", "FN Site 508", ProdRank.A, RevRank.B, "S", ["O'rrh Sim Castle Ruins"], ["Enduron Lead", "Marine Rutile"], ["fn504", "fn507", "fn509", "fn511"]),
        ("fn509", "FN Site 509", ProdRank.A, RevRank.A, "A", None, None, ["fn505", "fn508", "fn510", "fn513"]),
        ("fn510", "FN Site 510", ProdRank.C, RevRank.B, "B", None, ["Bonjelium"], ["fn509"]),
        ("fn511", "FN Site 511", ProdRank.A, RevRank.C, "A", None, ["Bonjelium"], ["fn508", "fn512", "fn514"]),
        ("fn512", "FN Site 512", ProdRank.C, RevRank.A, "S", None, None, ["fn511"]),
        ("fn513", "FN Site 513", ProdRank.C, RevRank.A, "B", ["M'gando Mineral Spring"], None, ["fn509", "fn516"]),
        ("fn514", "FN Site 514", ProdRank.C, RevRank.A, "B", ["Kw'arah Cloister"], None, ["fn511", "fn515"]),
        ("fn515", "FN Site 515", ProdRank.C, RevRank.B, "S", None, None, ["fn514"]),
        ("fn516", "FN Site 516", ProdRank.B, RevRank.E, "B", None, None, ["fn513"]),
    ]
}

TEST_DATA = {
    "Primordia": [
        # id, name, prod_rank, rev_rank, combat_rank, sightseeing, prec_resources, [connected_node_ids] 
        ("fn101", "FN Site 101", ProdRank.C, RevRank.S, "S", ["Stonelattice Cavern"], None, ["fn103"]),
        ("fn102", "FN Site 102", ProdRank.C, RevRank.F, "B", None, None, ["fn103"]),
        ("fn103", "FN Site 103", ProdRank.C, RevRank.E, "A", ["Wonderment Bluff"], None, ["fn101", "fn102"])
    ],
    "Noctilum": [
        ("fn219", "FN Site 219", ProdRank.C, RevRank.E, "B", None, ["Enduron Lead", "White Cometite"], ["fn220"]),
        ("fn220", "FN Site 220", ProdRank.C, RevRank.C, "A", ["Orochi's Belly"], ["Everfreeze Ore", "Infernium"], ["fn219", "fn225"]),
        ("fn223", "FN Site 223", ProdRank.C, RevRank.F, "B", ["Idyll Beach"], None, ["fn224"]),
        ("fn224", "FN Site 224", ProdRank.C, RevRank.A, "B", None, None, ["fn223"]),
        ("fn225", "FN Site 225", ProdRank.C, RevRank.A, "B", ["Decapotamon Vista"], None, ["fn220"])
    ]
}

PROBE_MAX_GEN = {
    "locked": None,
    "basic": None,
    "mining": 10, 
    "research": 6, 
    "booster": 2, 
    "duplicator": None, 
    "storage": None, 
    "combat": None,
}

# Basic, duplicator, storage, and combat nodes only have a single version each,
# meaning they essentially have no generations that will be used for calculations

PROBE_COSTS = {
    "locked": {0: 0},
    "basic": {0: 0},
    "mining": {
        1: 1000,
        2: 2000,
        3: 3000,
        4: 5000,
        5: 7000,
        6: 10000,
        7: 15000,
        8: 20000,
        9: 30000,
        10: 50000
    },
    "research": {
        1: 2000,
        2: 5000,
        3: 9000,
        4: 12000,
        5: 20000,
        6: 35000
    },
    "booster": {
        1: 7000,
        2: 13000
    },
    "duplicator": {0: 6000},
    "storage": {0: 5000},
    "combat": {0: 0}
}



