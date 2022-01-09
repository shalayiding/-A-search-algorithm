#!/usr/bin/python
import sys
from PIL import Image
import math
import numpy as np

G_W = 395
G_H = 500

#run : 
#python3 lab1_done.py terrain.png mpp.txt brown.txt redOut.png


# terrain type
terraintype_set = {(248, 148, 18): 1.5, #Open land
                   (255, 192, 0): 0.25, #Rough meadow
                   (255, 255, 255): 1.1,#Easy movement forest
                   (2, 208, 60): 0.95,#Slow run forest
                   (2, 136, 40): 0.75, #Walk forest
                   (5, 73, 24): 0.000001, #Impassible vegetation
                   (0, 0, 255): 0.000001,#Lake/Swamp/Marsh
                   (71, 51, 3): 1.8, #Paved road
                   (0, 0, 0): 1.5,   #Footpath
                   (205, 0, 101): 0} #Out of bounds


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.gscore = float("inf") 
        self.hscore = 0
        self.fscore = float("inf")
        self.camefrom = None
        self.ele_value = 0  #get from matrix
        self.terrain_type = 0   #get from image pixel value
        self.distance = 0

def Makemap(terrain_matrix, row, col, ele_value_set):  # build the map
    map = []
    for i in range(row):
        tmp = []
        for j in range(col):
            obj = Point(i, j)
            obj.ele_value = ele_value_set[j][i]     #2d list swap i and j 
            type_key = tuple(terrain_matrix[j,i][:-1])      #2d list
            obj.terrain_type = terraintype_set[type_key]    #get type from hash table
            tmp.append(obj)
        map.append(tmp)
    return map


def Closepixles(point, map, width, height):  # get four different neighbour
    four_value = []
    if point.y+1 < height:
        four_value.append(map[point.x][point.y+1])  # down

    if point.y-1 > 0:
        four_value.append(map[point.x][point.y-1])  # up

    if point.x+1 < width:
        four_value.append(map[point.x+1][point.y])  # right

    if point.x-1 > 0:
        four_value.append(map[point.x-1][point.y])  # left

    return four_value


def Calc_Hscore(point_1, point_2):  # calculate H score
    x0, x1 = point_1.x, point_2.x
    y0, y1 = point_1.y, point_2.y
    z0, z1 = point_1.ele_value, point_2.ele_value
    return abs(x1-x0)+abs(y1-y0)+abs(z1-z0)  #consider ele as 3d distance


def Calc_Gscore(point_1,point_2):
    ele_diff = (point_1.ele_value - point_2.ele_value)*0.1
    if point_1.y == point_2.y:
        distance = 10.29
    else :
        distance = 7.55
    point_2.distance = distance
    return distance / (point_2.terrain_type + ele_diff)



def Astar(start, end, map): #A* 


    # set start and end point with object map
    start_point = map[start[0]][start[1]]
    end_point = map[end[0]][end[1]]

    
    # create visited and ready_to_visit q
    visited_point = {start_point}
    ready_to_visit = [start_point]
    

    # calculate the start point of the f,g,h scores
    start_point.gscore = 0      #start point is orginal
    start_point.fscore = start_point.gscore + Calc_Hscore(start_point, end_point)


    while len(ready_to_visit) != 0: #if the list is not empty

        #first find the smalleset Fscore from the buffer 
        min_value = float("inf")
        for point in ready_to_visit:
            if point.fscore < min_value:
                min_value = point.fscore
                start_point = point

        #check if we reach the end or not
        if start_point == end_point:
            path = []
            while start_point.camefrom: #while point is camefrom other point
                path.append(start_point)
                start_point = start_point.camefrom  #go to place where point is camefrom
            path.append(start_point)
            return path

        
       
       # print(start_point.x,start_point.y,start_point.gscore,start_point.hscore,start_point.fscore)
        
        ready_to_visit.remove(start_point)
        four_points = Closepixles(start_point, map, len(map), len(map[0]))  # find four neighbors
        four_tmp = []
        for point in four_points: #check to see if the any of the point is out of map 
            if point.terrain_type != 0:
                four_tmp.append(point)


        for point in four_tmp: #loop it from four_point value
            point.gscore = Calc_Gscore(start_point,point)
            point.hscore = Calc_Hscore(point, end_point)

            if point not in visited_point: 
                visited_point.add(point)
                if point in ready_to_visit: #if point is been visited or not
                    if point.hscore + point.gscore < point.fscore:
                        point.fscore = point.hscore + point.gscore
                        point.camefrom = start_point
                else:
                    point.fscore = point.hscore + point.gscore 
                    point.camefrom = start_point
                    ready_to_visit.append(point)

    return 


def Point_scaler(point,terrain_b_matrix): # make point bigger 
    terrain_b_matrix[point[0],point[1]] = (75,0,130)
    if point[0]+1 < G_W:
        terrain_b_matrix[point[0]+1,point[1]] = (75,0,130)
    if point[0]-1 > 0:
        terrain_b_matrix[point[0]-1,point[1]] = (75,0,130)
    if point[1]+1 < G_H:
        terrain_b_matrix[point[0],point[1]+1] = (75,0,130)
    if point[1]-1 > 0:
        terrain_b_matrix[point[0],point[1]-1] = (75,0,130)
   
    return 

def main(argv):

    if len(sys.argv) != 5:
        print("4 arguments is required")
        sys.exit()

    Input_eleva_matrix = []  # hold set of eleva set data
    path_data_set = []       #hold set of path


    
    with open(sys.argv[2]) as eleva_f:          #read from two file 
        Input_eleva_matrix = [[float(value) for value in (line.strip()).split()] for line in eleva_f]
    with open(sys.argv[3]) as path_file:
        path_data_set = [[int(value) for value in (line.strip()).split()] for line in path_file]

    
    terrain_img = Image.open(sys.argv[1])   
    terrain_matrix = np.asarray(terrain_img)
    terrain_b_matrix = terrain_img.load()       #plan B backup matrix 
    G_distance = 0
    
    for itr in range(len(path_data_set)-1):
        map = Makemap(terrain_matrix, G_W,G_H, Input_eleva_matrix)  #map to hold all object
        start,end = path_data_set[itr],path_data_set[itr+1] # set start point
        path = Astar(start, end, map)  # A* start with start end and map
        for p in path:  # write the path into image pixle
            x, y,distance = p.x, p.y,p.distance
            terrain_b_matrix[x, y] = (255, 0, 0)
            G_distance +=distance

        Point_scaler(start,terrain_b_matrix)
        Point_scaler(end,terrain_b_matrix)
    print("total distance is meter is : ", G_distance)
    terrain_img.save(sys.argv[4])

main(sys.argv[1:])
