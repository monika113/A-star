from Node import Node
from AStar import AStar
from Util import *

if __name__ == '__main__':
    data = 1
    problem = 3
    penalty = 0
    para = 1000
    if data == 1:
        file, alpha1, alpha2, beta1, beta2, theta = 'data1.xlsx', 25, 15, 20, 25, 30
    else:
        file, alpha1, alpha2, beta1, beta2, theta = 'data2.xlsx', 20, 10, 15, 20, 20
    delta = 0.001

    a_star = AStar(alpha1, alpha2, beta1, beta2, theta, delta, problem, penalty)
    a_star.get_graph(file)
    a_star.a_star(0, [0], para=para)
    a_star.print_result()
    #write_excel('result.xls', a_star.ans)
