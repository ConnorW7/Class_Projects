# course.py
# Aaron Borjas, Connor Weldy, Jorjei Ngoche
# helper class to organize our data in the scheduling/graph coloring final project
# Last edited: 12/13/2022

# Course class
class Course:
    def __init__(self, course_id='default course', c_name='default name'):
        self.course_id = course_id # str course id
        self.course_name = c_name # str course name
        self.professor = 'no professor' # str professor
        self.timeslot = -1 # int timeslot -> "the color" in the graph coloring algorithm
        self.room = -1 # room number
        self.neighbors = [] # list of classes that cannot be at the same time as the current instance
    
    #https://stackoverflow.com/questions/12933964/printing-a-list-of-objects-of-user-defined-class
    #useful for simplying printing lists of Courses. Stackoverflow explained this.
    def __repr__(self):
        return self.course_id
    
    #function for displaying information of a course
    def __str__(self):
        #return self.course_id
        return f"ID: {self.course_id}, Course: {self.course_name}, Prof: {self.professor}, Timeslot: {self.timeslot}, Room: {self.room}"
    
    #=========== various getters and setters ==============

    # add_neighbor(course)
    # Adds a neighbor course to neighbors list
    def add_neighbor(self, course):
        self.neighbors.append(course)
    
    # remove_neighbor(course)
    # removes a neighbor course from neighbors list
    def remove_neighbor(self,course):
        self.neighbors.remove(course)
    
    # clear_neighbors()
    # removes all neighbor courses from neighbors list
    def clear_neighbors(self):
        self.neighbors.clear()
    
    # set_professor(professor)
    # sets the professor of a course
    def set_professor(self, professor):
        self.professor = professor
    
    # get_professor()
    # returns the professor of the course
    def get_professor(self):
        return self.professor
    
    # set_timeslot()
    # sets the timeslot of a course
    def set_timeslot(self, time):
        self.timeslot = time

    # get_timeslot()
    # returns the timeslot of a course
    def get_timeslot(self):
        return self.timeslot

    # set_room()
    # sets the room of the course
    def set_room(self, room):
        self.room = room

    # get_room()
    # returns the room number of the course
    def get_room(self):
        return self.room
    
    # get_course_id()
    # returns the course_id of the course
    def get_course_id(self):
        return self.course_id

    # get_neighbors()
    # returns the list of neighbors
    def get_neighbors(self):
        return self.neighbors

    # get_name()
    # returns the name of the course
    def get_name(self):
        return self.course_name

    # get_neighbor_timeslots()
    # returns a set of timeslots of each of the neigbor course
    def get_neighbor_timeslots(self):
        neighbor_timeslots = set()
        for n in self.neighbors:
            neighbor_timeslots.add(n.timeslot)
        return neighbor_timeslots
        