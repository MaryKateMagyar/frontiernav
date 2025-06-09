from enum import Enum

class ProbeType(Enum):
    BASIC = "Basic Probe"
    MINING = "Mining Probe"
    RESEARCH = "Research Probe"
    BOOSTER = "Booster Probe"
    DUPLICATOR = "Duplicator Probe"
    STORAGE = "Storage Probe"
    COMBAT = "Combat Probe"
    LOCKED = "Node not yet unlocked"
    # Need to adjust logic to account for Locked probes/nodes

class Probe:
    def __init__(self, probe_type, gen=None, name=None, cost=0):
        self.probe_type = probe_type    # The type of probe this instance contains, which is a member of the ProbeType enum
        self.gen = gen                  # The generation of the probe, used for calculations (ex. 1 = G1, 2 = G2, 3 = G3, etc)
        self.name = name                # The name of the probe as a string
        self.cost = cost                # The cost to install the probe
        self.boosted = 0


    def __repr__(self):
        return f"Probe({self.probe_type}, {self.gen}, {self.name})"

class ProbeSlot:
    node_to_slot = {}

    def __init__(self, node):
        self.node = node
        self.installed_probe = Probe(ProbeType.LOCKED, None, "Probe Slot Locked")     # Initializes with all slots locked
        ProbeSlot.node_to_slot[node] = self               # Adds the ProbeSlot node to a list of Nodes with a ProbeSlot
        node.probe_slot = self                            # Tells the Node which ProbeSlot it's linked to

    def __repr__(self):
        return f"ProbeSlot(node={self.node}, probe={self.installed_probe})"

    def __str__(self):
        return f"ProbeSlot(node={self.node}, probe={self.installed_probe})"

    def install_probe(self, probe):
        self.installed_probe = probe
        probe.boosted = 0

    def lock_probe(self):
        self.installed_probe = Probe(ProbeType.LOCKED, None, "Probe Slot is Locked")     # Used to block off probes that have not been unlocked yet

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
        miranium, credits, storage, prec_resources = self._calculate_base_output()
        miranium, credits, storage = self._apply_booster_effect(miranium, credits, storage)
        miranium, credits, storage = self._apply_link_multiplier(miranium, credits, storage)
        return int(miranium), int(credits), int(storage), prec_resources

    
    def _calculate_base_output(self):
        miranium = 0
        credits = 0
        storage = 0
        precious_resources = []

        match self.installed_probe.probe_type:

            case ProbeType.BASIC:
                miranium = self.node.prod_rank.value[1] * 0.50
                credits = self.node.rev_rank.value[1] * 0.50


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

                miranium = self.node.prod_rank.value[1] * gen_multiplier
                credits = self.node.rev_rank.value[1] * 0.30 

                if self.node.prec_resources:
                    precious_resources = list(self.node.prec_resources)


            case ProbeType.RESEARCH:
                if self.installed_probe.gen <= 1:
                    gen_multiplier = 1.5
                elif self.installed_probe.gen <= 6:
                    gen_multiplier = 0.5 * (self.installed_probe.gen + 3)
                else:
                    gen_multiplier = 4.5

                miranium = self.node.prod_rank.value[1] * 0.50 
                credits += self.node.rev_rank.value[1] * gen_multiplier

                if self.node.sightseeing:
                    credits = len(self.node.sightseeing) * (500 * (self.installed_probe.gen + 3))


            case ProbeType.BOOSTER:
                miranium = self.node.prod_rank.value[1] * 0.10
                credits = self.node.rev_rank.value[1] * 0.10


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


            case ProbeType.STORAGE:
                miranium = self.node.prod_rank.value[1] * 0.10
                credits = self.node.rev_rank.value[1] * 0.10
                storage = 3000

            case ProbeType.COMBAT:
                miranium = self.node.prod_rank.value[1] * 0.10
                credits = self.node.rev_rank.value[1] * 0.10

            case ProbeType.LOCKED:
                return 0, 0, 0, []

            case __:
                pass

        return miranium, credits, storage, precious_resources

    def _apply_booster_effect(self, miranium, credits, storage):
        # If any adjacent nodes are installed with Booster Probes
        # that bonus is calculated into the output here
        if self.installed_probe.probe_type != ProbeType.BOOSTER and \
            self.installed_probe.probe_type != ProbeType.BASIC and \
            self.installed_probe.probe_type != ProbeType.COMBAT and \
            self.installed_probe.probe_type != ProbeType.LOCKED:
            adjacent_nodes = self.node.get_adjacent_nodes()

            for adj_node in adjacent_nodes:
                if adj_node in ProbeSlot.node_to_slot:
                    adj_slot = ProbeSlot.node_to_slot[adj_node]
                    if adj_slot.installed_probe.probe_type == ProbeType.BOOSTER:

                        self.installed_probe.boosted = adj_slot.installed_probe.gen

                        if self.installed_probe.boosted == 1:
                            if self.installed_probe.probe_type == ProbeType.MINING:
                                miranium += miranium * 0.5
                            elif self.installed_probe.probe_type == ProbeType.RESEARCH:
                                credits += credits * 0.5
                            elif self.installed_probe.probe_type == ProbeType.STORAGE:
                                storage += storage * 0.5
                            elif self.installed_probe.probe_type == ProbeType.DUPLICATOR:
                                types = self._duplicator_copied_types()
                                for type in types:
                                    if type == ProbeType.MINING:
                                        miranium += miranium * 0.5
                                    elif type == ProbeType.RESEARCH:
                                        credits += credits * 0.5
                                    elif type == ProbeType.STORAGE:
                                        storage += storage * 0.5

                            
                        elif self.installed_probe.boosted == 2:
                            if self.installed_probe.probe_type == ProbeType.MINING:
                                miranium += miranium * 1.0
                            elif self.installed_probe.probe_type == ProbeType.RESEARCH:
                                credits += credits * 1.0
                            elif self.installed_probe.probe_type == ProbeType.STORAGE:
                                storage += storage * 1.0
                            elif self.installed_probe.probe_type == ProbeType.DUPLICATOR:
                                types = self._duplicator_copied_types
                                for type in types:
                                    if type == ProbeType.MINING:
                                        miranium += miranium * 1.0
                                    elif type == ProbeType.RESEARCH:
                                        credits += credits * 1.0
                                    elif type == ProbeType.STORAGE:
                                        storage += storage * 1.0
                            
            self.installed_probe.boosted = 0

        return miranium, credits, storage
    
    
    def _calculate_links_multiplier(self):
        same = set()
        queue = [self.node]
        visited_nodes = {self.node}

        current_probe = self.installed_probe
        if not current_probe or current_probe.probe_type is None or current_probe.probe_type is ProbeType.LOCKED:
            return 0
        
        starting_probe_type = current_probe.probe_type
        starting_probe_gen = current_probe.gen
        
        while queue:
            current_node = queue.pop(0)

            if current_node.probe_slot.installed_probe.probe_type == starting_probe_type and current_node.probe_slot.installed_probe.gen == starting_probe_gen:
                same.add(current_node)

                adjacent_nodes = current_node.get_adjacent_nodes()
                if adjacent_nodes:
                    for adj_node in adjacent_nodes:
                        if adj_node not in visited_nodes:
                            visited_nodes.add(adj_node)
                            queue.append(adj_node)         

        links = len(same)
        if links >= 8:
            return 1.8
        elif links >= 5:
            return 1.5
        elif links >= 3:
            return 1.3
        else:
            return 1

    
    
    def _apply_link_multiplier(self, miranium, credits, storage):
        # If a probe is of a type that recieves a link multiplier from adjacent prodes of the same type and gen
        # that bonus is used to calculate the final output here

        match self.installed_probe.probe_type:
            case ProbeType.MINING | ProbeType.RESEARCH | ProbeType.DUPLICATOR | ProbeType.STORAGE:
                link_multiplier = self._calculate_links_multiplier()
                dupe_multiplier = self._duplicator_link_boost()

            case __:
                pass

        match self.installed_probe.probe_type:
            case ProbeType.MINING:
                miranium = miranium * link_multiplier * dupe_multiplier
            case ProbeType.RESEARCH:
                credits = credits * link_multiplier * dupe_multiplier
            case ProbeType.STORAGE:
                storage = storage * link_multiplier * dupe_multiplier
            case ProbeType.DUPLICATOR:
                pass

        return miranium, credits, storage
    
    def _duplicator_copied_types(self):
        adjacent_probes = self.get_adjacent_probes()
        copied_types = []
        for adj_probe in adjacent_probes:
            if adj_probe.probe_type != ProbeType.DUPLICATOR:
                copied_types.append(adj_probe.probe_type)
        return copied_types

    def _duplicator_link_boost(self):
        if self.installed_probe.probe_type != ProbeType.DUPLICATOR:
            adjacent_nodes = self.node.get_adjacent_nodes()
            dupe_link_boost = 1
            for adj_node in adjacent_nodes:
                if adj_node.probe_slot.installed_probe.probe_type == ProbeType.DUPLICATOR:
                    boost = adj_node.probe_slot._calculate_links_multiplier()
                    if boost > dupe_link_boost:
                        dupe_link_boost = boost
            return dupe_link_boost