import argparse
import os
import sys
import time
import profile
import math

# Command line arguments
parser=argparse.ArgumentParser(description='Calculate the nearest two points on a plan')
parser.add_argument('--algorithm',default='a',\
    help='Algorithm: Select the algorithm to run, default is all. (a)ll, (b)ruteforce only or (d)ivide and conquer only')
parser.add_argument('-v','--verbose',action='store_true')
parser.add_argument('--profile',action='store_true')
parser.add_argument('filename',metavar='<filename>',\
    help='Input dataset of points')

#Calculates distance between two points using Euclidean distance equation
#Input: two points
#output: distance of the two points
def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
#end def distance(point1, point2):

#Divide and conquer version of the nearest neighbor algorithm
#Input: points := unsorted array of (x,y) coordinates
#Output: tuple of smallest distance and coordinates (distance,(x1,y1),(x2,y2))
def divideAndConquerNearestNeighbor(points):
    # TODO: Complete this function
    sort_x = sorted(points, key=lambda x: x[0])

    print("Divide and Conquer algorithm is complete")
    return findNearestNeighbor(sort_x, sort_x)
#end def divide_and_conquer(points):

#Helper function for 'divideAndConquerNearestNeighbor(points)'
#Divide and conquer version of the nearest neighbor algorithm
#Input: points := sorted arrays in x and y coordinates
#Return: tuple of smallest distance and coordinates (distance,(x1,y1),(x2,y2))
def findNearestNeighbor(px, py):
    num_px = len(px)
    if num_px <= 3:
        return recallBruteForce(px)

    mid = num_px // 2
    Left_x = px[:mid]
    Right_x = px[mid:]
    midpoint = px[mid][0]
    Left_y = list()
    Right_y = list()

    for i in py:
        if i[0] <= midpoint:
           Left_y.append(i)
        else:
           Right_y.append(i)
    (point1_L, point2_L, minimum_distance_L) = findNearestNeighbor(Left_x, Left_y)
    (point1_R, point2_R, minimum_distance_R) = findNearestNeighbor(Right_x, Right_y)

    if minimum_distance_L <= minimum_distance_R:
        current_min_d = minimum_distance_L
        closest_pts = (point1_L, point2_L)
    else:
        current_min_d = minimum_distance_R
        closest_pts = (point1_R, point2_R)
    (point1_M, point2_M, minimum_distance_M) = checkMiddle(px, py, current_min_d, closest_pts)

    if current_min_d <= minimum_distance_M:
        return closest_pts[0], closest_pts[1], current_min_d
    else:
        return point1_M, point2_M, minimum_distance_M
#end def findNearestNeighbor(px, py):

#Helper function for 'divideAndConquerNearestNeighbor(points)'
#Checks mid section if there are closer points that crosses the half line
#Input: points := sorted arrays in x and y coordinates
def checkMiddle(px, py, c, closest_pts):
    num_x = len(px)
    mid_x = px[num_x // 2][0]
    sorted_y = [x for x in py if mid_x - c <= x[0] <= mid_x + c]
    closest = c
    num_y = len(sorted_y)

    for i in range(num_y - 1):
        for j in range(i+1, min(i + 7, num_y)):
            pt1, pt2 = sorted_y[i], sorted_y[j]
            dist = distance(pt1, pt2)
            if dist < closest:
                closest_pts = pt1, pt2
                closest = dist
    return closest_pts[0], closest_pts[1], closest
#end def checkMiddle(px, py, c, closest_pts):

#Helper function for 'divideAndConquerNearestNeighbor(points)'
#Brute force version of the nearest neighbor algorithm
#Input: points := unsorted array of (x,y) coordinates
#   [(x,y),(x,y),...,(x,y)]
#Output: tuple of smallest distance and coordinates (distance,(x1,y1),(x2,y2))
def recallBruteForce(points):
    minimum_distance = distance(points[0], points[1])
    point1 = points[0]
    point2 = points[1]
    num_points = len(points)

    if num_points == 2:
        return point1, point2, minimum_distance
    else:
        for i in range(num_points - 1):
            for j in range(i + 1, num_points):
                if i != 0 and j != 1:
                    temp = distance(points[i], points[j])
                    if temp < minimum_distance:
                        minimum_distance = temp
                        point1, point2 = points[i], points[j]
    return (point1, point2, minimum_distance)
#end def recallBruteForce(points):

#Brute force version of the nearest neighbor algorithm
#Input: points := unsorted array of (x,y) coordinates 
#   [(x,y),(x,y),...,(x,y)]
#Output: tuple of smallest distance and coordinates (distance,(x1,y1),(x2,y2))
def bruteForceNearestNeighbor(points):
    # TODO: Complete this function
    minimum_distance = distance(points[0], points[1])
    point1 = points[0]
    point2 = points[1]
    num_points = len(points)

    if num_points == 2:
        return point1, point2, minimum_distance
    else:
        for i in range(num_points - 1):
            for j in range(i + 1, num_points):
                if i != 0 and j != 1:
                    temp = distance(points[i], points[j])
                    if temp < minimum_distance:
                        minimum_distance = temp
                        point1, point2 = points[i], points[j]
    print("Brute force algorithm is complete")
    return (point1, point2, minimum_distance)
#end def brute_force_nearest_neighbor(points):

#Parse the input file
#Input: filename := string of the name of the test case
#Output: points := unsorted array of (x,y) coordinates
#   [(x,y),(x,y),...,(x,y)]
def parseFile(filename):
    points = []
    f = open(filename,'r') 
    lines = f.readlines()
    for line in lines:
        coordinate = line.split(' ')
        points.append((float(coordinate[0]),float(coordinate[1])))
    return points
#end def parse_file(filename):

#Main
#Input: filename  := string of the name of the test case
#       algorithm := flag for the algorithm to run, 'a': all 'b': brute force, 'd': d and c
def main(filename,algorithm):
    points = parseFile(filename)
    result = bruteForceResult = divideAndConquerResult = None
    if algorithm == 'a' or algorithm == 'b':
        #TODO: Insert timing code here
        start_time = time.time()
        bruteForceResult = bruteForceNearestNeighbor(points)
        print("<<%s seconds>>" % (time.time() - start_time))
    if algorithm == 'a' or algorithm == 'd':
        #TODO: Insert timing code here
        start_time = time.time()
        divideAndConquerResult = divideAndConquerNearestNeighbor(points)
        print("<<%s seconds>>" % (time.time() - start_time))
    if algorithm == 'a': # Print whether the results are equal (check)
        if args.verbose:
            print('Brute force result: '+str(bruteForceResult))
            print('Divide and conquer result: '+str(divideAndConquerResult))
            print('Algorithms produce the same result? '+str(bruteForceResult == divideAndConquerResult))
        result = bruteForceResult if bruteForceResult == divideAndConquerResult else ('Error','N/A','N/A')
    else:  
        result = bruteForceResult if bruteForceResult is not None else divideAndConquerResult
    with open(os.path.splitext(filename)[0]+'_distance.txt','w') as f:
        f.write(str(result[0])+'\n')
        f.write(str(result[1])+'\n')
        f.write(str(result[2])+'\n')
#end def main(filename,algorithm):

if __name__ == '__main__':
    args=parser.parse_args()
    main(args.filename,args.algorithm)
#end if __name__ == '__main__':
