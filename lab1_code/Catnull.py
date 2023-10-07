"""
Author: Johnson
Time：2023-09-29 10:55
"""

from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np
import sys
import time


def center_point(p1, p2):
    cp = []
    for i in range(3):
        cp.append((p1[i] + p2[i]) / 2)

    return cp


def sum_point(p1, p2):
    sp = []
    for i in range(3):
        sp.append(p1[i] + p2[i])

    return sp


def div_point(p, d):

    sp = []
    for i in range(3):
        sp.append(p[i] / d)

    return sp


def mul_point(p, m):
    sp = []
    for i in range(3):
        sp.append(p[i] * m)

    return sp


def get_face_points(input_points, input_faces):
    # 3 dimensional space

    NUM_DIMENSIONS = 3

    # face_points will have one point for each face

    face_points = []

    for curr_face in input_faces:
        face_point = [0.0, 0.0, 0.0]
        for curr_point_index in curr_face:
            curr_point = input_points[curr_point_index]
            # add curr_point to face_point
            # will divide later
            for i in range(NUM_DIMENSIONS):
                face_point[i] += curr_point[i]
        # divide by number of points for average
        num_points = len(curr_face)
        for i in range(NUM_DIMENSIONS):
            face_point[i] /= num_points
        face_points.append(face_point)

    return face_points


def get_edges_faces(input_points, input_faces):

    # will have [pointnum_1, pointnum_2, facenum]

    edges = []

    # get edges from each face

    for facenum in range(len(input_faces)):
        face = input_faces[facenum]  # 对于每个面
        num_points = len(face)    # 这个面有n个顶点
        # loop over index into face
        for pointindex in range(num_points):
            # if not last point then edge is curr point and next point
            if pointindex < num_points - 1:
                pointnum_1 = face[pointindex]
                pointnum_2 = face[pointindex + 1]
            else:
                # for last point edge is curr point and first point
                pointnum_1 = face[pointindex]
                pointnum_2 = face[0]
            # order points in edge by lowest point number
            if pointnum_1 > pointnum_2:
                temp = pointnum_1
                pointnum_1 = pointnum_2
                pointnum_2 = temp
            edges.append([pointnum_1, pointnum_2, facenum])

    # sort edges by pointnum_1, pointnum_2, facenum

    edges = sorted(edges)

    # merge edges with 2 adjacent faces
    # [pointnum_1, pointnum_2, facenum_1, facenum_2] or
    # [pointnum_1, pointnum_2, facenum_1, None]

    num_edges = len(edges)
    eindex = 0
    merged_edges = []

    while eindex < num_edges:
        e1 = edges[eindex]
        # check if not last edge
        if eindex < num_edges - 1:
            e2 = edges[eindex + 1]
            if e1[0] == e2[0] and e1[1] == e2[1]:
                merged_edges.append([e1[0], e1[1], e1[2], e2[2]])
                eindex += 2
            else:
                merged_edges.append([e1[0], e1[1], e1[2], None])
                eindex += 1
        else:
            merged_edges.append([e1[0], e1[1], e1[2], None])
            eindex += 1

    # add edge centers

    edges_centers = []

    for me in merged_edges:
        p1 = input_points[me[0]]
        p2 = input_points[me[1]]
        cp = center_point(p1, p2)
        edges_centers.append(me + [cp])

    return edges_centers


def get_edge_points(input_points, edges_faces, face_points):

    edge_points = []

    for edge in edges_faces:
        # get center of edge
        cp = edge[4]
        # get center of two facepoints
        fp1 = face_points[edge[2]]
        # if not two faces just use one facepoint
        # should not happen for solid like a cube
        if edge[3] == None:
            fp2 = fp1
        else:
            fp2 = face_points[edge[3]]
        cfp = center_point(fp1, fp2)
        # get average between center of edge and
        # center of facepoints
        edge_point = center_point(cp, cfp)
        edge_points.append(edge_point)

    return edge_points


def get_avg_face_points(input_points, input_faces, face_points):

    # initialize list with [[0.0, 0.0, 0.0], 0]

    num_points = len(input_points)

    temp_points = []

    for pointnum in range(num_points):
        temp_points.append([[0.0, 0.0, 0.0], 0])

    # loop through faces updating temp_points

    for facenum in range(len(input_faces)):
        fp = face_points[facenum]
        for pointnum in input_faces[facenum]:
            tp = temp_points[pointnum][0]
            temp_points[pointnum][0] = sum_point(tp, fp)
            temp_points[pointnum][1] += 1
#以上统计每个点属于多少个面，并将每个面点求和，在接下来求平均
    # divide to create avg_face_points

    avg_face_points = []

    for tp in temp_points:
        afp = div_point(tp[0], tp[1])
        avg_face_points.append(afp)

    return avg_face_points


def get_avg_mid_edges(input_points, edges_faces):

    # initialize list with [[0.0, 0.0, 0.0], 0]

    num_points = len(input_points)

    temp_points = []

    for pointnum in range(num_points):
        temp_points.append([[0.0, 0.0, 0.0], 0])

    # go through edges_faces using center updating each point

    for edge in edges_faces:
        cp = edge[4]
        for pointnum in [edge[0], edge[1]]:
            tp = temp_points[pointnum][0]
            temp_points[pointnum][0] = sum_point(tp, cp)
            temp_points[pointnum][1] += 1

    # divide out number of points to get average

    avg_mid_edges = []

    for tp in temp_points:
        ame = div_point(tp[0], tp[1])
        avg_mid_edges.append(ame)

    return avg_mid_edges


