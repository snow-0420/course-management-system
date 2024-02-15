from app.assignment import Assignment
from app.errors import *


class Course:
    """
    Class that implements a course.
    """
    course_id = 0

    def __init__(self, course_name):
        self.name = course_name
        self.id = Course.course_id
        Course.course_id += 1
        self.enrolled_students = []
        self.assignments = []

    def add_assignment(self, assignment_id):
        """
        Add an assignment to this course.
        """

