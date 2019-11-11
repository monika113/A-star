import numpy as np
from Util import *
from Node import Node


class Graph:
    def __init__(self):
        self.node_dict = {}
        self.node_num = 0
        self.end_loc = (0, 0, 0)

    def set_end_node(self, loc):
        self.end_loc = loc

    def add_node(self, index, loc, type, mistake):
        node = Node(index, loc, type, self.end_loc, mistake)
        self.node_dict[index] = node
        self.node_num += 1

    def get_neighbors(self, v_thre, h_thre, thre):
        #print("start get neighbors")
        #num_neighbor = 0
        for index, node in self.node_dict.items():
            for neighbor_index, neighbor_node in self.node_dict.items():
                if index != neighbor_index and neighbor_index != 0:
                    dist = distance(node.loc, neighbor_node.loc)
                    if neighbor_node.type == 'V':
                        if dist <= v_thre:
                            node.add_neighbor((neighbor_index, dist))
                    if neighbor_node.type == 'H':
                        if dist <= h_thre:
                            node.add_neighbor((neighbor_index, dist))
                    if neighbor_node.type == 'B':
                        if dist <= thre:
                            node.add_neighbor((neighbor_index, dist))
            node.sort_neighbor()
            #num_neighbor += len(node.neighbors)
        #print(num_neighbor)
        #print(num_neighbor / self.node_num)

    def clear(self):
        for _, node in self.node_dict.items():
            node.clear()