def get_points_faces(input_points, input_faces):

    num_points = len(input_points)

    points_faces = []

    for pointnum in range(num_points):
        points_faces.append(0)

    for facenum in range(len(input_faces)):
        for pointnum in input_faces[facenum]:
            points_faces[pointnum] += 1

    return points_faces
#统计每个点属于多少个面

def get_new_points(input_points, points_faces, avg_face_points, avg_mid_edges):
    """
    m1 = (n - 3.0) / n
    m2 = 1.0 / n
    m3 = 2.0 / n
    new_coords = (m1 * old_coords)
               + (m2 * avg_face_points)
               + (m3 * avg_mid_edges)
    """

    new_points = []

    for pointnum in range(len(input_points)):
        n = points_faces[pointnum]
        m1 = (n - 3.0) / n
        m2 = 1.0 / n
        m3 = 2.0 / n
        old_coords = input_points[pointnum]
        p1 = mul_point(old_coords, m1)
        afp = avg_face_points[pointnum]
        p2 = mul_point(afp, m2)
        ame = avg_mid_edges[pointnum]
        p3 = mul_point(ame, m3)
        p4 = sum_point(p1, p2)
        new_coords = sum_point(p4, p3)

        new_points.append(new_coords)

    return new_points


def switch_nums(point_nums):

    if point_nums[0] < point_nums[1]:
        return point_nums
    else:
        return (point_nums[1], point_nums[0])


def cmc_subdiv(input_points, input_faces):
    # 1. for each face, a face point is created which is the average of all the points of the face.
    # each entry in the returned list is a point (x, y, z).

    face_points = get_face_points(input_points, input_faces)

    # get list of edges with 1 or 2 adjacent faces
    # [pointnum_1, pointnum_2, facenum_1, facenum_2, center] or
    # [pointnum_1, pointnum_2, facenum_1, None, center]

    edges_faces = get_edges_faces(input_points, input_faces)

    # get edge points, a list of points

    edge_points = get_edge_points(input_points, edges_faces, face_points)

    # the average of the face points of the faces the point belongs to (avg_face_points)

    avg_face_points = get_avg_face_points(input_points, input_faces, face_points)

    # the average of the centers of edges the point belongs to (avg_mid_edges)

    avg_mid_edges = get_avg_mid_edges(input_points, edges_faces)

    # how many faces a point belongs to

    points_faces = get_points_faces(input_points, input_faces)

    """

    m1 = (n - 3) / n
    m2 = 1 / n
    m3 = 2 / n
    new_coords = (m1 * old_coords)
               + (m2 * avg_face_points)
               + (m3 * avg_mid_edges)

    """

    new_points = get_new_points(input_points, points_faces, avg_face_points, avg_mid_edges)



    # add face points to new_points

    face_point_nums = []

    # point num after next append to new_points
    next_pointnum = len(new_points)

    for face_point in face_points:
        new_points.append(face_point)
        face_point_nums.append(next_pointnum)
        next_pointnum += 1

    # add edge points to new_points

    edge_point_nums = dict()

    for edgenum in range(len(edges_faces)):
        pointnum_1 = edges_faces[edgenum][0]
        pointnum_2 = edges_faces[edgenum][1]
        edge_point = edge_points[edgenum]
        new_points.append(edge_point)
        edge_point_nums[(pointnum_1, pointnum_2)] = next_pointnum
        next_pointnum += 1



    new_faces = []

    for oldfacenum in range(len(input_faces)):
        oldface = input_faces[oldfacenum]
        # 4 point face
        if len(oldface) == 4:
            a = oldface[0]
            b = oldface[1]
            c = oldface[2]
            d = oldface[3]
            face_point_abcd = face_point_nums[oldfacenum]
            edge_point_ab = edge_point_nums[switch_nums((a, b))]
            edge_point_da = edge_point_nums[switch_nums((d, a))]
            edge_point_bc = edge_point_nums[switch_nums((b, c))]
            edge_point_cd = edge_point_nums[switch_nums((c, d))]
            new_faces.append((a, edge_point_ab, face_point_abcd, edge_point_da))
            new_faces.append((b, edge_point_bc, face_point_abcd, edge_point_ab))
            new_faces.append((c, edge_point_cd, face_point_abcd, edge_point_bc))
            new_faces.append((d, edge_point_da, face_point_abcd, edge_point_cd))

    return new_points, new_faces


def graph_output(output_points, output_faces, fig):

    ax = fig.add_subplot(111, projection='3d')



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
    # cube

    input_points = [
        [-1.0, 1.0, 1.0],
        [-1.0, -1.0, 1.0],
        [1.0, -1.0, 1.0],
        [1.0, 1.0, 1.0],
        [1.0, -1.0, -1.0],
        [1.0, 1.0, -1.0],
        [-1.0, -1.0, -1.0],
        [-1.0, 1.0, -1.0]
    ]

    input_faces = [
        [0, 1, 2, 3],
        [3, 2, 4, 5],
        [5, 4, 6, 7],
        [7, 0, 3, 5],
        [7, 6, 1, 0],
        [6, 1, 2, 4],
    ]

    iterations = 4

    plt.ion()
    output_points, output_faces = input_points, input_faces

    fig = plt.figure(1)
    plt.clf()
    graph_output(input_points, input_faces, fig)
    plt.pause(0.2)
    print("output points:")
    for p in output_points:
        print(p)

    for i in range(iterations):
        output_points, output_faces = cmc_subdiv(output_points, output_faces)
        print("output points:")
        for p in output_points:
            print(p)
        fig = plt.figure(1)
        plt.clf()
        graph_output(output_points, output_faces, fig)
        plt.pause(0.2)



