import itertools
from math import floor
from app.course import Course
from app.course_service import CourseService
from app.student_service import StudentService
from app.assignment_service import AssignmentService
from app.errors import *
from typing import *


class CourseServiceImpl(CourseService):
    """
    Please implement the CourseService interface according to the requirements.
    """

    def __init__(self):
        self.course_lst = []
        self.student_service = StudentService()
        self.assignment_service = AssignmentService()
        self.course_id = itertools.count()

    def get_courses(self):
        """
        Returns a list of all courses.
        """
        return self.course_lst

    def get_course_by_id(self, course_id):
        """
        Returns a course by its id.
        """
        for course in self.course_lst:
            if course.id == course_id:
                return course
        raise InstanceNotFoundError(
            "Course with id {0} does not exist".format(course_id))

    def create_course(self, course_name):
        """
        Creates a new course.
        """
        for course in self.course_lst:
            if course_name == course.name:
                raise InstanceExistError(
                    "Course with name {0} has already existed".format(
                        course_name))
        new_course = Course(course_name, next(self.course_id))
        self.course_lst.append(new_course)

    def delete_course(self, course_id):
        """
        Deletes a course by its id.
        """
        found = False
        for course in self.course_lst:
            if course_id == course.id:
                found = True
                self.course_lst.remove(course)
                print("{0} has been removed".format(course.name))
                break
        if not found:
            raise InstanceNotFoundError(
                "Course with id {0} does not exist".format(course_id))

    def create_assignment(self, course_id, assignment_name):
        """
        Creates a new assignment for a course.
        """
        course = self.get_course_by_id(course_id)
        for assign_id in course.assignments:
            if assignment_name == self.assignment_service.get_assignment_by_id(assign_id).name:
                raise InstanceExistError(
                    "{0} already has an assignment with name {1}".format(
                        course.name, assignment_name))
        new_assign = self.assignment_service.create_assignment(assignment_name,
                                                               course)
        # Every un-submitted assignment will have grade 0
        for student_id in course.enrolled_students:
            self.student_service.get_student_by_id(student_id).assignments[new_assign.id] = 0
        print("{0} has been added to {1}".format(assignment_name, course.name))

    def enroll_student(self, course_id, student_id):
        """
        Enrolls a student in a course.
        """
        course = self.get_course_by_id(course_id)
        student = self.student_service.get_student_by_id(student_id)
        if student_id in course.enrolled_students:
            raise InstanceExistError(
                "{0} is already enrolled in {1}".format(
                    student.name, course.name))
        course.enrolled_students.append(student_id)
        student.enrolled_courses.append(course_id)
        print("{0} has enrolled in {1}".format(student.name, course.name))

    def dropout_student(self, course_id, student_id):
        """
        Drops a student from a course.
        """
        course = self.get_course_by_id(course_id)
        student = self.student_service.get_student_by_id(student_id)
        if student_id not in course.enrolled_students:
            raise InstanceNotFoundError(
                "{0} is not enrolled in {1}".format(student.name, course.name))
        course.enrolled_students.remove(student_id)
        student.enrolled_courses.remove(course_id)
        print("{0} has been dropped from {1}".format(student.name, course.name))

    def submit_assignment(self, course_id, student_id, assignment_id,
                          grade: int):
        """
        Submits an assignment for a student. A grade of an assignment will be an integer between 0 and 100 inclusive.
        """
        course = self.get_course_by_id(course_id)
        assignment = self.assignment_service.get_assignment_by_id(assignment_id)
        if assignment_id not in course.assignments:
            raise InstanceNotFoundError(
                "{0} ({2}) is not assigned for {1}".format(assignment.name,
                                                           course.name,
                                                           assignment_id))
        student = self.student_service.get_student_by_id(student_id)
        student.assignments[assignment_id] = grade

    def get_assignment_grade_avg(self, course_id, assignment_id) -> int:
        """
        Returns the average grade for an assignment. Floors the result to the nearest integer.
        """
        course = self.get_course_by_id(course_id)
        if assignment_id not in course.assignments:
            raise InstanceNotFoundError(
                "Assignment {0} is not assigned for course {1}".format(
                    assignment_id, course_id))
        total_grade = 0
        num_student = 0
        for student_id in course.enrolled_students:
            if assignment_id in self.student_service.get_student_by_id(student_id).assignments:
                total_grade += self.student_service.get_student_by_id(student_id).assignments[assignment_id]
                num_student += 1

        return floor(total_grade / num_student)

    def get_student_grade_avg(self, course_id, student_id) -> int:
        """
        Returns the average grade for a student in a course. Floors the result to the nearest integer.
        """
        course = self.get_course_by_id(course_id)
        student = self.student_service.get_student_by_id(student_id)
        if student_id not in course.enrolled_students:
            raise InstanceNotFoundError(
                "{0} is not enrolled in {1}".format(student.name, course.name))
        total_grade = 0
        num_assign = 0
        for assignment_id in course.assignments:
            if assignment_id in student.assignments:
                total_grade += student.assignments[assignment_id]
                num_assign += 1

        return floor(total_grade / num_assign)

    def get_top_five_students(self, course_id) -> List[int]:
        """
        Returns the IDs of the top 5 students in a course based on their average grades of all assignments.
        """
        course = self.get_course_by_id(course_id)
        # get student_id - avg_grade pair tuple in a list
        grades = [
            (student_id, self.get_student_grade_avg(course_id, student_id)) for
            student_id in course.enrolled_students]
        grades.sort(key=lambda pair: pair[1],
                    reverse=True)  # sort using avg_grade in the tuple

        # return top 5 (or all if less than 5 students)
        return [pair[0] for pair in
                (grades[:5] if len(grades) >= 5 else grades)]
