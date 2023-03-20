# CS473 Adv. Algorithms Final Project Group Eagles
# Aaron Borjas, Connor Weldy, Jorjei Ngoche
# In this project, we are aiming to complete a scheduling problem using graph coloring. In our situation, we are aiming to schedule classes for
# a single department of a university. We consider professors, classes, classrooms, and timeslots to complete this problem. 
# using sample data from Nate Moyer for CS 2023-2024 school year...
# Last edited: 12/13/2022

import math
import random
import pandas as pd
from graph_color_bfs import *
from graph_color_degree import *
from course import *
from course_constrainer import *
import time

# Reading in File
cs_draft_schedule = pd.read_csv('CS Draft Schedule 22-23.csv')
#cs_draft_schedule = pd.read_csv('Double CS Draft Schedule 22-23.csv')

# Processing Data via Pandas
fall_draft_schedule = cs_draft_schedule.loc[cs_draft_schedule['Semester'] == 'Fall']
fall_courses = fall_draft_schedule['Course']
fall_profs = list(fall_draft_schedule['Professor'].unique()) # list
fall_profs.remove('STAFF')

# Creating course constrainer object
course_constr = Course_Constrainer()

# Add courses to course constrainer from data
for i in range(fall_courses.shape[0]): # for every row in fall_courses
    c_id = f'C{i+1}' # Course Id
    c_name = fall_courses.iloc[i] # Get value at index location i in fall_courses dataframe
    course_constr.add_course(c_id, c_name) # Adding course to course constrainer
course_constr.add_profs(fall_profs) #implicit constrait - profs can't teach two courses at once
course_constr.add_same_course_constraints() #implicit constraint - sections of course can't be taught at same time

#course_constr.add_profs(["Dr.J", "QM", "PT", "SG", "MB"]) # extra professors for doubling method
course_list = course_constr.gen_graph() # Generates graph (constraints are defined)

# Testing how many edges there are (defined by how many neighbors each course has)
#count = 0 
#for c in course_list:
#    print(f"{c.course_id} - {c.get_neighbors()}")
#    count+= len(c.get_neighbors())
#print(f"COUNT: {count}")  

num_timeslots = 5 #5 total timeslots available for teachers to teach
num_rooms = 5 #5 total rooms available for each timeslot
#in total, we have num_rooms*num_timeslots rooms available in total. If we notice
#that the number total input classes is greater than num_rooms * num_timeslots,
#the problem is considered "unsolvable"

#===============================GREEDY GRAPH COLORING SECTION================================
start_time = time.time()
create_graph_coloring_greedy(course_list, num_timeslots, num_rooms) #graph coloring with 3 time slots, 2 rooms
greedy_time = time.time() - start_time
#print(f"=======\greedy time: {format(greedy_time, '.10f')}\n========")

### OUTPUT
# Translating course objects into lists
course_table_greedy = []
for course in course_list:
    id = course.get_course_id()
    name = course.get_name()
    prof = course.get_professor()
    my_time = course.get_timeslot()
    room = course.get_room()
    course_table_greedy.append([id, name, prof, my_time, room]) # adding lists togther to create table
output_df_greedy = pd.DataFrame(course_table_greedy) # Passing table into pandas.DataFrame object for nice output :)
output_df_greedy.columns = ['Course', 'Name', 'Professor', 'Timeslot', 'Room'] # setting columns
print(output_df_greedy.sort_values(by='Timeslot')) # sorting table by timeslot
print(f"===============================\ngreedy-based time: {format(greedy_time, '.10f')}\n===============================")

#===============================DEGREE GRAPH COLORING SECTION================================
start_time = time.time()
create_graph_coloring_degree(course_list, num_timeslots, num_rooms)
degree_time = time.time() - start_time
#print(f"=======\ndegree time: {format(degree_time, '.10f')}\n========")

### OUTPUT 
# reference Greedy method output above
course_table = []
for course in course_list:
    id = course.get_course_id()
    name = course.get_name()
    prof = course.get_professor()
    my_time = course.get_timeslot()
    room = course.get_room()
    course_table.append([id, name, prof, my_time, room])
