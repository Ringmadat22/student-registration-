import datetime
import pickle

class Course:
    def __init__(self, dept, num, name, credits):
        self.dept = dept
        self.num = num
        self.name = name
        self.credits = credits

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
        # For simplicity, assuming the grade is just appended to student's transcript
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
    dept = input('Please enter department code: ')
    num = int(input('Please enter a course number: '))
    name = input('Please enter name: ')
    credits = int(input('Please enter number of credits: '))
    course = Course(dept, num, name, credits)
    institution['courses'][(dept, num)] = course
    print('\n' + course.name + ' added to course list!\n')

def schedule_course_offering(institution):
    key = input('Course Name: ')
    if key in institution['courses']:
        course = institution['courses'][key]
        section = int(input('Please enter a section number: '))
        quarter = input('Please enter quarter (Fall, Winter, Spring, Summer): ')
        year = int(input('Please enter year (YYYY): '))
        course_offering = CourseOffering(course, section, year, quarter)
        institution['course_offerings'][(course.dept, course.num, section, year, quarter)] = course_offering
        print('\n' + course_offering.__str__() + ' has been scheduled!\n')
    else:
        print('This course is not currently offered. Please add new course or select from the following offerings: \n')

def list_course_catalog(institution):
    print('\nCourse Catalog:')
    for key, course in institution['courses'].items():
        print(f"{key}: {course.name}, Credits: {course.credits}")
    print()

def list_course_schedule(institution):
    quarter = input('Please enter quarter (Fall, Winter, Spring, Summer): ')
    year = int(input('Please enter year (YYYY): '))
    print('\nCourse Schedule:')
    for key, course_offering in institution['course_offerings'].items():
        if course_offering.quarter == quarter and course_offering.year == year:
            print(course_offering)
    print()

def hire_instructor(institution):
    last_name = input('Please enter instructor last name: ')
    first_name = input('Please enter instructor first name: ')
    year = int(input('Please enter year (YYYY): '))
    month = int(input('Please enter birth month (MM): '))
    day = int(input('Please enter birth day (DD): '))
    dob = datetime.date(year, month, day)
    username = input('Please give instructor a unique username: ')
    instructor = Instructor(last_name, first_name, institution['name'], dob, username)
    institution['instructors'][username] = instructor
    print('\nYou have hired', instructor.first_name, instructor.last_name, '\n')

def assign_instructor(institution):
    username = input('Instructor username: ')
    if username in institution['instructors']:
        this_instructor = institution['instructors'][username]
        course_name = input('Course name: ')
        dept = input('Department: ')
        number = int(input('Course Number: '))
        quarter = input('Please enter quarter (Fall, Winter, Spring, Summer): ')
        year = int(input('Please enter year (YYYY): '))
        section = int(input('Section Number: '))
        offering_key = (dept, number, section, year, quarter)
        if offering_key in institution['course_offerings']:
            institution['course_offerings'][offering_key].assign_instructor(this_instructor)
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
    student = Student(last_name, first_name, institution['name'], dob, username)
    institution['students'][username] = student
    print('\n' + student.first_name, student.last_name, 'has been enrolled!\n')

def register_student(institution):
    username = input('Student username: ')
    course_name = input('Course name: ')
    if username in institution['students'] and course_name in institution['courses']:
        student = institution['students'][username]
        course = institution['courses'][course_name]
        section = int(input('Section Number: '))
        quarter = input('Please enter quarter (Fall, Winter, Spring, Summer): ')
        year = int(input('Please enter year offered (YYYY): '))
        offering_key = (course.dept, course.num, section, year, quarter)
        if offering_key in institution['course_offerings']:
            institution['course_offerings'][offering_key].register_student(student)
            print(student.first_name, student.last_name, 'has been registered for', course_name)
        else:
            print('Invalid course offering.\n')
    else:
        print('Invalid student or course.\n')

def list_enrolled_students(institution):
    print('\nEnrolled Students:')
    for username, student in institution['students'].items():
        print(f"{student.first_name} {student.last_name} ({username})")
    print()

