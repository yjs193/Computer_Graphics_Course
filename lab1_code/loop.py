"""
Author: Johnson
Time：2023-09-29 14:24
"""
from matplotlib import pyplot as plt
import numpy as np

# 函数构建

# 输入的坐标点的下标进行前后大小调整
def adjust_position(pointnum1, pointnum2):
    if pointnum1 > pointnum2:
        v = pointnum1
        pointnum1 = pointnum2
        pointnum2 = v

    return pointnum1, pointnum2


# 新边点计算公式1
def new_edge_point1(input_point, pointnum):
    point0 = input_point[pointnum[0]]
    point1 = input_point[pointnum[1]]
    edge_point_x = np.average([point0[0], point1[0]])
    edge_point_y = np.average([point0[1], point1[1]])
    edge_point_z = np.average([point0[2], point1[2]])
    return [edge_point_x, edge_point_y, edge_point_z]


# 新边点计算公式2
def new_edge_point2(input_point, pointnum):
    point0 = input_point[pointnum[0]]
    point1 = input_point[pointnum[1]]
    point2 = input_point[pointnum[2]]
    point3 = input_point[pointnum[3]]
    edge_point_x = 3 / 8 * (point0[0] + point1[0]) + 1 / 8 * (point2[0] + point3[0])
    edge_point_y = 3 / 8 * (point0[1] + point1[1]) + 1 / 8 * (point2[1] + point3[1])
    edge_point_z = 3 / 8 * (point0[2] + point1[2]) + 1 / 8 * (point2[2] + point3[2])
    return [edge_point_x, edge_point_y, edge_point_z]


# 寻找面上的另一点
def find_point(input_face, pointnum):
    for i in input_face:
        if i == pointnum[0] or i == pointnum[1]:
            continue
        else:
            return i


# 获取新边点
def get_edge_point(input_point, input_face):
    n1 = len(input_face)  # 多面体面的数量

    # 1. [point1, point2, face1]
    edge1 = []
    for facenum in range(n1):
        m1 = len(input_face[facenum])
        face = input_face[facenum]  # 把下标对应的面取出来
        for pointnum in range(m1):
            if pointnum + 1 < m1:
                pointnum1 = face[pointnum]
                pointnum2 = face[pointnum + 1]
                pointnum1, pointnum2 = adjust_position(pointnum1, pointnum2)  # adjust_position 调整下标的位置，小的下标在前，大的下标在后
            else:
                pointnum1 = face[pointnum]
                pointnum2 = face[0]
                pointnum1, pointnum2 = adjust_position(pointnum1, pointnum2)
            edge1.append([pointnum1, pointnum2, facenum])

    # 2. [point1, point2, face1, face2]
    edge2 = []
    edge1_new = sorted(edge1)
    n2 = len(edge1_new)
    edgenum = 0  # edge1_new 的下标

    while edgenum < n2:
        if edgenum + 1 < n2:
            edge_1 = edge1_new[edgenum]
            edge_2 = edge1_new[edgenum + 1]
            if edge_1[0] == edge_2[0] and edge_1[1] == edge_2[1]:
                edge2.append([edge_1[0], edge_1[1], edge_1[2], edge_2[2]])
                edgenum += 2
            else:
                edge2.append([edge_1[0], edge_1[1], edge_1[2], None])
                edgenum += 1
        else:
            edge_1 = edge1_new[edgenum]
            edge2.append([edge_1[0], edge_1[1], edge_1[2], None])
            edgenum += 1

    # 3. [point1, point2, face1, face2, edge_point]
    n3 = len(edge2)
    edge3 = []
    edge_point = []

    for edgenum in range(n3):
        edge = edge2[edgenum]
        # 一条边只有一个邻接面时的边点计算调用 new_edge_point1 函数
        if edge[3] == None:
            #             print(2)
            pointnum = [edge[0], edge[1]]
            new_edge_point = new_edge_point1(input_point, pointnum)
        # 一条边有2个及2个以上邻接面时的边点计算调用 new_edge_point2 函数
        else:
            #             print(1)
            pointnum = [edge[0], edge[1]]
            # 寻找面上除了边的两个端点外的另一个点
            for i in range(2):
                facenum = edge[i + 2]
                pointnum1 = find_point(input_face[facenum], [edge[0], edge[1]])
                pointnum.append(pointnum1)
            new_edge_point = new_edge_point2(input_point, pointnum)
        #         print(new_edge_point)
        edge.append(new_edge_point)
        #         print(edge)
        edge3.append(edge)
        #         print(edge3)
        edge_point.append(new_edge_point)

    return edge3, edge_point


