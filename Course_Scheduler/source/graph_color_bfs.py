# CS473 Group Eagles final project - Aaron Borjas, Connor Weldy, Jorjei Ngoche
# 12/2/2022 CS473 adv algorithms, Dr. Kent Jones
# This file does the graph coloring using breadth first search for our project
from course import *

#BUDGETED COLORING -> possible solution:
#1. Use breadth first search and prioritize coloring of higher-degree neighbors.
#2. in coloring, we can know minimum number of necessary time slots based on # classes & # rooms 
#   -> x classes / y rooms = z timeslots (minimum number of timeslots).
#3. create a list of numbers that is length of z, with indeces being timeslots and 
#   values being number of rooms currently used in that timeslot. 
#4. increment value of list for timeslot with the least number of rooms used...
#   e.g. initially 4 timeslots [0 0 0 0] -> [1 0 0 0] -> ... -> 
#   [1 1 1 0] (in this one, choose last index) -> [1 1 1 1] -> etc

# assigns the course to a room based on the room assignments of other classes (basically greedy coloring)
# inputs - current course class that doesn't have a room assigned, number of rooms available, 
#          number of rooms available in total as an integer, and a list of neighbors to the course
# outputs - no return values but sets the room value of the current course (colors it)
# average time complexity: O(1), where V is the # of adjacent vertices worse case is O(V)
def set_timeslot_and_room(current_course, num_avail_timeslots, rooms_used, number_rooms_available):
    neighbor_timeslots = current_course.get_neighbor_timeslots() # get_neighbor_timeslots() returns a set of timeslots

    # gets next available timelost that is not used by a neighbor course and that hasn't been used a max number of times
    for timeslot in range(1,num_avail_timeslots+1):
        # check how many times timeslot has been used
        # number_of_times(timeslot) < rooms_available:
        if (timeslot not in neighbor_timeslots) and (rooms_used[timeslot-1] < number_rooms_available): #avg case O(1), worse case O(V) efficiency (hashing collisions)
            current_course.set_timeslot(timeslot)
            current_course.set_room(rooms_used[timeslot-1])
            rooms_used[timeslot-1] += 1
            break # gets lowest available timeslot
    

# create_graph_coloring_greedy function - colors a graph using a greedy algorithm. uses https://iq.opengenus.org/graph-colouring-greedy-algorithm/ as a reference
# input: an dictionary adjacency list representation of a graph, where the vertices are classes and edges are incompatibilities. 
#        e.g. c1---c2 means c1 and c2 can't be at the same time
#        input graph will just be a list of course objects, which have a member variable
#           that contains all neighbors
#        later we can implement stuff like time slots available and rooms available
# output: returns a set of Courses, with all items having the color assigned using graph
#           coloring methods.
def create_graph_coloring_greedy(adj_list, num_avail_timeslots, num_rooms):
        
    rooms_used = [0]*num_avail_timeslots #index is timeslot, value is number of rooms used

    # Color first vertex with first color
    # Repeat following for V-1 times:
    # - consider the currently picked vertex
    # - color it with lowest numbered color not used by previously colored vertices adjacent to it
    # - if all previously used colors appear on vertices adjacent to v, assign a new color it
    
    '''
    PSEUDO CODE
    bfs approach - bfs to find nodes to color then separate color checker for adj to node n

    add first node to queue
    for course in list:
        check if course is colored, if not then add to queue
        while queue
            course = pop(0)
            if course no room
                # get neighbor rooms
                # choose lowest numbered room available
                # adding neigbors to queue that arent colored and not already in queue
    
    '''
    #graph coloring with BFS
    #adj_list[0].set_room(1)
    bfs_queue = []
    visited = set()

    #AVERAGE CASE BFS: V + E
    for course in adj_list: #make sure we cover all the courses -> O(V) if fully disconnected
        if course.get_room() == -1: # if course does not have a room yet
            bfs_queue.append(course) # add to end of queue
        while bfs_queue: #while the queue isnt empty -> O(V) if fully connected
            #print(f"queue: {bfs_queue}")
            current_course = bfs_queue.pop(0) # get first course from queue
            visited.add(current_course)
            if current_course.get_timeslot() == -1: # if course does not have a room yet
                      
                # Set the room to the course
                set_timeslot_and_room(current_course, num_avail_timeslots, rooms_used, num_rooms) # for last node this is O(v^2) but for all previous nodes it is less than that
                # Add neighbor nodes that don't have a room
                #O(E)
                for neighbor_course in current_course.get_neighbors():
                    #add the neighbor_course to the queue if the course isn't in the queue
                    #and if the course has not been visited yet.
                    if (neighbor_course not in bfs_queue) and (neighbor_course not in visited): # not in bfs queue O(n) n is size of bfs queue; not in visited is O(n) n is size of visited; THESE BOTH HAPPEN 2 *E TIMES
                        bfs_queue.append(neighbor_course)
