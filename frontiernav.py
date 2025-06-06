from nodes import Node, Connection
from probes import ProbeSlot, Probe, ProbeType
from data import PROBE_COSTS, PROBE_MAX_GEN

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
        self.cost = 0

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

                self.cost += slot.installed_probe.cost

        return {
            "total miranium": self.miranium,
            "total credits": self.credits,
            "total storage": self.storage,
            "possible resources": list(self.prec_resources),
            "total cost": self.cost
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

    @staticmethod
    def load_game_data(node_data):
        # Creates a nodes dictionary
        nodes = {}
        all_node_ids = set()
        for region, region_nodes_data in node_data.items():
            nodes[region] = {}
            for node_id, name, prod_rank, rev_rank, combat_rank, sightseeing, prec_resources, _ in region_nodes_data:
                nodes[region][node_id] = Node(name, prod_rank, rev_rank, combat_rank, sightseeing, prec_resources)
                all_node_ids.add(node_id)

        # Creates connections between nodes which are connected in game for adjacent bonuses
        connections = []
        made_connections = set()
        for region, region_nodes_data in node_data.items():
            for node_info in region_nodes_data:
                node_id = node_info[0]
                connected_ids = node_info[7]

                for connected_id in connected_ids:
                    if connected_id in all_node_ids:
                        if connected_id in nodes[region]:
                            connected_region = region
                        elif connected_id.startswith("fn1"):
                            connected_region = "Primordia"
                        elif connected_id.startswith("fn2"):
                            connected_region = "Noctilum"
                        elif connected_id.startswith("fn3"):
                            connected_region = "Oblivia"
                        elif connected_id.startswith("fn4"):
                            connected_region = "Sylvalum"
                        elif connected_id.startswith("fn5"):
                            connected_region = "Cauldros"
                        else:
                            print(f"Warning: {connected_ids} is not in a valid region")

                        if frozenset([node_id, connected_id]) not in made_connections:
                            connections.append(Connection(nodes[region][node_id], nodes[connected_region][connected_id]))
                            made_connections.add(frozenset([node_id, connected_id]))
                    else:
                        print(f"Warning: Cannot create Connection between {node_id} and {connected_id} as {connected_id} node does not exist!")

        # Creates a probe slot for each node
        slots = {}
        for region, region_nodes in nodes.items():
            slots[region] = {}
            for node_id, node in region_nodes.items():
                slots[region][node_id] = ProbeSlot(node)

        # Creates all possible probes in the game
        probes = {}
        for probe_type, max_gen in PROBE_MAX_GEN.items():
            probes[probe_type] = {}
            probe_name = f"{probe_type.capitalize()}"

            try:
                enum_type = getattr(ProbeType, probe_type.upper())
            except AttributeError:
                print(f"Warning: ProbeType.{probe_type.upper()} does not exist in the ProbeType enum!")
                continue

            if max_gen is None:
                if probe_type != "locked":
                    probe_name_new = probe_name + " Probe"
                else:
                    probe_name_new = "Probe Slot Locked"

                # Use key 0 for probes with no generations
                cost = PROBE_COSTS[probe_type][0]
                probes[probe_type] = {0: Probe(enum_type, None, probe_name_new, cost)}

            else:
                for gen in range(1, max_gen + 1):
                    probe_name_new = probe_name + f" G{gen} Probe"
                    cost = PROBE_COSTS[probe_type][gen]
                    probes[probe_type][gen] = Probe(enum_type, gen, probe_name_new, cost)


        return {
            "nodes": nodes,
            "connections": connections,
            "slots": slots,
            "probes": probes
        }
