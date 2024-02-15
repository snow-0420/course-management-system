from app.assignment import Assignment
from app.errors import *


class AssignmentService:

    def __init__(self):
        self.assignment_lst = []

    def get_assignment_by_id(self, assignment_id):
        for assign in self.assignment_lst:
            if assignment_id == assign.id:
                return assign
        raise InstanceNotFoundError("Assignment with id {0} does not exist".format(assignment_id))

    def create_assignment(self, assignment_name, course):
        for assignment in self.assignment_lst:
            if assignment_name == assignment.name:
                raise InstanceExistError(
                    "Assignment with {0} has already existed".format(assignment_name))
        new_assign = Assignment(assignment_name, course.id)
        self.assignment_lst.append(new_assign)
        course.assignments.append(new_assign.id)
        # Every un-submitted assignment will have grade 0
        for student in course.enrolled_students:
            student.assignments[new_assign.id] = 0
