"""
Unit tests for the gradebook service.
"""

import unittest

from gradebook.service import GradebookService


# Tests for the GradebookService class
class TestGradebookService(unittest.TestCase):
    """Test cases for gradebook service methods."""

    # Create a fresh service before each test
    def setUp(self):
        self.service = GradebookService()

    # Test adding a student
    def test_add_student(self):
        student = self.service.add_student("John Doe")

        self.assertEqual(student.id, 1)
        self.assertEqual(student.name, "John Doe")
        self.assertEqual(len(self.service.students), 1)

    # Test adding a grade after student is enrolled in a course
    def test_add_grade(self):
        student = self.service.add_student("John Doe")
        self.service.add_course("CS101", "Intro to CS")
        self.service.enroll(student.id, "CS101")

        grade = self.service.add_grade(student.id, "CS101", 95)

        self.assertEqual(grade.student_id, student.id)
        self.assertEqual(grade.course_code, "CS101")
        self.assertEqual(grade.grade, 95)
        self.assertEqual(len(self.service.grades), 1)

    # Test computing average grade for a student in one course
    def test_compute_average(self):
        student = self.service.add_student("John Doe")
        self.service.add_course("CS101", "Intro to CS")
        self.service.enroll(student.id, "CS101")

        self.service.add_grade(student.id, "CS101", 90)
        self.service.add_grade(student.id, "CS101", 100)

        average = self.service.compute_average(student.id, "CS101")

        self.assertEqual(average, 95)

    # Test failing case: adding grade without enrollment
    def test_add_grade_without_enrollment(self):
        student = self.service.add_student("John Doe")
        self.service.add_course("CS101", "Intro to CS")

        with self.assertRaises(ValueError):
            self.service.add_grade(student.id, "CS101", 95)


# Run the tests
if __name__ == "__main__":
    unittest.main()