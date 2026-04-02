"""
Storage functions for saving and loading gradebook data.
"""

import json

from .models import Student, Course, Enrollment, Grade


# Save gradebook data to a JSON file
def save_data(service, filename):
    data = {
        "students": [
            {"id": student.id, "name": student.name}
            for student in service.students
        ],
        "courses": [
            {"code": course.code, "title": course.title}
            for course in service.courses
        ],
        "enrollments": [
            {
                "student_id": enrollment.student_id,
                "course_code": enrollment.course_code
            }
            for enrollment in service.enrollments
        ],
        "grades": [
            {
                "student_id": grade.student_id,
                "course_code": grade.course_code,
                "grade": grade.grade
            }
            for grade in service.grades
        ],
        "next_student_id": service.next_student_id
    }

    # Write data to JSON file
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


# Load gradebook data from a JSON file
def load_data(service, filename):
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Rebuild students
    service.students = [
        Student(student["id"], student["name"])
        for student in data.get("students", [])
    ]

    # Rebuild courses
    service.courses = [
        Course(course["code"], course["title"])
        for course in data.get("courses", [])
    ]

    # Rebuild enrollments
    service.enrollments = [
        Enrollment(enrollment["student_id"], enrollment["course_code"])
        for enrollment in data.get("enrollments", [])
    ]

    # Rebuild grades
    service.grades = [
        Grade(grade["student_id"], grade["course_code"], grade["grade"])
        for grade in data.get("grades", [])
    ]

    # Restore next student ID
    service.next_student_id = data.get("next_student_id", 1)