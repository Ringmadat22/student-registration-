students = []

def register_student():
    name = input("Enter student name: ")
    age = int(input("Enter student age: "))
    grade = input("Enter student grade of completion: ")
    nationality = input("Enter student nationality: ")
    student_type = input("Enter student type: ")
    registration_method = input("Enter registration method: ")
    
    # Ask for subjects and marks and store them in a dictionary
    subjects_marks = {}
    while True:
        subject = input("Enter subject (or type 'done' to finish): ")
        if subject.lower() == 'done':
            break
        mark = float(input(f"Enter mark for {subject}: "))
        subjects_marks[subject] = mark
    
    student = {
        "name": name,
        "age": age,
        "grade": grade,
        "nationality": nationality,
        "student_type": student_type,
        "registration_method": registration_method,
        "subjects_marks": subjects_marks  # Add subjects and marks to the student dictionary
    }
    students.append(student)
    print("Student registered successfully!")

def view_students():
    if not students:
        print("No students registered yet.")
    else:
        print("Student data:")
        for index, student in enumerate(students, start=1):
            print(f"{index}. Name: {student['name']}, Age: {student['age']}, Grade: {student['grade']}, Nationality: {student['nationality']}, Student_type: {student['student_type']}, Registration_method: {student['registration_method']}")
            print("Subjects and Marks:")
            for subject, mark in student['subjects_marks'].items():
                print(f"    {subject}: {mark}")

def update_student():
    view_students()
    if not students:
        return
    choice = int(input("Enter student number to update: "))
    if choice <= 0 or choice > len(students):
        print("Invalid student number.")
        return
    student = students[choice - 1]
    print(f"Updating {student['name']}:")
    student["name"] = input("Enter updated name: ")
    student["age"] = int(input("Enter updated age: "))
    student["grade"] = input("Enter updated grade: ")
    student["nationality"] = input("Enter student nationality: ")
    student["student_type"] = input("Enter student type: ")
    student["registration_method"] = input("Enter registration_method: ")
    
    # Update subjects and marks
    subjects_marks = {}
    while True:
        subject = input("Enter subject (or type 'done' to finish): ")
        if subject.lower() == 'done':
            break
        mark = float(input(f"Enter mark for {subject}: "))
        subjects_marks[subject] = mark
    student["subjects_marks"] = subjects_marks
    
    print("Student information updated successfully!")

def delete_student():
    view_students()
    if not students:
        return
    choice = int(input("Enter student number to delete: "))
    if choice <= 0 or choice > len(students):
        print("Invalid student number.")
        return
    deleted_student = students.pop(choice - 1)
    print(f"{deleted_student['name']} deleted successfully!")

def menu():
    print("\nWelcome to Student Registration System")
    print()
    print("1. Register Student")
    print()
    print("2. View Students")
    print()
    print("3. Update Student Information")
    print()
    print("4. Delete Student")
    print()
    print("5. Exit")
    print()

# Main loop
while True:
    menu()
    option = input("Enter your choice: ")
    if option == '1':
        register_student()
        print()
    elif option == '2':
        view_students()
        print()
    elif option == '3':
        update_student()
        print()
    elif option == '4':
        delete_student()
        print()
    elif option == '5':
        print("Thank you. Exiting...")
        break
        print()
    else:
        print("Invalid option. Please choose again.")
        print()