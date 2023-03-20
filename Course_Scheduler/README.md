# __Class Scheduling with Graph Coloring__
Final Project Group Eagles

Aaron Borjas, Connor Weldy, Jorjei Ngoche

Last edited - December 13, 2022

CS473 Advanced Algorithms Design and Analysis, Dr. Kent Jones

# Project Description

The goal of this project was to create a generic class scheduling algorithm for a department. In our situation, we based inputs on the Mathematics and Computer Science department from Whitworth University. We wanted to have an algorithm that could help analyze various limits in resources, particularly those listed below.

At a base level, we wanted to consider timeslots available, rooms available, the number of professors, and the number of classes. Using this input we could build an algorithm to solve the graph coloring problem - graph coloring. In this approach, vertices are unique sections of all courses and edges between two vertices means that those two sections cannot be taught at the same time. We also call edges "constraints" in our documentation, which you may notice elsewhere. Then, colors represent different timeslots and each node of a certain color means different rooms used in that timeslot So, if we have 3 colors that means that the courses provided fit into 3 timeslots. Graph coloring is typically done by coloring connected vertices different colors. If there is an edge between two vertices, V1 and V2, they would have to be different colors. 

We used two variations of graph coloring algorithms, one which was "greedy" and based on Breadth First Search, and another which was based on the degree of vertices. The BFS-based algorithm is our greedy approach, because we navigate our way through the graph using BFS and color nodes based on the first color not used by their neighbors. In our degree-based method, we sort the nodes based on their degree (the number of edges of a vertex) and then color the highest-degree node(s) first, since this will eliminate certain colors from consideration for more nodes.

We decided to focus on creating an efficient but generic algorithm that could easily be expanded to help professors and the registrar schedule classes. After a lot of brainstorming and design we decided this method would allow the most versatility in expansion, making this project more practical for real world use. For the scope of this project, we created a generic scheduling algorithm that doesn't considered professor preferences. Below is high-level flow chart for how we conceptualized and implemented code for the university scheduling problem.
![Shows High-Level Flow Diagram Diagram](./img/high_level_project_flow_diagram.png?raw=true)

# Assumptions
The scheduling problem is infamously complex. We decided to make several assumptions to simplify the project overall to make it more feasible with the allotted time. Below are assumptions we made while designing our project.
* Users have enough knowledge to be able to run the program using VScode or the python command line.
* All classes repeat the same number of times on every weekday. We did not really consider the timing of classes, such as different schedules for Monday/Wednesday/Friday compared to Tuesday/Thursday classes. We leave that up to the available timeslots of the department or university.
* We assumed that professors are unavailable to teach more than one class at a time, since professors cannot be in two places at once.
* We also assumed that sections of one class cannot be at the same time. For example, Computer Science I in our input data occurs four times, and our algorithm treats each section as unique.
* Every professor can teach every class. This is not accurate as professors in real-world situations have preferences or certain levels of expertise in different topics, but we assumed this is not the case and that anybody can teach any class, distributing classes as such.
* Professors do not have time slot preferences. Realistically, some professors prefer morning classes whereas others prefer afternoon/evening classes, but in this case that does not happen. Sort of a consequence of assumption 2.
* Not all classrooms have to be used at the same time. This seems a bit intuitive for real-world situations, but it would be unrealistic for classrooms to require a class for our algorithm to function. 
* Classes require timeslots for the algorithm to "work". The algorithm will function if this is not the case, but realistically if classes do not have a timeslot, there is/are a constraint(s) that is preventing the configuration from working correctly.

# How to run the program

To run this program, you will need all of the files in /final-project/source/ outside of the pycache folder. In addition, a csv of planned classes, including all sections of a course, is required. For an example, please see __Math Draft Schedule 22-23.csv__ or __CS Draft Schedule 22-23.csv__. At the very least, we require columns titled "Course", "Professor", and "Semester", since our input processing handles these cases. When you have these .csv files prepared and in the ./final-project/ directory, you will need to select "main.py" and execute it. We require python 3 at the very least, but recommend the latest version of python. On a mac, this can be run in the terminal on VSCode by running something similar to "/usr/local/bin/python3 "__path to project location__/final-project/source/main.py". When main is ran by python, that is it! You have run the project.

# Pseudocode Design of Algorithms

