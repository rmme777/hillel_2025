"""
1. Application - Python
2. User - Teacher in the scool
3. Iterface - TUI (Terminal User Interface)


struct Student:
    name: str
    marks: list[int]

struct Teacher: no structure since authentication process
"""

students = {}

# CRUD

class Student:
    next_id = 1
    def __init__(self, name: str, marks: list[int], info: str):
        self.name = name
        self.marks = marks
        self.info = info
        self.id = Student.next_id
        Student.next_id += 1

    def __str__(self):
        return f'{self.id}. {self.name}'


def add_student(name, marks, info=None):
    student = Student(name, marks, info)
    students[student.id] = student



def show_students():
    if len(students) >= 1:
        print("=========================")
        for student in students.values():
            print(student)
        print("=========================\n")
    else:
        print('There are no added students')

def show_student(student_id):
    if student_id in students.keys():
        to_info = students[student_id]
        text = f"{to_info.id}. {to_info.name} <-\nMarks: {to_info.marks}\nInfo: {to_info.info}"
        print("=========================")
        print(text)
        print("=========================")
    else:
        print('Student not found')


def ask_student_payload():
    ask_prompt = (
        "Enter student's payload data using text template: "
        "John Doe;1,2,3,4,5;from Canada\n"
        "where 'John Doe' is a full name, [1,2,3,4,5] are marks and 'from Canada' is an additional information.\n"
        "The data must be separated by ';' "
    )
    user_data: str = input(ask_prompt)
    if not user_data[-1] in '1234567890':
        name, raw_marks, info = user_data.split(";")
        marks = [int(item) for item in raw_marks.replace(" ", "").split(",")]
        print(f"Student {name} successfully added")
        return add_student(name, marks, info)
    else:
        name, raw_marks = user_data.split(";")
        marks = [int(item) for item in raw_marks.replace(" ", "").split(",")]
        print(f"Student {name} successfully added")
        return add_student(name, marks)



def student_management_command_handle(command: str):
    if command == "show":
        show_students()
    elif command == "add":
        ask_student_payload()
    elif command == "search":
        student_id: int = int(input("\nEnter student's ID: "))
        show_student(student_id)
    else:
        print("Command not found")

def main():
    OPERATIONAL_COMMANDS = ("quit", "help")
    STUDENT_MANAGEMENT_COMMANDS = ("show", "add", "search")
    AVAILABLE_COMMANDS = (*OPERATIONAL_COMMANDS, *STUDENT_MANAGEMENT_COMMANDS)

    HELP_MESSAGE = (
        "Hello in the Journal! User the menu to interact with the application.\n"
        f"Available commands: {AVAILABLE_COMMANDS}"
    )

    print(HELP_MESSAGE)

    while True:

        command = input("\n Select command: ")

        if command == "quit":
            print("\nThanks for using the Journal application")
            break
        elif command == "help":
            print(HELP_MESSAGE)
        else:
            student_management_command_handle(command)


if __name__ == "__main__":
    main()