from enum import Enum

class ProdRank(Enum):
    A = ("A", 500)    # Baseline of 500 miranium per tick
    B = ("B", 350)    # Baseline of 350 miranium per tick
    C = ("C", 250)    # Baseline of 250 miranium per tick

class RevRank(Enum):
    S = ("S", 850)     # Baseline of 850 credits per tick
    A = ("A", 750)     # Baseline of 750 credits per tick
    B = ("B", 650)     # Baseline of 650 credits per tick
    C = ("C", 550)     # Baseline of 550 credits per tick
    D = ("D", 450)     # Baseline of 450 credits per tick
    E = ("E", 300)     # Baseline of 300 credits per tick
    F = ("F", 200)     # Baseline of 200 credits per tick

class Node:
    def __init__(self, name, prod_rank, rev_rank, combat_rank, sightseeing, prec_resources):
        self.name = name                    # The name of the node, a string (ex. "FN Site 104")
        self.prod_rank = prod_rank          # The rank of the node's production ability, which is a member of the ProdRank enum
        self.rev_rank = rev_rank            # The rank of the node's revenue ability, which is a member of the RevRank enum
        self.combat_rank = combat_rank      # The rank of the node's combat support, a string (ex. "A"), which is not used in any relevant calculations
        
        self.sightseeing = sightseeing              # A list of the node's sightseeing spots
        self.prec_resources = prec_resources        # A list of available precious resources from the node

        self.prod_letter = prod_rank.value[0]   # The string of the node's production rank
        self.prod_value = prod_rank.value[1]    # The integer of the node's miranium production per tick

        self.rev_letter = rev_rank.value[0]     # The string of the node's revenue rank
        self.rev_value = rev_rank.value[1]      # The integer of the node's credit production per tick

        self.connections = []       # List of Connection objects, not nodes

        self.probe_slot = None      # The ProbeSlot that a Node is linked to

    def get_adjacent_nodes(self):
        # Return a list of node objects that are connected to self
        adjacent = []
        for connection in self.connections:
            if connection.node1 == self:
                adjacent.append(connection.node2)
            else:
                adjacent.append(connection.node1)
        return adjacent
    
    def __repr__(self):
        return f"Node({self.name}, {self.prod_rank}, {self.rev_rank}, {self.combat_rank}, {self.sightseeing}, {self.prec_resources})"

    
class Connection:
    # Tells the nodes that they are connected to one another
    def __init__(self, node1, node2):
        self.node1 = node1
        self.node2 = node2

        node1.connections.append(self)
        node2.connections.append(self)

    def get_other_node(self, node):
        if node == self.node1:
            return self.node2
        elif node == self.node2:
            return self.node1
        else:
            raise ValueError(f"Node {node.name} is not part of this connection")

class ProbeType(Enum):
    BASIC = "Basic Probe"
    MINING = "Mining Probe"
    RESEARCH = "Research Probe"
    BOOSTER = "Booster Probe"
    DUPLICATOR = "Duplicator Probe"
    STORAGE = "Storage Probe"
    COMBAT = "Combat Probe"

class Probe:
    def __init__(self, probe_type, gen=None, name=None):
        self.probe_type = probe_type    # The type of probe this instance contains, which is a member of the ProbeType enum
        self.gen = gen                  # The generation of the probe, used for calculations (ex. 1 = G1, 2 = G2, 3 = G3, etc)
        self.name = name                # The name of the probe as a string

    def __repr__(self):
        return f"Probe({self.probe_type}, {self.gen}, {self.name})"