## Greedy BFS-Based Algorithm
BFS to find nodes to color, then separate color checker for nodes adjacent to node n.

    def graph_color_greedy(list_of_courses, num_timeslots, num_rooms)
        rooms_used = [0]*num_timeslots  # list tracks how many rooms are used per timeslot
        initialize visited set
        initialize queue
        add first node to queue
        "color" first node with first timeslot
        for curr_course in list_of_courses: # makes sure all nodes go through queue
            check if curr_course has timeslot, if not then add to queue
            add curr_course to visited set
            while queue not empty
                course = queue.pop(0)
                if course has no timeslot assigned
                    get neighbor courses timeslots
                    #choose lowest numbered timeslot and room available not in neighbor timeslots
                    set_timeslot_and_room(course, num_timeslots, rooms_used, num_rooms)
                    add neigbors to queue that have not been visited or are not already in queue

## Degree-Based Algorithm
Uses python's Timsort (O(Vlog_2(V)) to sort vertices on degree (number of constraints per vertex) in descending order (most degree -> lowest degree), then colors the nodes in that order based on neighbor nodes' colors.

    def graph_color_degree(list, num_timeslots, num_rooms)
        sorted_courses_list = sort list on len(list item neighbors), order = descending
        rooms_used = [0]*num_timeslots
        for curr_course in sorted_courses_list
            set_timeslot_and_room(curr_course, num_timeslots, rooms_used, num_rooms)

## Important helper function: set_timeslot_and_room
This function works in constant time (average case) based on the number of timeslots available and neighbors of the current node to set the timeslot (color) of the node. Essentially this gets the next available timeslot not used by neighbors and that still has a room available for that timeslot.

    def set_timeslot_and_room(course, num_timeslots, rooms_used, num_rooms)
        neighbor_timeslots = neighbors of course
        for timeslot in num_timeslots
            if timeslot not in neighbor_timeslots and rooms_used[timeslot] < num_rooms
                set course timeslot (color)
                set course room
                increment the room count in rooms_used[timeslot]
                break




# Algorithm Analysis - Doubling Method
## 1. Estimate Runtime Hypothesis using worst/average case

* V: Vertices represent courses.
* E: Edges connect two courses that can't be scheduled at the same time (1 edge = 1 constraint).
* Colors - unique timeslots

Greedy-bfs-based coloring: O(V + E)

Degree-based coloring: O(V + VlogV)

## 2. Perform Emprical Tests
### Empirical speeds (N inputs)
Inputs and Constraints:
* 21 courses (vertices)
* 5 professors - implicitly 84 course neighbors (edges)
* 11 available time slots (constraint)
* 10 available rooms per time slot (constraint)

Greedy-bfs-based coloring: 0.0000770092 seconds => 77.0 microseconds

Degree-based coloring: 0.0000438690 seconds => 43.8 microseconds

### Empirical speeds (2N inputs)
Inputs and Constraints:
* 42 courses (vertices)
* 10 professors - implicitly 152 course neighbors (edges)
* 11 available time slots (constraint)
* 10 available rooms per time slot (constraint)
  
We doubled the number of classes and professors available. Some overlap in constraints produced less edges than if we had just doubled the number of edges explicitly (e.g. professors cannot teach more than one class during one timeslot, sections of one course cannot be in the same timeslot).

Greedy-bfs-based coloring: 0.0001511574 => 151.1 microseconds

Degree-based coloring: 0.0000860691 => 86.07 microseconds

## 3. Confirm/Disprove Your Hypothesis
### Greedy Method Empirical Ratio

151.1 microseconds / 77.0 microseconds = __1.96__

### Degree Method Empirical Ratio

86.07 microseconds / 43.8 microseconds = __1.97__

### Hypothetical Ratios

Greedy-bfs-based coloring: O(V+E)

(2V+2E)/(V+E) = __2__

Degree-based coloring: Average Case: O(V + VlogV)

(2V + 2Vlog2V)/(V + VlogV) = __2__

### __Final analysis, hypothesis confirmation__
Greedy empirical ratio is about equal to the hypothetical ratio: __1.96 ~= 2__

Degree-based empirical ratio is about equal to the hypothetical ratio: __1.97 ~= 2__


# Works Cited

1. (course_constrainer.py) How to distribute list values evenly in a list - https://stackoverflow.com/questions/53144723/python-evenly-distribute-value-to-a-list-in-a-dictionary  
2. (course.py) How to print a list of user-defined objects - https://stackoverflow.com/questions/12933964/printing-a-list-of-objects-of-user-defined-class
3. (graph_color_degree.py) Details on timsort, the method used in python's default sorted() method: https://en.wikipedia.org/wiki/Timsort, https://www.geeksforgeeks.org/timsort/
4. (graph_color_bfs.py) Referenced this to start working on BFS-based greedy graph coloring https://iq.opengenus.org/graph-colouring-greedy-algorithm/