# 计算n
def get_n(input_point, input_face):
    m1 = len(input_point)
    m2 = len(input_face)
    ad_point = []  # 顶点的邻接点
    n = []  # 邻接面的数量
    for i in range(m1):
        n1 = []
        n2 = 0
        for face in input_face:
            if i in face:
                #                 face.remove(i)
                #                 n1 = n1+face
                '''此处做过修改，注释的地方行不通，不知道是为啥，讲道理应该一样'''
                for j in face:
                    if j != i:
                        n1.append(j)
                n2 += 1
            else:
                continue
        n1 = list(set(n1))
        ad_point.append(n1)
        n.append(n2)

    return ad_point, n


# 计算β
def get_beta(n):
    beta = 1 / n * (5 / 8 - np.power(3 / 8 + 1 / 4 * np.cos(2 * np.pi / n), 2))
    return beta


# 内部新顶点更新1
def new_point1(input_point, pointnum_v0, v0_ad, beta, n):
    #     print(1)
    vi_x = []
    vi_y = []
    vi_z = []
    for i in range(n):
        pointnum_vi = v0_ad[i]
        vi = input_point[pointnum_vi]
        vi_x.append(vi[0])
        vi_y.append(vi[1])
        vi_z.append(vi[2])
    v0 = input_point[pointnum_v0]
    v_x = (1 - n * beta) * v0[0] + beta * sum(vi_x)
    v_y = (1 - n * beta) * v0[1] + beta * sum(vi_y)
    v_z = (1 - n * beta) * v0[2] + beta * sum(vi_z)
    return [v_x, v_y, v_z]


# 边界新顶点更新2
def new_point2(input_point, pointnum_v0, pointlist):
    vi_x = []
    vi_y = []
    vi_z = []

    n = len(pointlist)
    for i in range(n):
        pointnum_vi = pointlist[i]
        vi = input_point[pointnum_vi]
        vi_x.append(vi[0])
        vi_y.append(vi[1])
        vi_z.append(vi[2])
    v0 = input_point[pointnum_v0]
    v_x = 3 / 4 * v0[0] + 1 / 8 * sum(vi_x)
    v_y = 3 / 4 * v0[1] + 1 / 8 * sum(vi_y)
    v_z = 3 / 4 * v0[2] + 1 / 8 * sum(vi_z)

    return [v_x, v_y, v_z]


# 获取新顶点
def get_point(input_point, input_face, edge3):
    # 计算邻接点 ad_point 以及邻接点数量 n
    ad_point, n = get_n(input_point, input_face)

    m1 = len(input_point)  # m1 为旧顶点的个数
    new_point = []  # 存储新顶点的坐标
    for pointnum in range(m1):
        # 第pointnum个顶点
        # v0 = input_point[pointnum]

        # 该顶点的邻接顶点的下标
        v0_ad = ad_point[pointnum]

        # 该顶点的邻接点数量
        n1 = n[pointnum]

        # 计算该顶点的beta
        beta = get_beta(n1)

        # 判断顶点是边界点还是内部点  # False代表内部点，True代表外部点
        # 默认顶点为内部点
        '''
            根据v0以及ad_point邻接点来选取线段，
            并通过判断线段是否只邻接一个面来选择顶点更新的方法
        '''
        position_bol = False
        pointlist = []  # 用于存储只有一个邻接面的边
        for v0_ad_num in v0_ad:
            #             print('v0={0},v0_ad={1}'.format(pointnum,v0_ad_num))
            pointnum1, pointnum2 = adjust_position(pointnum, v0_ad_num)
            #             print('v1={0},v2={1}\n'.format(pointnum1,pointnum2))
            for edge in edge3:
                #                 print(edge)
                if pointnum1 == edge[0] and pointnum2 == edge[1]:
                    #                     print('step1')
                    # 如果边只邻接一个面，则修改position_bol，并将边添加到pointlist中
                    if None in edge:
                        #                         print('step2')
                        position_bol = True
                        pointlist.append(v0_ad_num)

        # 计算新顶点
        if position_bol:
            #             print(pointlist)
            #             print(2)
            v = new_point2(input_point, pointnum, pointlist)
        else:
            #             print(1)
            #             print(v0_ad)
            v = new_point1(input_point, pointnum, v0_ad, beta, n1)
        new_point.append(v)

    return new_point


