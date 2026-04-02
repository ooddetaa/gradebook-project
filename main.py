"""
Command-line interface for the gradebook system.
"""

import argparse
import os
import logging

from gradebook.service import GradebookService
from gradebook.storage import load_data, save_data


# Path to JSON data file
DATA_FILE = "data/gradebook.json"

# Path to log file
LOG_FILE = "logs/app.log"


# Configure logging (INFO and ERROR will be saved to file)
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# Check that a text value is not empty
def parse_non_empty_text(value, field_name):
    value = value.strip()

    if not value:
        raise ValueError(f"{field_name} cannot be empty.")

    return value


# Check that grade is a valid number between 0 and 100
def parse_grade(value):
    try:
        grade = float(value)
    except ValueError:
        raise ValueError("Grade must be a number.")

    if grade < 0 or grade > 100:
        raise ValueError("Grade must be between 0 and 100.")

    return grade


# Create service and load existing data if file exists
def get_service():
    service = GradebookService()

    if os.path.exists(DATA_FILE):
        load_data(service, DATA_FILE)
        logging.info("Data loaded successfully.")

    return service


# Main CLI function
def main():
    parser = argparse.ArgumentParser(description="Gradebook CLI")
    subparsers = parser.add_subparsers(dest="command")

    # add-student command
    add_student_parser = subparsers.add_parser("add-student")
    add_student_parser.add_argument("--name", required=True)

    # add-course command
    add_course_parser = subparsers.add_parser("add-course")
    add_course_parser.add_argument("--code", required=True)
    add_course_parser.add_argument("--title", required=True)

    # enroll command
    enroll_parser = subparsers.add_parser("enroll")
    enroll_parser.add_argument("--student-id", type=int, required=True)
    enroll_parser.add_argument("--course", required=True)

    # add-grade command
    add_grade_parser = subparsers.add_parser("add-grade")
    add_grade_parser.add_argument("--student-id", type=int, required=True)
    add_grade_parser.add_argument("--course", required=True)
    add_grade_parser.add_argument("--grade", required=True)

    # list command
    list_parser = subparsers.add_parser("list")
    list_parser.add_argument("category", choices=["students", "courses", "enrollments"])
    list_parser.add_argument("--sort", choices=["name", "code"])

    # avg command
    avg_parser = subparsers.add_parser("avg")
    avg_parser.add_argument("--student-id", type=int, required=True)
    avg_parser.add_argument("--course", required=True)

    # gpa command
    gpa_parser = subparsers.add_parser("gpa")
    gpa_parser.add_argument("--student-id", type=int, required=True)

    args = parser.parse_args()
    service = get_service()

    try:
        # Add student
        if args.command == "add-student":
            name = parse_non_empty_text(args.name, "Student name")
            student = service.add_student(name)
            save_data(service, DATA_FILE)

            logging.info(f"Added student: {student.id} - {student.name}")
            print(f"Student added: ID={student.id}, Name={student.name}")

        # Add course
        elif args.command == "add-course":
            code = parse_non_empty_text(args.code, "Course code")
            title = parse_non_empty_text(args.title, "Course title")
            course = service.add_course(code, title)
            save_data(service, DATA_FILE)

            logging.info(f"Added course: {course.code}")
            print(f"Course added: Code={course.code}, Title={course.title}")

        # Enroll student
        elif args.command == "enroll":
            course_code = parse_non_empty_text(args.course, "Course code")
            service.enroll(args.student_id, course_code)
            save_data(service, DATA_FILE)

            logging.info(f"Enrolled student {args.student_id} in {course_code}")
            print("Student enrolled successfully.")

        # Add grade
        elif args.command == "add-grade":
            course_code = parse_non_empty_text(args.course, "Course code")
            grade = parse_grade(args.grade)
            service.add_grade(args.student_id, course_code, grade)
            save_data(service, DATA_FILE)

            logging.info(f"Added grade for student {args.student_id} in {course_code}: {grade}")
            print("Grade added successfully.")

        # List data
        elif args.command == "list":
            if args.category == "students":
                students = service.list_students(sort_by=args.sort)
                for student in students:
                    print(f"ID={student.id}, Name={student.name}")

            elif args.category == "courses":
                courses = service.list_courses(sort_by=args.sort)
                for course in courses:
                    print(f"Code={course.code}, Title={course.title}")

            elif args.category == "enrollments":
                enrollments = service.list_enrollments()
                for enrollment in enrollments:
                    print(
                        f"Student ID={enrollment.student_id}, "
                        f"Course={enrollment.course_code}"
                    )

        # Compute average
        elif args.command == "avg":
            course_code = parse_non_empty_text(args.course, "Course code")
            average = service.compute_average(args.student_id, course_code)

            logging.info(f"Computed average for student {args.student_id} in {course_code}")
            print(f"Average: {average:.2f}")

        # Compute GPA
        elif args.command == "gpa":
            gpa = service.compute_gpa(args.student_id)

            logging.info(f"Computed GPA for student {args.student_id}")
            print(f"GPA: {gpa:.2f}")

        else:
            parser.print_help()

    except ValueError as error:
        logging.error(f"ValueError: {error}")
        print(f"Error: {error}")

    except Exception as error:
        logging.error(f"Unexpected error: {error}")
        print(f"Unexpected error: {error}")


if __name__ == "__main__":
    main()