output_df = pd.DataFrame(course_table)
output_df.columns = ['Course', 'Name', 'Professor', 'Timeslot', 'Room']
print(output_df.sort_values(by='Timeslot'))
print(f"===============================\ndegree-based time: {format(degree_time, '.10f')}\n===============================")

'''
#Example from diagrams
course_constr = Course_Constrainer()
course_constr.add_courses(['C1','C4','C7','C2','C5','C8','C3','C6'])
profs = ['P1', 'P2', 'P3']
class_constraints = [('C1', 'C4'), ('C2', 'C7'), ('C6', 'C8'), ('C1', 'C8')]
course_constr.add_profs(profs)
course_constr.add_course_constraints(class_constraints)
course_list = course_constr.gen_graph() #a normal list of courses, e.g. [c1, c2, ..., c_n]
#create graph coloring with x = adj list of courses, 3 = num avail timeslots, 2 = num avail rooms
#create_graph_coloring_greedy(course_list, 3, 2) #graph color with limited number of timeslots
create_graph_coloring_degree(course_list, 5, 10)
'''

'''
SCRATCH WORK
CS Department:

Profs: Kent Jones, Qian Mao, Scott Griffith, Matt Bell, Pete Tucker (5 total)
Classes (fall): 
    CS125 x2, CS171 x4, CS172 x1, CS200 x1, CS273 x2, CS274 x1, CS278 x1, CS313 x1, 
    CS333 x1, CS344 x1, CS359 x1, CS370 x1, CS373 x1, CS374 x1, CS471 x1, CS473 x1
    21 total classes in the fall
Classes (spring): 
    CS125 x2, CS171 x2, CS172 x2, CS251 x1, CS273 x1, CS274 x1, CS278 x1, CS314 x1,
    CS374 x1, CS375 x1, CS378 x1, CS401 x1, CS457 x1, CS472 x1, CS475 x1
    18 total classes offered in the spring
Time slots (fall): 
    MWF - 8-8:55am, 9:05-10am, 10:25-11:20am, 11:45am-12:40pm, 12:50-1:45pm (5 timeslots)
    TTh - 8-9:20am, 9:30-10:50am, 12:50-2:10pm, 4-6pm, 6-6:55pm (5 timeslots)
Time slots (spring):
    MWF - 8-8:55am, 9:05-10am, 10:25am-11:20am, 11:45am-12:40pm, 12:50-1:45pm, 1:55-2:10pm, 6:30-9pm (7 timeslots)
    TTH - 8-9:20am, 9:30-10:50am, 12:50-2:10pm, 2:20-3:40pm (4 timeslots)

    Methods:
    1. Total time slots -> treat timeslots from TTh as unique timeslots on mwf (e.g. 8am mwf != 8am Tth)
    2. subset -> divide into separate MWF and TTh days

Math Department
Profs: Kelsey Marcinko, Lindy Moyer, Martha Gady, Diana Schepens, Jordan Broussard, Nate Moyer, Immanual Manohar,
       Molly Lamb, Steve Gady, Lyle Cochran (10 total)
Classes (fall): 
    MA/CS294, MA/CS499, MA107 x2, MA108 x2, MA130, MA150 x2, MA171 x4, MA172 x2, MA221, MA222, MA256 x2,
    MA273 x2, MA278, MA281, MA306, MA330, MA357, MA410
Classes (spring): 
    MA107, MA108, MA130, MA150, MA158, MA171 x2, MA172 x3, MA221, MA222, MA256 x3, MA273, MA278, MA281, 
    MA330, MA350, MA358, MA365, MA411, MA430
Time slots (fall):
    MWF - 8-8:55am, 9:05-10am, 10:25-11:20am, 11:45am-12:40pm, 12:50-1:45pm, 1:55-2:50pm (6 timeslots)
    TTH - 8-9:20am, 9:30-10:50am (2 timeslots)
Time slots (spring):
    MWF - 8-8:55am, 9:05-10am, 10:25-11:20am, 11:45am-12:40pm, 12:50-1:45pm, 1:55-2:50pm (6 timeslots)
    TTH - 8-9:20am, 9:30-10:50am (2 timeslots)
'''