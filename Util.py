import xlrd
import xlwt
import pandas as pd
import numpy as np
#from Node import Node
#from Graph import Graph
import math


def read_excel(file, graph):
    df = pd.read_excel(file, index_col=0, header=1)
    end_node = df.tail(1)
    end_loc = (end_node.iat[0, 0], end_node.iat[0, 1], end_node.iat[0, 2])
    graph.set_end_node(end_loc)
    for index, row in df.iterrows():
        graph.add_node(index, (row[0], row[1], row[2]), row[3], row[4])
    return graph


def write_excel(file, ans):
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet('result1', cell_overwrite_ok=True)
    sheet.write(0, 0, 'index')
    sheet.write(0, 1, 'ang1')
    sheet.write(0, 2, 'ang2')
    i = 1
    for index, step_dist in ans:
        sheet.write(i, 0, index)
        sheet.write(i, 1, step_dist[1])
        sheet.write(i, 2, step_dist[2])
        i += 1
    book.save(file)


def module(v):
    return np.sqrt(sum(np.power(v, 2)))


def cos_ang(v1, v2):
    return v1.dot(v2)/(module(v1)*module(v2))
    return np.sqrt(1 - cos_ang**2)


def distance(loc1, loc2):
    return np.sqrt(sum(np.power(np.array(loc1) - np.array(loc2), 2)))


def distance_p2(parent_loc, loc, next_loc):
    r = 200
    v1 = np.array(loc) - np.array(parent_loc)
    v2 = np.array(next_loc) - np.array(loc)
    d1 = module(v2)
    ang = math.acos(cos_ang(v1, v2))
    sin_ang1 = (1 + cos_ang(v1, v2))/2
    ang1 = math.asin(sin_ang1)
    min_dist = r*math.sqrt(1 - cos_ang(v1, v2)**2) + 2*r*math.sqrt(1 - sin_ang1**2)
    new_dist = (ang + math.pi - 2*ang1)*r
    if d1 <min_dist:
        return -1, 0, 0
    else:
        return d1 - min_dist + new_dist, ang + math.pi/2 - ang1, math.pi/2 - ang1


def take_second(elem):
    return elem[1]


if __name__ == '__main__':
    loc1 = (0, 0, 0)
    loc2 = (16612.273, 46538.567, 9942.567)
    a, b = (1, 2)
    print(b)
    #print(distance(loc1, loc2))
