"""
Data models for the gradebook system.
"""


# Represents a student with an ID and name
class Student:
    """Student entity."""

    def __init__(self, student_id: int, name: str):
        self.id = student_id      # unique student ID
        self.name = name          # student name


# Represents a course with code and title
class Course:
    """Course entity."""

    def __init__(self, code: str, title: str):
        self.code = code          # course code (e.g., CS101)
        self.title = title        # course title


# Represents enrollment of a student in a course
class Enrollment:
    """Enrollment entity."""

    def __init__(self, student_id: int, course_code: str):
        self.student_id = student_id   # ID of the student
        self.course_code = course_code # course code


# Represents a grade for a student in a course
class Grade:
    """Grade entity."""

    def __init__(self, student_id: int, course_code: str, grade: float):
        self.student_id = student_id   # ID of the student
        self.course_code = course_code # course code
        self.grade = grade             # numeric grade