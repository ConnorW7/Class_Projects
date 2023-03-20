#graph coloring by coloring the high-degree nodes first
#12/13/2022 by Aaron Borjas, Connor Weldy, Jorjei Ngoche
#CS473 adv. algorithms, Dr. Kent Jones
from graph_color_bfs import set_timeslot_and_room

#sort courses in descending order based on number of constraints [c w/ more constraints, ... c w/ less constraints]
#both worst case and average case efficiency is O(nlogn) so that's pretty neat
#   https://en.wikipedia.org/wiki/Timsort, https://www.geeksforgeeks.org/timsort/
def sort_on_constraints(courses):
    #timsort, which is a combination of mergesort and insertion sort and is O(nlogn)
    return sorted(courses, key=lambda x: -len(x.get_neighbors())) 

#creates a graph coloring by starting at the highest degree vertices and navigating down
#inputs - a list of courses (NOT sorted), integer number of available timeslots, and integer number of rooms 
#outputs - no output, but changes timeslot and room values for the classes
#Worse case: O(V*n+VlogV)
def create_graph_coloring_degree(courses, num_avail_timeslots, num_rooms):
    sorted_courses_list = sort_on_constraints(courses) #courses sorted on degree in descending order O(vlogv)
    rooms_used = [0]*num_avail_timeslots #index is timeslot, value is number of rooms used
    for current_course in sorted_courses_list: #make sure we cover all the courses -> O(V) if fully disconnected
        # Get rooms of neighbors:
        set_timeslot_and_room(current_course, num_avail_timeslots, rooms_used, num_rooms) # for last node this is O(v^2) but for all previous nodes it is less than that
