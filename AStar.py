from Util import *
from Graph import Graph


class AStar:
    def __init__(self, alpha1, alpha2, beta1, beta2, theta, delta, problem, penalty):
        self.graph = Graph()
        self.alpha1 = alpha1
        self.alpha2 = alpha2
        self.beta1 = beta1
        self.beta2 = beta2
        self.theta = theta
        self.delta = delta
        self.problem = problem
        self.ans = []
        self.ans_num = 0
        self.ans_dist = 0
        self.penalty = penalty

    def get_graph(self, file):
        read_excel(file, self.graph)
        self.graph.get_neighbors(min(self.alpha1, self.alpha2) / self.delta, min(self.beta1, self.beta2) / self.delta, self.theta / self.delta)

    def clear(self):
        self.graph.clear()
        self.ans = []
        self.ans_num = 0
        self.ans_dist = 0
    #A-star

    def cal_dist(self, parent_node, node):
        if self.problem == 2:
            if parent_node.type == 'A':
                return distance(parent_node.loc, node.loc), 0, 0
            else:
                pre_node = self.graph.node_dict[parent_node.parent]
                return distance_p2(pre_node.loc, parent_node.loc, node.loc)
        else:
            return distance(parent_node.loc, node.loc), 0, 0

    def trace_back(self, index):
        self.ans = []
        node_dict = self.graph.node_dict
        ang1 = 0
        ang2 = 0
        self.ans_dist = 0
        while node_dict[index].type != 'A':
            self.ans.append((index, (node_dict[index].new_dist, ang1, ang2)))
            self.ans_dist += node_dict[index].new_dist
            ang1 = node_dict[index].ang1
            ang2 = node_dict[index].ang2
            index = node_dict[index].parent
        self.ans.append((index, (0, 0, 0)))
        '''
        parent_index = node_dict[index].parent
        self.ans_dist = 0
        while node_dict[parent_index].type != 'A':
            dist, _, _= self.cal_dist(node_dict[parent_index], node_dict[index])
            self.ans_dist += dist
            self.ans.append((index, dist))
            index = parent_index
            parent_index = node_dict[index].parent
        dist = self.cal_dist(node_dict[parent_index], node_dict[index])
        self.ans_dist += dist[0]
        self.ans.append((index, dist))
        self.ans.append((parent_index, (0, 0, 0)))
        '''
        self.ans.reverse()
        self.ans_num = len(self.ans)

    def trace_false(self, index):
        path = [index]
        while self.graph.node_dict[index].type != 'A':
            index = self.graph.node_dict[index].parent
            path.append(index)
        path.reverse()
        print(path)

    def cal_g(self, v_error, h_error, tmp_v_error, tmp_h_error, variance):
        return tmp_v_error - v_error + tmp_h_error - h_error + variance * self.penalty

    def sort_by_f(self, elem):
        return self.graph.node_dict[elem].f

    def cal_error(self, v_error, h_error, neighbor_type, dist):
        v_error = v_error + dist * self.delta
        h_error = h_error + dist * self.delta
        variance = 0
        if neighbor_type == 'B':
            if not (v_error <= self.theta and h_error <= self.theta):
                v_error = -1
        if neighbor_type == 'V':
            if v_error > self.alpha1 or h_error > self.alpha2:
                v_error = -1
            else:
                if self.problem != 3:
                    v_error = 0
                else:
                    v_error = 0.2*min(v_error, 5)
                    variance = 0.4*min(v_error, 5)
        if neighbor_type == 'H':
            if v_error > self.beta1 or h_error > self.beta2:
                v_error = -1
            else:
                if self.problem != 3:
                    h_error = 0
                else:
                    h_error = 0.2*min(h_error, 5)
                    variance = 0.4*min(h_error, 5)
        return v_error, h_error, variance

    def a_star(self, index, open_list, para):
        if self.graph.node_dict[index].type == 'B':
            self.trace_back(index)
            return True
        self.graph.node_dict[index].searched = True
        open_list.remove(index)
        node = self.graph.node_dict[index]
        for (neighbor_index, neighbor_dist) in node.neighbors:
            neighbor_node = self.graph.node_dict[neighbor_index]
            if neighbor_node.searched:
                continue
            ang1 = 0
            ang2 = 0
            if self.problem == 2:
                neighbor_dist, ang1, ang2 = self.cal_dist(node, neighbor_node)
            if neighbor_dist < 0:
                continue
            tmp_v_error, tmp_h_error, variance = self.cal_error(node.v_error, node.h_error, neighbor_node.type, neighbor_dist)
            if tmp_v_error >= 0:
                tmp_g = self.cal_g(node.v_error, node.h_error, tmp_v_error, tmp_h_error, variance)
                if neighbor_index in open_list:
                    if neighbor_node.g < tmp_g:
                        self.graph.node_dict[neighbor_index].update_g(tmp_g, index, tmp_v_error, tmp_h_error, para, neighbor_dist, ang1, ang2)
                else:
                    self.graph.node_dict[neighbor_index].update_g(tmp_g, index, tmp_v_error, tmp_h_error, para, neighbor_dist, ang1, ang2)
                    open_list.append(neighbor_index)
        open_list.sort(key=self.sort_by_f)
        for neighbor_index in open_list:
            if self.a_star(neighbor_index, open_list, para):
                return True
            #else:
                #self.trace_false(index)
        self.graph.node_dict[index].searched = False
        return False

    def print_result(self):
        print('num: %d, distance: %.3f' % (self.ans_num, self.ans_dist))
        for index, step_dist in self.ans:
            node = self.graph.node_dict[index]
            if self.problem == 1:
                print("index : %d, type: %s, loc: (%.3f, %.3f, %.3f), dist: %.3f, error: (%.3f, %.3f)"
                      % (index, node.type, node.loc[0], node.loc[1], node.loc[2], step_dist[0], node.v_error, node.h_error))

            if self.problem == 2:
                print("index : %d, type: %s, loc: (%.3f, %.3f, %.3f), dist: %.3f, ang1: %.3f, ang2: %.3f, error: (%.3f, %.3f)"
                      % (index, node.type, node.loc[0], node.loc[1], node.loc[2], step_dist[0], step_dist[1], step_dist[2], node.v_error, node.h_error))
            if self.problem == 3:
                print("index : %d, type: %s, mistake: %s, loc: (%.3f, %.3f, %.3f), dist: %.3f, error: (%.3f, %.3f)"
                      % (index, node.type, node.mistake, node.loc[0], node.loc[1], node.loc[2], step_dist[0], node.v_error, node.h_error))

        if self.problem == 3:
            self.problem = 1
            cur_pro = [((0, 0), 1)]
            new_pro = []
            for index, step_dist in self.ans:
                if index == 0:
                    continue
                new_pro.clear()
                if not self.graph.node_dict[index].mistake:
                    for stat in cur_pro:
                        v_error, h_error, _ = self.cal_error(stat[0][0], stat[0][1], self.graph.node_dict[index].type, step_dist[0])
                        if v_error >= 0:
                            new_pro.append(((v_error, h_error), stat[1]))
                else:
                    for stat in cur_pro:
                        v_error, h_error, _ = self.cal_error(stat[0][0], stat[0][1], self.graph.node_dict[index].type,
                                                             step_dist[0])
                        if v_error >= 0:
                            new_pro.append(((v_error, h_error), stat[1]*0.8))
                            v_error = stat[0][0] + step_dist[0] * self.delta
                            h_error = stat[0][1] + step_dist[0] * self.delta
                            if self.graph.node_dict[index].type == 'V':
                                new_pro.append(((min(v_error, 5), h_error), stat[1] * 0.2))
                            if self.graph.node_dict[index].type == 'H':
                                new_pro.append(((v_error, min(h_error, 5)), stat[1] * 0.2))
                cur_pro = new_pro.copy()
                #print(cur_pro)
            suc_pro = 0
            for stat in cur_pro:
                suc_pro += stat[1]
            self.problem = 3
            print('success rate: %.3f ' % (suc_pro*100))
