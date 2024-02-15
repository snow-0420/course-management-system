import pytest

from app.course_service_impl import CourseServiceImpl
from app.errors import *

def test_init():
    course_service = CourseServiceImpl()
    assert course_service.course_lst == []
    assert course_service.student_service.student_lst == []
    assert course_service.assignment_service.assignment_lst == []

def test_create_course():
    course_service = CourseServiceImpl()
    course_service.create_course("Math")
    assert len(course_service.course_lst) == 1
    assert course_service.course_lst[0].name == "Math"
    assert course_service.course_lst[0].enrolled_students == []
    assert course_service.course_lst[0].assignments == []

    with pytest.raises(InstanceExistError) as e:
        course_service.create_course("Math")
        assert str(e.value) == "Course with name Math has already existed"
        assert len(course_service.course_lst) == 1

def test_delete_course():
    course_service = CourseServiceImpl()
    course_service.create_course("Math")
    course_service.create_course("English")
    course_service.create_course("Chemistry")
    course_service.create_course("Music")
    course_service.delete_course(2) # Delete Chemistry
    assert [course.name for course in course_service.course_lst] == ["Math", "English", "Music"]

    with pytest.raises(InstanceNotFoundError) as e:
        course_service.delete_course(2)
        assert str(e.value) == "Course with id 2 does not exist"
        assert len(course_service.course_lst) == 3

def test_get_course_by_id():
    course_service = CourseServiceImpl()
    course_service.create_course("Math")
    course_service.create_course("English")
    course_service.create_course("Chemistry")
    course_service.create_course("Music")
    course_service.delete_course(2) # Delete Chemistry
    assert course_service.get_course_by_id(0).name == "Math"

    with pytest.raises(InstanceNotFoundError) as e:
        course_service.get_course_by_id(2)
        assert str(e.value) == "Course with id 2 does not exist"

def test_enroll_student():
    course_service = CourseServiceImpl()
    course_service.create_course("Math")
    course_service.student_service.create_student("Alice")
    course_service.enroll_student(0, 0) #Enrol Alice to Math
    assert course_service.get_course_by_id(0).enrolled_students == [0]
    assert course_service.student_service.get_student_by_id(0).enrolled_courses == [0]

    with pytest.raises(InstanceExistError) as e:
        course_service.enroll_student(0, 0)
        assert str(e.value) == "Alice is already enrolled in Math"

    assert course_service.get_course_by_id(0).enrolled_students == [0]
    assert course_service.student_service.get_student_by_id(0).enrolled_courses == [0]

def test_dropout_student():
    course_service = CourseServiceImpl()
    course_service.create_course("Math")
    course_service.student_service.create_student("Alice")
    course_service.student_service.create_student("Bob")
    course_service.enroll_student(0, 0) #Enrol Alice to Math

    with pytest.raises(InstanceNotFoundError) as e:
        course_service.dropout_student(0, 1) #Drop Bob from Math, but Bob is not enrolled in Math
        assert str(e.value) == "Bob is not enrolled in Math"
        assert course_service.get_course_by_id(0).enrolled_students == [0]

    course_service.dropout_student(0, 0) #Drop Alice from Math
    assert course_service.get_course_by_id(0).enrolled_students == []
    assert course_service.student_service.get_student_by_id(0).enrolled_courses == []


def test_create_assignment():
    course_service = CourseServiceImpl()
    course_service.create_course("Math")
    course_service.student_service.create_student("Alice")
    course_service.student_service.create_student("Bob")
    course_service.student_service.create_student("Catherine")
    course_service.enroll_student(0, 0) #Enrol Alice to Math
    course_service.enroll_student(0, 1) # Enrol Bob in Math
    course_service.enroll_student(0, 2) # Enrol Catherine in Math
    course_service.create_assignment(0, "Assignment 1") # Create Assignment 1 for Math
    assert course_service.get_course_by_id(0).assignments == [0]
    for student_id in course_service.get_course_by_id(0).enrolled_students:
        assert course_service.student_service.get_student_by_id(student_id).assignments[0] == 0

    with pytest.raises(InstanceExistError) as e:
        course_service.create_assignment(0, "Assignment 1")
        assert str(e.value) == "Math already has an assignment with name Assignment 1"
        assert course_service.get_course_by_id(0).assignments == [0]

def test_submit_assignment():
    course_service = CourseServiceImpl()
    course_service.create_course("Math")
    course_service.create_course("English")
    course_service.student_service.create_student("Alice")
    course_service.student_service.create_student("Bob")
    course_service.student_service.create_student("Catherine")
    course_service.enroll_student(0, 0) #Enrol Alice to Math
    course_service.enroll_student(0, 1) # Enrol Bob in Math
    course_service.enroll_student(0, 2) # Enrol Catherine in Math
    course_service.create_assignment(0, "Assignment 1") # Create Assignment 1 for Math
    course_service.create_assignment(1, "Essay 1") # Create Essay 1 for English

    course_service.submit_assignment(0, 0, 0, 85) #Alice get 85 on Assignment 1 for Math
    assert course_service.student_service.get_student_by_id(0).assignments == {0: 85}

    with pytest.raises(InstanceNotFoundError) as e:
        course_service.submit_assignment(0, 0, 1, 70) #Assignment 1 for English, but use Math as course_id
        assert str(e.value) == "Essay 1 (1) is not assigned for Math"
        assert course_service.student_service.get_student_by_id(0).assignments.get(1, -1) == -1

