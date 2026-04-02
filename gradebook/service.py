"""
Service layer for the gradebook system.
"""

from .models import Student, Course, Enrollment, Grade


class GradebookService:
    """Main service class that manages gradebook operations."""

    def __init__(self):
        self.students = []
        self.courses = []
        self.enrollments = []
        self.grades = []
        self.next_student_id = 1

    def add_student(self, name: str):
        """Add a new student."""
        student = Student(self.next_student_id, name)
        self.students.append(student)
        self.next_student_id += 1
        return student

    def add_course(self, code: str, title: str):
        """Add a new course."""
        for course in self.courses:
            if course.code == code:
                raise ValueError("Course already exists.")

        course = Course(code, title)
        self.courses.append(course)
        return course

    def enroll(self, student_id: int, course_code: str):
        """Enroll a student in a course."""
        if not any(student.id == student_id for student in self.students):
            raise ValueError("Student not found.")

        if not any(course.code == course_code for course in self.courses):
            raise ValueError("Course not found.")

        for enrollment in self.enrollments:
            if enrollment.student_id == student_id and enrollment.course_code == course_code:
                raise ValueError("Student already enrolled in this course.")

        enrollment = Enrollment(student_id, course_code)
        self.enrollments.append(enrollment)
        return enrollment

    def add_grade(self, student_id: int, course_code: str, grade: float):
        """Add a grade for a student in a course."""
        enrolled = any(
            enrollment.student_id == student_id and enrollment.course_code == course_code
            for enrollment in self.enrollments
        )

        if not enrolled:
            raise ValueError("Student is not enrolled in this course.")

        grade_obj = Grade(student_id, course_code, grade)
        self.grades.append(grade_obj)
        return grade_obj

    def list_students(self, sort_by=None):
        """Return list of students (optionally sorted)."""
        if sort_by == "name":
            return sorted(self.students, key=lambda student: student.name)
        return self.students

    def list_courses(self, sort_by=None):
        """Return list of courses (optionally sorted)."""
        if sort_by == "code":
            return sorted(self.courses, key=lambda course: course.code)
        return self.courses

    def list_enrollments(self):
        """Return list of enrollments."""
        return self.enrollments

    def compute_average(self, student_id: int, course_code: str):
        """Compute average grade for a student in a course."""
        matching_grades = [
            grade.grade
            for grade in self.grades
            if grade.student_id == student_id and grade.course_code == course_code
        ]

        if not matching_grades:
            raise ValueError("No grades found for this student in this course.")

        return sum(matching_grades) / len(matching_grades)

    def compute_gpa(self, student_id: int):
        """Compute GPA (average of all grades for a student)."""
        student_grades = [
            grade.grade
            for grade in self.grades
            if grade.student_id == student_id
        ]

        if not student_grades:
            raise ValueError("No grades found for this student.")

        return sum(student_grades) / len(student_grades)