def list_students_registered_for_course(institution):
    course_name = input('Course name: ')
    if course_name in institution['courses']:
        print(f"\nStudents registered for {course_name}:")
        for offering_key, course_offering in institution['course_offerings'].items():
            if offering_key[:2] == course_name:
                print(f"Section {offering_key[2]} ({offering_key[4]} {offering_key[3]}):")
                for student in course_offering.enrolled_students:
                    print(f"{student.first_name} {student.last_name} ({student.username})")
                print()
    else:
        print('Invalid course.\n')

def list_faculty(institution):
    print('\nFaculty:')
    for username, instructor in institution['instructors'].items():
        print(f"{instructor.first_name} {instructor.last_name} ({username})")
    print()

def submit_student_grade(institution):
    username = input('Student username: ')
    course_name = input('Course name: ')
    quarter = input('Please enter quarter (Fall, Winter, Spring, Summer): ')
    year = int(input('Please enter year (YYYY): '))
    section = int(input('Section Number: '))
    grade = input('Enter a grade (A to F): ')
    offering_key = (course_name, section, year, quarter)
    if username in institution['students'] and offering_key in institution['course_offerings']:
        student = institution['students'][username]
        institution['course_offerings'][offering_key].submit_grade(student, grade)
        print('Grade submitted successfully!\n')
    else:
        print('Invalid student or course offering.\n')

def get_student_records(institution):
    username = input('Enter student username: ')
    if username in institution['students']:
        student = institution['students'][username]
        print(student)
        print('Transcript\n----------\n')
        for course_name, grade in student.transcript.items():
            print(f"{course_name}: {grade}")
    else:
        print('Invalid student.\n')

def main():
    print('\nWelcome to the Registration System\n')

    institution = {}

    # Data Persistence
    load_existing = input('Would you like to load existing data? Enter Yes or No: ').lower()

    if load_existing == 'yes':
        file_path = input('Please enter the filepath: ')  # must be a .pickle file
        with open(file_path, 'rb') as pickle_file:
            institution = pickle.load(pickle_file)  # load existing registration

    else:  # create a new institution dictionary
        name = input('Please enter an institution name: ')
        domain = input('Please enter a domain name (format = <institution>.edu): ')
        institution = {
            'name': name,
            'domain': domain,
            'courses': {},
            'course_offerings': {},
            'instructors': {},
            'students': {}
        }

    menu_string = (
        '\nPlease select an option from the following:\n\n'
        'MENU\n'
        '----------------------------------------\n'
        '1 Create a course\n'
        '2 Schedule a course offering\n'
        '3 List course catalog\n'
        '4 List course schedule\n'
        '5 Hire an instructor\n'
        '6 Assign an instructor to a course\n'
        '7 Enroll a student\n'
        '8 Register a student for a course\n'
        '9 List enrolled students\n'
        '10 List students registered for a course\n'
        '11 List faculty\n'
        '12 Submit student grade\n'
        '13 Get student records\n'
        '14 EXIT\n'
    )

    menu_options = {
        '1': create_course,
        '2': schedule_course_offering,
        '3': list_course_catalog,
        '4': list_course_schedule,
        '5': hire_instructor,
        '6': assign_instructor,
        '7': enroll_student,
        '8': register_student,
        '9': list_enrolled_students,
        '10': list_students_registered_for_course,
        '11': list_faculty,
        '12': submit_student_grade,
        '13': get_student_records
    }

    while True:
        var = input('\n ...press enter to continue...')
        if not var:
            print(menu_string)
            menu_input = input('Enter Menu Choice: ')
            if menu_input == '14':
                print('\nEXITING...Thank you!\n')
                break
            elif menu_input in menu_options:
                menu_options[menu_input](institution)
            else:
                print('\nINVALID MENU OPTION: Please try again\n')

    save_session = input('Would you like to save the contents of this session? Enter Yes or No: ').lower()

    if save_session == 'yes':
        file_name = input('Please enter a filename for saving your data (this is a .pickle file): ')
        with open(file_name, 'wb') as pickle_file:
            pickle.dump(institution, pickle_file)
        print('Session contents saved, goodbye!')
    else:
        print('Goodbye!')

if __name__ == "__main__":
    main()