def test_get_assignment_grade_avg():
    course_service = CourseServiceImpl()
    course_service.create_course("Math")
    course_service.create_course("English")
    course_service.student_service.create_student("Alice")
    course_service.student_service.create_student("Bob")
    course_service.student_service.create_student("Catherine")
    course_service.enroll_student(0, 0) #Enrol Alice to Math
    course_service.enroll_student(0, 1) # Enrol Bob in Math
    course_service.enroll_student(0, 2) # Enrol Catherine in Math
    course_service.create_assignment(0, "Assignment 1") # Create Assignment 1 for Math
    course_service.submit_assignment(0, 0, 0, 85) #Alice get 85 on Assignment 1 for Math

    course_service.student_service.create_student("Donny")
    course_service.enroll_student(0, 3)

    course_service.submit_assignment(0, 1, 0, 70) #Bob get 70 on A1 for Math
    course_service.submit_assignment(0, 2, 0, 95) #Catherine get 95 on A1 for Math
    assert course_service.get_assignment_grade_avg(0, 0) == 83
    # Note that Donny do not have grades on A1 for Math, because he enrolled in
    # Math *later* than A1 is created for Math, and he hasn't submitted scores
    # for it, so didn't include it in the calculation
    course_service.submit_assignment(0, 3, 0, 66)
    # Now Donny has submitted one, avg should change
    assert course_service.get_assignment_grade_avg(0, 0) == 79

def test_get_student_grade_avg():
    course_service = CourseServiceImpl()
    course_service.create_course("Math")
    course_service.create_course("English")
    course_service.student_service.create_student("Alice")
    course_service.enroll_student(0, 0) #Enrol Alice to Math
    course_service.create_assignment(0, "Assignment 1") # Create Assignment 1 for Math
    course_service.create_assignment(0, "Midterm") #Midterm for math
    course_service.submit_assignment(0, 0, 0, 85) #Alice get 85 on Assignment 1 for Math
    course_service.submit_assignment(0, 0, 1, 90) #Alice get 90 on Midterm for Math
    assert course_service.student_service.get_student_by_id(0).assignments == {0:85, 1:90}
    assert course_service.get_student_grade_avg(0, 0) == 87

    course_service.create_assignment(0, "Final") #Final for math
    course_service.submit_assignment(0, 0, 2, 97) #Alice get 97 on Final for Math
    assert course_service.get_student_grade_avg(0, 0) == 90

def test_get_top_five_students():
    course_service = CourseServiceImpl()
    course_service.create_course("Math")
    course_service.create_course("English")
    course_service.student_service.create_student("Alice")
    course_service.student_service.create_student("Bob")
    course_service.student_service.create_student("Catherine")
    course_service.student_service.create_student("Donny")
    course_service.student_service.create_student("Elaina")
    course_service.student_service.create_student("Fiona")
    course_service.enroll_student(0, 0) #Enrol Alice to Math
    course_service.enroll_student(0, 1) # Enrol Bob in Math
    course_service.enroll_student(0, 2) # Enrol Catherine in Math
    course_service.create_assignment(0, "Assignment 1") # Create Assignment 1 for Math

    course_service.enroll_student(0, 3)
    course_service.enroll_student(0, 4)
    course_service.enroll_student(0, 5)
    course_service.create_assignment(0, "Midterm") #Midterm for math
    course_service.create_assignment(0, "Final") #Final for math
    course_service.submit_assignment(0, 0, 0, 85) #Alice get 85 on Assignment 1 for Math
    course_service.submit_assignment(0, 1, 0, 70) #Bob get 70 on A1 for Math
    course_service.submit_assignment(0, 2, 0, 95) #Catherine get 95 on A1 for Math
    course_service.submit_assignment(0, 0, 1, 90) #Alice get 90 on Midterm for Math
    course_service.submit_assignment(0, 0, 2, 97) #Alice get 97 on Final for Math
    for student_id in range(1, 6):
        for assignment_id in [1, 2]:
            course_service.submit_assignment(0, student_id, assignment_id, 15 * student_id + assignment_id * 3)
            #let everyone get some different grades :)

    # Now we should have all the grades like this:
    # Alice
    assert course_service.student_service.get_student_by_id(0).assignments == {0:85, 1:90, 2:97}
    # Bob
    assert course_service.student_service.get_student_by_id(1).assignments == {0:70, 1:18, 2:21}
    # Catherine
    assert course_service.student_service.get_student_by_id(2).assignments == {0:95, 1:33, 2:36}
    # Donny (Due to scope, the score for A1 is not included here)
    assert course_service.student_service.get_student_by_id(3).assignments == {1:48, 2:51}
    # Elaina (Enrolled after A1 and didn't submit A1, so don't count that in calculation)
    assert course_service.student_service.get_student_by_id(4).assignments == {1:63, 2:66}
    # Fiona (Same as Elaina)
    assert course_service.student_service.get_student_by_id(5).assignments == {1:78, 2:81}

    # By order, their average should be [90, 36, 54, 49, 64, 79]
    assert course_service.get_top_five_students(0) == [0, 5, 4, 2, 3]
