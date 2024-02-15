import itertools

from app.assignment import Assignment
from app.errors import *


class AssignmentService:

    def __init__(self):
        self.assignment_lst = []
        self.assignment_id = itertools.count()

    def get_assignment_by_id(self, assignment_id):
        for assign in self.assignment_lst:
            if assignment_id == assign.id:
                return assign
        raise InstanceNotFoundError("Assignment with id {0} does not exist".format(assignment_id))

    def create_assignment(self, assignment_name, course):
        new_assign = Assignment(assignment_name, course.id, next(self.assignment_id))
        self.assignment_lst.append(new_assign)
        course.assignments.append(new_assign.id)

        # Return the assignment object for ease
        return new_assign
