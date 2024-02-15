class Student:
    """
    Class that implements a student.
    """
    student_id = 0

    def __init__(self, student_name):
        self.name = student_name
        self.id = Student.student_id
        Student.student_id += 1
        self.enrolled_courses = []
        self.assignments = {}  # {Assignment_id: Grade}
