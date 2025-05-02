students = {}  

# CRUD

class Student:
    """
   implementation of a student as an object of class Student
    allows to optimize access to a student from the “students”
     storage from O(n) to O(1). Also, when creating a new instance
      of the Student class, the id which will be the key to access the
       student autoincrementing by 1.
    """
    next_id = 1
    def __init__(self, name: str, marks: list[int], info="None"):
        self.name = name
        self.marks = marks
        self.info = info
        self.id = Student.next_id
        Student.next_id += 1

    def add_marks(self, raw_marks: str) -> list:
        clear_marks = [int(item) for item in raw_marks.replace(" ", "").split(',')]
        for i in clear_marks:
            self.marks.append(i)
        return self.marks

    def update_name(self, name: str):
        self.name = name
        return self.name

    def update_info(self, info):
        self.info = info
        return self.info

    def add_info(self, info):
        self.info += info
        return self.info

    def __str__(self):
        return f'{self.id}. {self.name}'


def add_student(name, marks, info="None"):
    student = Student(name, marks, info)
    students[student.id] = student  # adding student {id: Student_instance}



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

def add_marks(student_id):
    if student_id in students:
        to_add = input("Add marks in format: 1,4,3,5: ")
        students[student_id].add_marks(to_add)
        print(f"Marks {to_add} successfully added to student {students[student_id].name}!")
    else:
        print("Student not found")

def smart_update():
    student_id: int = int(input("\nEnter student's ID: "))
    if student_id in students:
        to_update = int(input("Type '1' if you want to update students name,\n"
                              "Type '2' if you want to update students information: "))
        if to_update in [1, 2]:
            if to_update == 1:
                update_name: str = input("\nEnter new students name: ")
                print(f"\nThe student's name has been changed from {students[student_id].name} to {update_name}.")
                students[student_id].update_name(update_name)
            elif to_update == 2:
                update_info_: str = input("\nEnter new information about student: ")
                check_input = update_info_.strip(' ')
                if not students[student_id].info == "None":
                    check_objects = students[student_id].info.strip(' ')
                    for i in check_objects:
                        for j in check_input:
                            if i == j:
                                students[student_id].update_info(update_info_)
                                print(f"\nInformation about student {students[student_id].name} successfully updated")
                                return

                            students[student_id].add_info(update_info_)
                            print(f"\nInformation about student {students[student_id].name} successfully updated")
                            return
                elif students[student_id].info == "None":
                    students[student_id].update_info(update_info_)
                    print(f"\nInformation about student {students[student_id].name} successfully updated")
        else:
            print("Entered wrong number")
    else:
        print("Student not found")

def ask_student_payload():
    ask_prompt = (
        "Enter student's payload data using text template: "
        "John Doe;1,2,3,4,5;from Canada\n"
        "where 'John Doe' is a full name and [1,2,3,4,5] are marks - required input information."
        " 'from Canada' is an additional optional information.\n"
        "If you dont want to add marks, type 0.\n"
        "The data must be separated by ';' "
    )
    user_data: str = input(ask_prompt)
    if not user_data[-1] in '1234567890':
        name, raw_marks, info = user_data.split(";")
        if raw_marks == '0':
            marks = []
            print(f"Student {name} successfully added")
            return add_student(name, marks, info)

        marks = [int(item) for item in raw_marks.replace(" ", "").split(",")]
        print(f"Student {name} successfully added")
        return add_student(name, marks, info)

    else:
        name, raw_marks = user_data.split(";")
        if raw_marks == '0':
            marks = []
            print(f"Student {name} successfully added")
            return add_student(name, marks)

        marks = [int(item) for item in raw_marks.replace(" ", "").split(",")]
        print(f"Student {name} successfully added")
        return add_student(name, marks)



def student_management_command_handle(command: str):
    if command == "show all":
        show_students()
    elif command == "add student":
        ask_student_payload()
    elif command == "show student":
        student_id: int = int(input("\nEnter student's ID: "))
        show_student(student_id)
    elif command == "add marks":
        student_id: int = int(input("\nEnter student's ID: "))
        add_marks(student_id)
    elif command == "update student":
        smart_update()
    else:
        print("Command not found")

def main():
    OPERATIONAL_COMMANDS = ("quit", "help")
    STUDENT_MANAGEMENT_COMMANDS = ("show all", "add student", "show student", "add marks", "update student")
    AVAILABLE_COMMANDS = (*OPERATIONAL_COMMANDS, *STUDENT_MANAGEMENT_COMMANDS)

    HELP_MESSAGE = ("\n-USAGE GUIDE-\nCommand |show all| - view all added students with their ids\n"
                    "Command |add student| - add a student\n"
                    "Command |show student| - show added student by its id\n"
                    "Command |update student| - to update student's name or information about student\n"
                    "Command |add marks| - add marks to the student\nCommand |quit| - quit digital journal")

    START_MESSAGE = (
        "Hello in the Journal! User the menu to interact with the application.\n"
        f"Available commands: {AVAILABLE_COMMANDS}"
    )

    print(START_MESSAGE)

    while True:

        command = input("\n Select command: ").lower().strip()

        if command == "quit":
            print("\nThanks for using the Journal application")
            break
        elif command == "help":
            print(HELP_MESSAGE)
        else:
            student_management_command_handle(command)


if __name__ == "__main__":
    main()