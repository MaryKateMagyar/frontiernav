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

    def __repr__(self):
        return f"Connection({self.node1.name}, {self.node2.name})"

    def get_other_node(self, node):
        if node == self.node1:
            return self.node2
        elif node == self.node2:
            return self.node1
        else:
            raise ValueError(f"Node {node.name} is not part of this connection")

  