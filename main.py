from data import node_data, test_data, load_game_data
from frontiernav import FrontierNav

if __name__ == "__main__":
    game_data = load_game_data(node_data)
    frontier_nav = FrontierNav(game_data)
    probe1 = frontier_nav.probes["mining"][5]
    probe2 = frontier_nav.probes["booster"][1]
    probe3 = frontier_nav.probes["storage"][0]
    frontier_nav.nodes["Primordia"]["fn101"].probe_slot.install_probe(probe1)
    frontier_nav.nodes["Primordia"]["fn108"].probe_slot.install_probe(probe1)
    frontier_nav.nodes["Primordia"]["fn102"].probe_slot.install_probe(probe2)
    frontier_nav.nodes["Primordia"]["fn103"].probe_slot.install_probe(probe3)
    frontier_nav.nodes["Noctilum"]["fn225"].probe_slot.lock_probe()
    print(frontier_nav.nodes["Primordia"]["fn104"].probe_slot.calculate_output())
    print(frontier_nav.calculate_total())
    