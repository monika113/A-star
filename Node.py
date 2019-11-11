import numpy as np
from Util import *


class Node:
    def __init__(self, index, loc, type, end_loc, mistake):
        self.index = index
        self.loc = loc
        self.type = type
        if type == 1:
            self.type = 'V'
        if type == 0:
            self.type = 'H'
        if type == 'A点' or type == 'A 点':
            self.type = 'A'
        if type == 'B点' or type == 'B 点':
            self.type = 'B'
        if mistake == 1:
            self.mistake = True
        else:
            self.mistake = False
        self.neighbors = []
        #A-star
        self.h = distance(self.loc, end_loc)
        self.g = 0
        self.f = self.h
        self.parent = 0
        self.v_error = 0
        self.h_error = 0
        self.new_dist = 0
        self.ang1 = 0
        self.ang2 = 0
        self.searched = False

    def update_g(self, tmp_g, index, tmp_v_error, tmp_h_error, para, new_dist, ang1, ang2):
        self.g = tmp_g
        self.f = self.h + self.g * para
        self.parent = index
        self.v_error = tmp_v_error
        self.h_error = tmp_h_error
        self.new_dist = new_dist
        self.ang1 = ang1
        self.ang2 = ang2

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)

    def sort_neighbor(self):
        self.neighbors.sort(key=take_second, reverse=True)

    def clear(self):
        self.g = 0
        self.f = self.h
        self.parent = 0
        self.v_error = 0
        self.h_error = 0
        self.searched = False
        self.new_dist = 0
        self.ang1 = 0
        self.ang2 = 0

