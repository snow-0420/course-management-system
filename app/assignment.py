class Assignment:
    """
    Class that implements an assignment.
    """

    def __init__(self, assignment_name, course_id, assignment_id):
        self.name = assignment_name
        self.id = assignment_id
        self.assigned_course = course_id
