from data import NODE_DATA, TEST_DATA 
from frontiernav import FrontierNav
from window import GUI

if __name__ == "__main__":
    # frontier_nav = FrontierNav(FrontierNav.load_game_data(NODE_DATA))
    # probe1 = frontier_nav.probes["mining"][5]
    # probe2 = frontier_nav.probes["booster"][1]
    # probe3 = frontier_nav.probes["duplicator"][0]
    # frontier_nav.nodes["Primordia"]["fn102"].probe_slot.install_probe(probe1)
    # frontier_nav.nodes["Primordia"]["fn104"].probe_slot.install_probe(probe1)
    # frontier_nav.nodes["Primordia"]["fn106"].probe_slot.install_probe(probe1)
    # frontier_nav.nodes["Primordia"]["fn103"].probe_slot.install_probe(probe2)
    # frontier_nav.nodes["Primordia"]["fn101"].probe_slot.install_probe(probe3)
    # frontier_nav.nodes["Primordia"]["fn105"].probe_slot.install_probe(probe3)
    # frontier_nav.nodes["Primordia"]["fn109"].probe_slot.install_probe(probe3)
    # #print(frontier_nav.calculate_total())
    # print(frontier_nav.probes)
    GUI(NODE_DATA)