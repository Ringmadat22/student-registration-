import datetime

class Institution:
    def __init__(self, institution_name, institution_domain):
        self.institution_name = institution_name
        self.institution_domain = institution_domain
        self.courses = {}
        self.course_offerings = {}
        self.instructors = {}
        self.students = {}

    def add_course(self, course):
        self.courses[course.name] = course

    def add_course_offering(self, course_offering):
        key = (course_offering.course.dept, course_offering.course.name, course_offering.section, course_offering.year, course_offering.quarter)
        self.course_offerings[key] = course_offering

    def add_instructor(self, instructor):
        self.instructors[instructor.username] = instructor

    def add_student(self, student):
        self.students[student.username] = student

class Course:
    def __init__(self, dept, name, hours):
        self.dept = dept
        self.name = name
        self.hours = hours

class CourseOffering:
    def __init__(self, course, section, year, quarter):
        self.course = course
        self.section = section
        self.year = year
        self.quarter = quarter
        self.instructor = None
        self.enrolled_students = []

    def assign_instructor(self, instructor):
        self.instructor = instructor

    def register_student(self, student):
        self.enrolled_students.append(student)

    def submit_grade(self, student, grade):
        student.transcript[self.course.name] = grade

class Instructor:
    def __init__(self, last_name, first_name, institution, dob, username):
        self.last_name = last_name
        self.first_name = first_name
        self.institution = institution
        self.dob = dob
        self.username = username

class Student:
    def __init__(self, last_name, first_name, institution, dob, username):
        self.last_name = last_name
        self.first_name = first_name
        self.institution = institution
        self.dob = dob
        self.username = username
        self.transcript = {}


def create_course(institution):
    dept = input("Enter department: ")
    name = input("Enter course name: ")
    hours = input("Enter course hours: ")
    try:
        hours = int(hours)
    except ValueError:
        print("Please enter a valid number for hours.")
        return
    course = Course(dept, name, hours)
    institution.add_course(course)
    print(f'\n{course.name} added to course list!\n')

def list_course_catalog(institution):
    print('\nCourse Catalog:')
    for course in institution.courses.values():
        print(f"{course.dept} {course.name}, hours: {course.hours}")
    print()

def hire_instructor(institution):
    first_name = input('Please enter instructor first name: ')
    last_name = input('Please enter instructor last name: ')
    year = int(input('Please enter year (YYYY): '))
    month = int(input('Please enter birth month (MM): '))
    day = int(input('Please enter birth day (DD): '))
    dob = datetime.date(year, month, day)
    username = input('Please give instructor a unique username: ')
    instructor = Instructor(last_name, first_name, institution.institution_name, dob, username)
    institution.add_instructor(instructor)
    print('\nYou have hired', instructor.first_name, instructor.last_name, '\n')

def assign_instructor(institution):
    username = input('Instructor username: ')
    if username in institution.instructors:
        this_instructor = institution.instructors[username]
        course_name = input('Course name: ')
        dept = input('Department: ')
        section = int(input('Section Number: '))
        quarter = input('Please enter quarter (Fall, Winter, Spring, Summer): ')
        year = int(input('Please enter year (YYYY): '))
        offering_key = (dept, course_name, section, year, quarter)
        if offering_key in institution.course_offerings:
            institution.course_offerings[offering_key].assign_instructor(this_instructor)
            print('Instructor assigned successfully!\n')
        else:
            print('Invalid course offering.\n')
    else:
        print('Invalid instructor username.\n')

def enroll_student(institution):
    last_name = input('Last name: ')
    first_name = input('First name: ')
    year = int(input('Birth year (YYYY): '))
    month = int(input('Birth month (MM): '))
    day = int(input('Birth day (DD): '))
    dob = datetime.date(year, month, day)
    username = input('Assign unique username: ')
    student = Student(last_name, first_name, institution.institution_name, dob, username)
    institution.add_student(student)
    print(f'\n{student.first_name} {student.last_name} has been enrolled!\n')

