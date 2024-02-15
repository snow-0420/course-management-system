from app.errors import *
from app.student import Student


class StudentService:

    def __init__(self):
        self.student_lst = []

    def get_student_by_id(self, student_id):
        for student in self.student_lst:
            if student_id == student.id:
                return student
        raise InstanceNotFoundError("Student with id {0} does not exist".format(student_id))

    def create_student(self, student_name):
        for student in self.student_lst:
            if student_name == student.name:
                raise InstanceExistError(
                    "Student with {0} has already existed".format(student_name))
        new_student = Student(student_name)
        self.student_lst.append(new_student)

    def remove_student(self, student_id):
        found = False
        for student in self.student_lst:
            if student_id == student.id:
                found = True
                self.student_lst.remove(student)
                print("{0} has been removed".format(student.name))
                break
        if not found:
            raise InstanceNotFoundError("Student with id {0} does not exist".format(student_id))
