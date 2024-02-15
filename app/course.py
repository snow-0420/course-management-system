class Course:
    """
    Class that implements a course.
    """

    def __init__(self, course_name, course_id):
        self.name = course_name
        self.id = course_id
        self.enrolled_students = []
        self.assignments = []
