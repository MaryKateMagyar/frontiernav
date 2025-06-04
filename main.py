from data import node_data, test_data, load_game_data, print_game_data, save_game_data_to_file

if __name__ == "__main__":
    game_data = load_game_data(node_data)
    probe1 = game_data["probes"]["mining"][8]
    probe2 = game_data["probes"]["booster"][1]
    probe3 = game_data["probes"]["storage"][0]
    game_data["nodes"]["Primordia"]["fn101"].probe_slot.install_probe(probe1)
    game_data["nodes"]["Primordia"]["fn102"].probe_slot.install_probe(probe2)
    game_data["nodes"]["Primordia"]["fn103"].probe_slot.install_probe(probe3)
    game_data["nodes"]["Noctilum"]["fn225"].probe_slot.lock_probe()
    #print_game_data(game_data)
    save_game_data_to_file(game_data)