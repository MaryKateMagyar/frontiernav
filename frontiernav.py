class FrontierNav:
    def __init__(self, game_data):
        self.nodes = game_data["nodes"]
        self.connections = game_data["connections"]
        self.slots = game_data["slots"]
        self.probes = game_data["probes"]

        self.miranium = 0
        self.credits = 0
        self.storage = 6000
        self.prec_resources = set()

    def calculate_total(self):
        for region in self.slots:
            for node_id in self.slots[region]:
                slot = self.slots[region][node_id]
                current_slot_totals = slot.calculate_output()

                self.miranium += current_slot_totals[0]
                self.credits += current_slot_totals[1]
                self.storage += current_slot_totals[2]

                pr_output = current_slot_totals[3]
                for pr in pr_output:
                    self.prec_resources.add(pr)

        return {
            "total miranium": self.miranium,
            "total credits": self.credits,
            "total storage": self.storage,
            "possible resources": list(self.prec_resources)
        }

    def print_game_data(self):     
        # Prints current data for FrontierNav in the terminal
        print("---- Xenoblade Chronicles X: Definitive Edition ----")
        print("----------------- FrontierNav Data -----------------\n")

        for region in self.nodes:
            print(f">>> {region} <<<")
            for node_id in self.nodes[region]:
                node = self.nodes[region][node_id]
                print(f"{node.name}")
                print(f"\n- Production Rank: {node.prod_rank.value[0]}")
                print(f"- Revenue Rank: {node.rev_rank.value[0]}")
                print(f"- Combat Rank: {node.combat_rank}")
                
                ssing_sites = "- Sightseeing Sites: "
                if node.sightseeing:
                    ssing_sites += f"{len(node.sightseeing)}"
                    for i in range(len(node.sightseeing)):
                        ssing_sites += f"\n     * {node.sightseeing[i]}"
                else:
                    ssing_sites += "0"
                print(ssing_sites)

                resources = "- Precious Resources: "
                if node.prec_resources:
                    resources += f"{len(node.prec_resources)}"
                    for i in range(len(node.prec_resources)):
                        resources += f"\n     * {node.prec_resources[i]}"
                else:
                    resources += "0"
                print(resources)
                
                connects_to = "- Connected To: "
                if node.connections:
                    connects_to += f"{len(node.connections)}"
                    for connection in node.connections:
                        connection = repr(connection)
                        links = connection.removeprefix("Connection(FN Site ").removesuffix(")")
                        links = links.split(", FN Site")
                        for link in links:
                            link = link.strip(" ")
                            if link != node.name.removeprefix("FN Site "):
                                connects_to += f"\n     * {link}"
                else:
                    connects_to += "0"
                print(connects_to)
                print(f"- Installed Probe: {node.probe_slot.installed_probe.name}")


    def save_game_data_to_file(self, file_name="current_frontiernav_game_data.txt"):
        # Creates a .txt file with the current data for FrontierNav
        lines = []
        lines.append("---- Xenoblade Chronicles X: Definitive Edition ----")
        lines.append("----------------- FrontierNav Data -----------------\n")

        for region in self.nodes:
            lines.append(f"\n>>> {region} <<<")
            for node_id in self.nodes[region]:
                node = self.nodes[region][node_id]
                lines.append(f"\n{node.name}")
                lines.append(f"- Production Rank: {node.prod_rank.value[0]}")
                lines.append(f"- Revenue Rank: {node.rev_rank.value[0]}")
                lines.append(f"- Combat Rank: {node.combat_rank}")
                
                ssing_sites = "- Sightseeing Sites: "
                if node.sightseeing:
                    ssing_sites += f"{len(node.sightseeing)}"
                    for i in range(len(node.sightseeing)):
                        ssing_sites += f"\n     * {node.sightseeing[i]}"
                else:
                    ssing_sites += "0"
                lines.append(ssing_sites)

                resources = "- Precious Resources: "
                if node.prec_resources:
                    resources += f"{len(node.prec_resources)}"
                    for i in range(len(node.prec_resources)):
                        resources += f"\n     * {node.prec_resources[i]}"
                else:
                    resources += "0"
                lines.append(resources)
                
                connects_to = "- Connected To: "
                if node.connections:
                    connects_to += f"{len(node.connections)}"
                    for connection in node.connections:
                        connection = repr(connection)
                        links = connection.removeprefix("Connection(FN Site ").removesuffix(")")
                        links = links.split(", FN Site")
                        for link in links:
                            link = link.strip(" ")
                            if link != node.name.removeprefix("FN Site "):
                                connects_to += f"\n     * {link}"
                else:
                    connects_to += "0"
                lines.append(connects_to)
                lines.append(f"- Installed Probe: {node.probe_slot.installed_probe.name}")
        
        with open(file_name, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