def register_student(institution):
    username = input('Student username: ')
    course_name = input('Course name: ')
    if username in institution.students and course_name in institution.courses:
        student = institution.students[username]
        course = institution.courses[course_name]
        section = int(input('Section Number: '))
        quarter = input('Please enter quarter (Fall, Winter, Spring, Summer): ')
        year = int(input('Please enter year offered (YYYY): '))
        offering_key = (course.dept, course.name, section, year, quarter)
        if offering_key in institution.course_offerings:
            institution.course_offerings[offering_key].register_student(student)
            print(f'{student.first_name} {student.last_name} has been registered for {course_name}')
        else:
            print('Invalid course offering.\n')
    else:
        print('Invalid student or course.\n')

def list_enrolled_students(institution):
    print('\nEnrolled Students:')
    for student in institution.students.values():
        print(f"{student.first_name} {student.last_name} ({student.username})")
    print()

def list_students_registered_for_course(institution):
    course_name = input('Course name: ')
    if course_name in institution.courses:
        print(f"\nStudents registered for {course_name}:")
        for offering_key, course_offering in institution.course_offerings.items():
            if offering_key[1] == course_name:
                print(f"Section {offering_key[2]} ({offering_key[4]} {offering_key[3]}):")
                for student in course_offering.enrolled_students:
                    print(f"{student.first_name} {student.last_name} ({student.username})")
                print()
    else:
        print('Invalid course.\n')

def submit_student_grade(institution):
    username = input('Student username: ')
    course_name = input('Course name: ')
    quarter = input('Please enter quarter (Fall, Winter, Spring, Summer): ')
    year = int(input('Please enter year (YYYY): '))
    section = int(input('Section Number: '))
    grade = input('Enter a grade (A to F): ')
    offering_key = (course_name, section, year, quarter)
    if username in institution.students and offering_key in institution.course_offerings:
        student = institution.students[username]
        institution.course_offerings[offering_key].submit_grade(student, grade)
        print('Grade submitted successfully!\n')
    else:
        print('Invalid student or course offering.\n')

def get_student_records(institution):
    username = input('Enter student username: ')
    if username in institution.students:
        student = institution.students[username]
        print(student)
        print('Transcript\n----------\n')
        for course_name, grade in student.transcript.items():
            print(f"{course_name}: {grade}")
    else:
        print('Invalid student.\n')

def main():
    print('\nWelcome to the Registration System\n')

    name = input('Please enter an institution name: ')
    domain = input('Please enter a domain name (format = <institution>.edu): ')
    institution = Institution(name, domain)

    menu_string = (
        '\nPlease select an option from the following:\n\n'
        'MENU\n'
        '----------------------------------------\n'
        '1 Create a course\n'
        '2 List course catalog\n'
        '3 Hire an instructor\n'
        '4 Assign an instructor to a course\n'
        '5 Enroll a student\n'
        '6 Register a student for a course\n'
        '7 List enrolled students\n'
        '8 List students registered for a course\n'
        '9 Submit student grade\n'
        '10 Get student records\n'
        '11 EXIT\n'
    )

    menu_options = {
        '1': create_course,
        '2': list_course_catalog,
        '3': hire_instructor,
        '4': assign_instructor,
        '5': enroll_student,
        '6': register_student,
        '7': list_enrolled_students,
        '8': list_students_registered_for_course,
        '9': submit_student_grade,
        '10': get_student_records
    }

    while True:
        var = input('\n ...press enter to continue...')
        if not var:
            print(menu_string)
            menu_input = input('Enter Menu Choice: ')
            if menu_input == '13':
                print('\nEXITING...Thank you!\n')
                break
            elif menu_input in menu_options:
                menu_options[menu_input](institution)
            else:
                print('\nINVALID MENU OPTION: Please try again\n')

    save_session = input('Would you like to save the contents of this session? Enter Yes or No: ').lower()

    # if save_session == 'yes':
    #     file_name = input('Please enter a filename for saving your data (this is a .pickle file): ')
    #     with open(file_name, 'wb') as pickle_file:
    #         pickle.dump(institution, pickle_file)
    #     print('Session contents saved, goodbye!')
    # else:
    #     print('Goodbye!')

if __name__ == "__main__":
    main()
