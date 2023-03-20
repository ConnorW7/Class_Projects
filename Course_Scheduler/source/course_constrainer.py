# course_constrainer.py
# Aaron Borjas, Connor Weldy, Jorjei Ngoche
# helper class to organize our data in the scheduling/graph coloring final project
# Last edited: 12/13/2022
# Course constrainer is ONLY to hold information for initialization of the graph/courses
# this class does not handle any of the graph coloring, it only
# generates the adjacency list which graph coloring uses.

from course import Course
import random

# course_constrainer class
class Course_Constrainer:
    def __init__ (self):
        self.course_list = [] #list of Courses
        self.prof_list = [] #list of strings
        self.course_constraints = [] #list of course constraints
    
    # add_course(course, name)
    # adds a single course with id=course and name=name to the object
    def add_course(self, course, name):
        self.course_list.append(Course(course, name))
    
    # add_courses(courses)
    # adds a list of courses to course_list
    # def add_courses(self, courses):
    #     for course in courses:
    #         self.add_course(course)

    # returns a course object based on name
    def get_course(self, course_name):
        for course in self.course_list:
            if course_name == course.course_id:
                return course

    # adds a signle professor to the course constrainer
    def add_prof(self, prof):
        self.prof_list.append(prof)
    
    # adds a list of professors to the course constrainer
    def add_profs(self, prof_list):
        for x in prof_list:
            self.add_prof(x)

    # adds a course constraint to the course_constraints list
    def add_course_constraint(self, pair): # pair: ('C1','C2')
        c1 = self.get_course(pair[0])
        c2 = self.get_course(pair[1])
        self.course_constraints.append((c1,c2))

    # adds a list of course constraints
    def add_course_constraints(self, constraint_list):
        for constraint in constraint_list:
            self.add_course_constraint(constraint)

    # adds constraints so that all sections of a course cannot be at the same time
    def add_same_course_constraints(self):
        # makes a dictionary with keys being unique course names and values are lists of course ids which will be appended to course_constraints
        course_occurrence = {c: [] for c in set([cl.course_name for cl in self.course_list])}
        for c in self.course_list:
            course_occurrence[c.course_name].append(c.course_id)
        
        # Creating constraints based off of same course name (different sections)
        for sections in course_occurrence.values(): #for each unique course
            for i in range(0, len(sections)-1):
                for j in range(i+1, len(sections)):
                    self.add_course_constraint((sections[i], sections[j]))
                
    # future implementation idea
    # adds a random constraint between two classes
    def add_random_course_constraints(self):
        pass
    
    # clears all constraints (neighbors) for each course object in course_list
    def clear_course_constraints(self):
        for x in self.course_list:
            x.clear_neighbors()

    # random_assign_class_to_profs function
    # Purpose: assign classes to profs in a random fashion, equally distributing classes to profs
    # output: dictionary containing profs as keys and values as list of classes
    def __random_assign_class_to_profs(self):
        prof_to_class_dict = {}
        random.shuffle(self.course_list) # shuffle the classes in class_list for randomization :)
        #https://stackoverflow.com/questions/53144723/python-evenly-distribute-value-to-a-list-in-a-dictionary  
        #Lst[ Initial : End : IndexJump ]
        # for (index of prof) and (prof) in prof_list => (0, seq[0]), (1, seq[1]), (2, seq[2]), ...
        for idx, prof in enumerate(self.prof_list):
            # gets every (number of profs)th class in class list and adds to list stored in value of dictionary
            prof_to_class_dict[prof] = self.course_list[idx::len(self.prof_list)]
        return prof_to_class_dict
        
    # future implementation idea
    # pref_assign_class_to_profs function
    # Purpose: assign classes to profs using professor preferences, attempting to equally distribute classes to profs
    # input: list of classes
    #        list of profs
    #        professor preferences
    # output: dictionary containing profs as keys and values as list of classes
    #def pref_assign_class_to_profs(class_list, prof_list, prof_preferences):
    #    prof_to_class_dict = {}
    #    return prof_to_class_dict

    # gen_graph function
    # Purpose: combine professor constraints and class constraints into adjacency list format with
    #          keys as class and values as a list of classes constrained
    # Input: prof_constraints: dictionary coming from either random_assign_class_to_profs or pref_assign_class_to_profs functions
    #        class_constraints: list of tuples containing pairs of classes that cannot be at the same time
    def gen_graph(self):
        # Transforming professor constraints to class constraints:
        # for all lists in the prof_constraints dictionary values
        prof_constraints = self.__random_assign_class_to_profs()
        for prof, prof_courses in prof_constraints.items():
            # for every node listed in the list
            for course in prof_courses:
                # for all other nodes in the list
                course.set_professor(prof)
                for other_course in prof_courses:
                    # add to adjacency list for node
                    if (other_course != course) and (other_course not in course.neighbors):
                        course.add_neighbor(other_course)
        
        # Transforming class constraints to adjacency list
        # for every pair of classes in class constraints
        for pair in self.course_constraints:
            # if first course is not in second course neighbors, add to neighbors
            if pair[0] not in pair[1].neighbors:
                pair[1].add_neighbor(pair[0])
            # if second course is not in first course neighbors, add to neighbors
            if pair[1] not in pair[0].neighbors:
                pair[0].add_neighbor(pair[1])
        return self.course_list