class ProbeSlot:
    node_to_slot = {}

    def __init__(self, node):
        self.node = node
        self.installed_probe = Probe(ProbeType.BASIC)     # Initializes with a basic probe in each slot to reflect in-game behavior of FrontierNav
        ProbeSlot.node_to_slot[node] = self               # Adds the ProbeSlot node to a list of Nodes with a ProbeSlot
        node.probe_slot = self                            # Tells the Node which ProbeSlot it's linked to

    def __repr__(self):
        return f"ProbeSlot(node={self.node}, probe={self.installed_probe})"

    def __str__(self):
        return f"ProbeSlot(node={self.node}, probe={self.installed_probe})"

    def install_probe(self, probe):
        self.installed_probe = probe

    def uninstall_probe(self):
        self.installed_probe = None     # Used to block off probes that have not been unlocked yet

    def get_adjacent_probes(self):
        # Return a list of Probe objects that are installed in adjacent slots
        adjacent_probes = []
        adjacent_nodes = self.node.get_adjacent_nodes()

        for adj_node in adjacent_nodes:
            adj_slot = adj_node.probe_slot

            if adj_slot.installed_probe:
                adjacent_probes.append(adj_slot.installed_probe)

        return adjacent_probes
    

    def calculate_output(self):
        miranium = 0
        credits = 0
        storage = 0
        precious_resources = []

        match self.installed_probe.probe_type:

            case ProbeType.BASIC:
                miranium = self.node.prod_value * 0.50
                credits = self.node.rev_value * 0.50
                return miranium, credits, storage, precious_resources

            case ProbeType.MINING:
                if self.installed_probe.gen <= 0:
                    gen_multiplier = 1.0
                elif self.installed_probe.gen <= 8:
                    gen_multiplier = 1 + (0.2 * (self.installed_probe.gen - 1))
                elif self.installed_probe.gen == 9:
                    gen_multiplier = 1.1 + (0.2 * (self.installed_probe.gen - 1))
                elif self.installed_probe.gen == 10:
                    gen_multiplier = 1.2 + (0.2 * (self.installed_probe.gen - 1))
                else:
                    gen_multiplier = 3.0

                miranium = self.node.prod_value * gen_multiplier
                credits = self.node.rev_value * 0.30

                if self.node.prec_resources:
                    precious_resources = list(self.node.prec_resources)

                return miranium, credits, storage, precious_resources

            case ProbeType.RESEARCH:
                if self.installed_probe.gen <= 1:
                    gen_multiplier = 1.5
                elif self.installed_probe.gen <= 6:
                    gen_multiplier = 0.5 * (self.installed_probe.gen + 3)
                else:
                    gen_multiplier = 4.5

                miranium = self.node.prod_value * 0.50
                credits = self.node.rev_value * gen_multiplier

                if self.node.sightseeing:
                    credits += len(self.node.sightseeing) * (500 * (self.installed_probe.gen + 3))

                return miranium, credits, storage, precious_resources

            case ProbeType.BOOSTER:
                miranium = self.node.prod_value * 0.10
                credits = self.node.rev_value * 0.10

                adjacent_nodes = self.node.get_adjacent_nodes()

                for adj_node in adjacent_nodes:
                    if adj_node in ProbeSlot.node_to_slot:
                        adj_slot = ProbeSlot.node_to_slot[adj_node]
                        if adj_slot.installed_probe.probe_type != ProbeType.BOOSTER:
                            adj_miranium, adj_credits, adj_storage, adj_precious = adj_slot.calculate_output()
                            if self.installed_probe.gen == 1:
                                miranium += adj_miranium * 0.5
                                credits += adj_credits * 0.5
                                storage += adj_storage * 0.5
                            elif self.installed_probe.gen == 2:
                                miranium += adj_miranium * 1.0
                                credits += adj_credits * 1.0
                                storage += adj_storage * 1.0

                return miranium, credits, storage, precious_resources

            case ProbeType.DUPLICATOR:
                adjacent_probes = self.get_adjacent_probes()

                for adj_probe in adjacent_probes:
                    if adj_probe.probe_type != ProbeType.DUPLICATOR:
                        original_probe = self.installed_probe
                        self.installed_probe = adj_probe

                        duped_output = self.calculate_output()

                        miranium += duped_output[0] # Using the adjacent probe, adds the miranium produced to the node's total output
                        credits += duped_output[1]  # Using the adjacent probe, adds the credits produced to the node's total output
                        storage += duped_output[2]  # Using the adjacent probe, adds the storage alloted to the node's total output

                        if (adj_probe.probe_type == ProbeType.MINING and duped_output[3]) and len(precious_resources) == 0:   # If using the adjacent probe has a chance to produce any precious resources, adds them to the list of the node's output
                            precious_resources = duped_output[3]

                        self.installed_probe = original_probe

                return miranium, credits, storage, precious_resources

            case ProbeType.STORAGE:
                miranium = self.node.prod_value * 0.10
                credits = self.node.rev_value * 0.10
                storage = 3000
                return miranium, credits, storage, precious_resources

            case ProbeType.COMBAT:
                miranium = self.node.prod_value * 0.10
                credits = self.node.rev_value * 0.10
                return miranium, credits, storage, precious_resources
                
            case __:
                return miranium, credits, storage, precious_resources


        