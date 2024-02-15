class Assignment:
    """
    Class that implements an assignment.
    """
    assignment_id = 0

    def __init__(self, assignment_name, course_id):
        self.name = assignment_name
        self.id = Assignment.assignment_id
        Assignment.assignment_id += 1
        self.assigned_course = course_id