def loop_subdiv(input_point, input_face):
    # 计算新边点
    '''
    edge3的返回形式
        [pointnum1, pointnum2, face1, face2, edge_point1]
        [pointnum1, pointnum2, face1, None, edge_point1]
    并且下标  pointnum1 < pointnum2

    edge_point1的形式为
        [point_x, point_y, point_z]

    edge_point的返回形式
        [[point_x, point_y, point_y],..]
    '''
    edge3, edge_point = get_edge_point(input_point, input_face)
    #     print(edge3)

    # 计算新顶点
    '''
        new_point的返回形式
        [[point_x, point_y, point_y],..]
    '''
    new_point = get_point(input_point, input_face, edge3)

    # 输出新的顶点列表 output_point

    output_point = new_point
    n1 = len(new_point)  # 新边点存储至新顶点列表的第一个点的下标
    m1 = len(edge_point)  # 新边点的个数
    edge_point_num = dict()  # 使用字典的形式存储边点的下标
    for edgenum in range(m1):
        edge = edge3[edgenum]
        #         print(edge)
        pointnum1 = edge[0]
        pointnum2 = edge[1]
        output_point.append(edge[4])
        edge_point_num[(pointnum1, pointnum2)] = n1
        n1 += 1

    # 输出新的面列表 output_face

    '''
    一个面可以生成四个面
    for a quad face (a,b,c):
       (a, edge_point ab, edge_point ca)
       (b, edge_point bc, edge_point ab)
       (c, edge_point ca, edge_point bc)
       (edge_point ab, edge_point bc, edge_point ca)
    '''
    n2 = len(input_face)  # 输入面的数量
    output_face = []
    for facenum in range(n2):
        face = input_face[facenum]
        a = face[0]
        b = face[1]
        c = face[2]
        edge_point_ab = edge_point_num[adjust_position(a, b)]
        edge_point_bc = edge_point_num[adjust_position(b, c)]
        edge_point_ca = edge_point_num[adjust_position(c, a)]
        output_face.append([a, edge_point_ab, edge_point_ca])
        output_face.append([b, edge_point_ab, edge_point_bc])
        output_face.append([c, edge_point_ca, edge_point_bc])
        output_face.append([edge_point_ab, edge_point_bc, edge_point_ca])

    return output_point, output_face


def graph_output(output_points, output_faces, fig, m):
    ax = fig.add_subplot(111, projection='3d')

    """
    Plot each face
    """
    ax.set_title('{0}次细分'.format(str(m)), fontsize=18)
    for facenum in range(len(output_faces)):
        curr_face = output_faces[facenum]
        xcurr = []
        ycurr = []
        zcurr = []
        for pointnum in range(len(curr_face)):
            xcurr.append(output_points[curr_face[pointnum]][0])
            ycurr.append(output_points[curr_face[pointnum]][1])
            zcurr.append(output_points[curr_face[pointnum]][2])
        xcurr.append(output_points[curr_face[0]][0])
        ycurr.append(output_points[curr_face[0]][1])
        zcurr.append(output_points[curr_face[0]][2])
        ax.plot(xcurr, ycurr, zcurr, color='b')


if __name__ == '__main__':
    # 参数输入

    # 锥体
    input_point = [
        [-1.0, 1.0, 1.0],
        #[-1.0, -1.0, 1.0],
        [1.0, -1.0, 1.0],
        #[1.0, 1.0, 1.0],
        #[1.0, -1.0, -1.0],
        [1.0, 1.0, -1.0],
        [-1.0, -1.0, -1.0],
        #[-1.0, 1.0, -1.0]
    ]

    input_face = [
        [0, 3, 1],
        [0, 3, 2],
        [0, 2, 1],
        [3, 2, 1],
    ]

    # 正方体
    # input_point = [[10.0, 10.0, 10.0], [-10.0, 10.0, 10.0], [10.0, -10.0, 10.0], [-10.0, -10.0, 10.0],
    #                [10.0, 10.0, -10.0], [-10.0, 10.0, -10.0], [10.0, -10.0, -10.0], [-10.0, -10.0, -10.0]]
    # input_face = [
    #     [0,1,3],
    #     [0,2,3],
    #     [0,1,5],
    #     [0,4,5],
    #     [0,2,4],
    #     [1,3,7],
    #     [1,5,7],
    #     [3,2,7],
    #     [6,2,7],
    #     [6,2,4],
    #     [4,6,7],
    #     [4,5,7],
    # ]

    # # 曲面
    # input_point = [
    #     [1.0, 0.0, 0.0],
    #     [2.0, 1.0, 0.0],
    #     [1.0, 1.0, 0.0],
    #     [0.0, 0.6, 1.0]
    # ]
    #
    # input_face = [
    #     [0, 1, 2],
    #     [0, 2, 3]
    # ]

    iterations = 4
    plt.ion()  # 维持多张图展示，不因为plt.show()而停止展示
    output_points, output_faces = input_point, input_face
    fig = plt.figure(1, figsize=(10, 8))
    plt.clf()
    graph_output(output_points, output_faces, fig, 0)
    plt.pause(1)

    for i in range(iterations):
        output_points, output_faces = loop_subdiv(output_points, output_faces)
        # print(output_points)
        # print(output_faces)
        fig = plt.figure(1, figsize=(10, 8))
        plt.clf()
        graph_output(output_points, output_faces, fig, i + 1)
        plt.pause(1)



