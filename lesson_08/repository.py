import random
import datetime


class StudentsRepository:
    students_count = 0
    ids_for_students = list(range(100000, 200000))

    def __init__(self):
        self.students = {}
        """
        students: {int: [str, str|None, {data.today(): []}]}
        """

    async def add_student(self, name, marks, info):
        today = datetime.date.today()
        StudentsRepository.students_count += 1
        student_id = random.choice(StudentsRepository.ids_for_students)
        StudentsRepository.ids_for_students.remove(student_id)
        self.students[student_id] = [name, info, {today: marks}]

    async def show_student(self, student_id: int):
        try:
            return self.students[student_id]
        except KeyError:
            return None

    async def show_students(self):
        return self.students

    async def update_student(self, student_id: int, name: str=None, info: str=None, marks: list=None):
        today =datetime.date.today()
        if name and info:
            self.students[student_id][0] = name
            self.students[student_id][1] = info
        elif name and not info:
            self.students[student_id][0] = name
        elif info and not name:
            self.students[student_id][1] = info
        elif marks:
            day_marks = self.students[student_id][2].setdefault(today, [])
            day_marks.extend(marks)

    async def delete_student(self, student_id):
        del self.students[student_id]
        StudentsRepository.students_count -= 1

    def get_all_marks_today(self) -> list[int]:
        today_marks = []
        today_str = datetime.date.today()
        for student in self.students.values():
            marks_dict = student[2]
            for data, marks in marks_dict.items():
                if data == today_str:
                    today_marks.extend(marks)
        return today_marks

    def get_all_marks_per_month(self) -> list[int]:
        month_marks = []
        today = datetime.date.today()
        for student in self.students.values():
            marks_dict = student[2]
            for date_obj, marks in marks_dict.items():
                delta = today - date_obj
                if 0 <= delta.days < 30:
                    month_marks.extend(marks)
        return month_marks

repo = StudentsRepository()


