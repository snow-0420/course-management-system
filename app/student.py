class Student:
    """
    Class that implements a student.
    """

    def __init__(self, student_name, student_id):
        self.name = student_name
        self.id = student_id
        self.enrolled_courses = []
        self.assignments = {}  # {Assignment_id: Grade}
