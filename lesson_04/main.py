from repositories.repository import StudentRepository

repo = StudentRepository() # persistent storage

def add_student(name: str, marks, info):
    info = info or ""
    to_add = f"{name};{marks};{info}"
    repo.add_person(to_add)
    print(f"Student {name} successfully added!")


def show_students():
    students = repo.get_info_of_all_persons()
    # print(f"[DEBUG] Received {students}")
    if students:
        print("=========================")
        for row in students:
            print(f"{row.split(';')[0]}. {row.split(';')[1]}")
        print("=========================")
    else:
        print("No students added")

def show_student(student_id):
    student_raw = repo.get_person_info(student_id)
    if not student_raw:
        print('Student not found')
        return
    student = student_raw.split(';')
    text = f"{student[0]}. {student[1]} <-\nMarks: {student[2]}\nInfo: {student[3]}"
    print("=========================")
    print(text)
    print("=========================")

def add_marks(student_id):
    student = repo.get_person_info(student_id)
    if student:
        to_add = input("Add marks in format: 1, 4, 3, 5: ")
        repo.add_marks(student_id, to_add)
        print(f"Marks [{to_add}] successfully added!")
    elif not student:
        print("Student not found")

def smart_update():
    try:
        student_id = int(input("\nEnter student's ID: "))
    except ValueError:
        print("Invalid ID")
        return

    student = repo.get_person_info(student_id)
    if not student:
        print("Student not found")
        return

    try:
        to_update = int(input("Type '1' to update name, '2' info, '3' both: "))
    except ValueError:
        print("Invalid input")
        return

    if to_update == 1:
        update_name = input("Enter new name: ").strip()
        repo.update_person_info(student_id, 1, update_name)
        print("Name updated successfully.")
    elif to_update == 2:
        update_info = input("Enter new info: ").strip()
        repo.update_person_info(student_id, 2, update_info)
        print("Info updated successfully.")
    elif to_update == 3:
        update_name_and_info = input("Enter new name and info separated by ';': ").strip()
        try:
            name, info = update_name_and_info.split(";")
        except ValueError:
            print("Incorrect format. Use 'Name;Info'")
            return
        repo.update_person_info(student_id, 3, f"{name.strip()};{info.strip()}")
        print("Name and info updated successfully.")
    else:
        print("Wrong option selected.")

def delete_student():
    student_id = input("Enter student's ID: ")
    if not student_id.isdigit():
        print("Invalid ID")
        return
    if repo.delete_person(student_id):
        print("Student deleted successfully!")
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
    user_data = input(ask_prompt).strip()

    parts = user_data.split(';')
    if len(parts) == 3:
        name, raw_marks, info = parts
    elif len(parts) == 2:
        name, raw_marks = parts
        info = None
    else:
        print("Incorrect format.")
        return

    name = name.strip()
    raw_marks = raw_marks.strip()

    raw_marks_clean = raw_marks.replace('[', '').replace(']', '').replace(' ', '')

    try:
        marks = '[]' if raw_marks_clean == '0' else str([int(m) for m in raw_marks_clean.split(",")])
    except ValueError:
        print("Invalid marks format. Use numbers like: 1,2,3 or 0")
        return

    add_student(name, marks, info)


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
    elif command == "delete student":
        delete_student()
    else:
        print("Command not found")

def main():
    OPERATIONAL_COMMANDS = ("quit", "help")
    STUDENT_MANAGEMENT_COMMANDS = ("show all", "add student", "show student", "add marks", "update student", "delete student")
    AVAILABLE_COMMANDS = (*OPERATIONAL_COMMANDS, *STUDENT_MANAGEMENT_COMMANDS)

    HELP_MESSAGE = ("\n-USAGE GUIDE-\nCommand |show all| - view all added students with their ids\n"
                    "Command |add student| - add a student\n"
                    "Command |show student| - show added student by its id\n"
                    "Command |update student| - to update student's name or information about student\n"
                    "Command |add marks| - add marks to the student\n"
                    "Command |delete student| - to delete student\n"
                    "Command |quit| - quit digital journal")

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