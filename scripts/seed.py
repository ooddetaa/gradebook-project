"""
Seed script for creating sample gradebook data.
"""

from gradebook.service import GradebookService
from gradebook.storage import save_data


# Path to the JSON file
DATA_FILE = "data/gradebook.json"


# Create sample data and save it
def main():
    service = GradebookService()

    # Add students
    student1 = service.add_student("John Doe")
    student2 = service.add_student("Jane Smith")
    student3 = service.add_student("Alice Brown")

    # Add courses
    service.add_course("CS101", "Intro to CS")
    service.add_course("MATH101", "Calculus I")

    # Enroll students in courses
    service.enroll(student1.id, "CS101")
    service.enroll(student1.id, "MATH101")
    service.enroll(student2.id, "CS101")
    service.enroll(student3.id, "MATH101")

    # Add grades
    service.add_grade(student1.id, "CS101", 90)
    service.add_grade(student1.id, "CS101", 85)
    service.add_grade(student1.id, "MATH101", 88)

    service.add_grade(student2.id, "CS101", 95)

    service.add_grade(student3.id, "MATH101", 92)
    service.add_grade(student3.id, "MATH101", 89)

    # Save everything to JSON
    save_data(service, DATA_FILE)

    print("Sample data created in data/gradebook.json")


# Run the seed script
if __name__ == "__main__":
    main()