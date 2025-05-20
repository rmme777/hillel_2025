import enum
import datetime

class Role(enum.StrEnum):
    STUDENT = enum.auto()
    TEACHER = enum.auto()


class Notification:
    def __init__(self, subject: str, message: str, attachment: str = "") -> None:
        self.subject = subject
        self.message = message
        self.attachment = attachment

    def __str__(self) -> str:
        basic_format = (f"================\nSubject: {self.subject}\n{self.message}\n"
                        f"Attachment: {self.attachment}\n================")
        return basic_format


class User:
    def __init__(self, name: str, email: str, role: Role) -> None:
        self.name = name
        self.email = email
        self.role = role
        self.sender = (f"New notification from {self.role} {self.name}.\n{self.role}'s email: {self.email}"
                       f"\nSend data: {datetime.date}")

    def __str__(self) -> str:
        return self.sender

    def send_notification(self, message: str|Notification):
        notification = self.sender + '\n' + message
        print(notification)
        if self.role == Role.TEACHER:
            with open('teachers_desk.txt', 'a') as file:
                file.write(notification + f'\nSending time: {datetime.datetime.now()}\n\n')
        elif self.role == Role.STUDENT:
            with open('student_portal.txt', 'a') as file:
                file.write(notification + f'\nSending time: {datetime.datetime.now()}\n\n')



class StudentNotification(Notification):
    def to_send(self) -> str:
        return super().__str__() +"\n*Sent via Student Portal*"

class TeacherNotification(Notification):
    def to_send(self) -> str:
        return super().__str__() + "\n*Teacher's Desk Notification*"

def main():
    student = User("Sasha", "student.sasha@mgu.com", Role.STUDENT)
    teacher = User("Maria", "teacher.maria@mgu.com", Role.TEACHER)

    student_notification = StudentNotification('Problems with the toilet', 'Blablablablabla',
                                               "https://online-photos/photo/41234")
    student.send_notification(student_notification.to_send())
    print()
    teacher_notification = TeacherNotification("Math exam", "New math exam scheduled for Friday")
    teacher.send_notification(teacher_notification.to_send())

if __name__ == "__main__":
    main()

