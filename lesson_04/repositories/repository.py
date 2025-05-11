import csv
from csv import DictWriter
from pathlib import Path
from abc import ABC, abstractmethod

from lesson_02.main import students


class BasePersonRepository(ABC):

    @abstractmethod
    def get_info_of_all_persons(self):
        raise NotImplementedError

    @abstractmethod
    def get_person_info(self, person_id):
        raise NotImplementedError

    @abstractmethod
    def add_person(self, person_info):
        raise NotImplementedError

    @abstractmethod
    def update_person_info(self, person_id: int, option: int, person_info: str):
        raise NotImplementedError

    @abstractmethod
    def delete_person(self, person_id):
        raise NotImplementedError


class StudentRepository(BasePersonRepository):
    PATH = Path("storages/students_storage.csv")
    FIELDNAMES = ['id', 'name', 'marks', 'info']

    def get_info_of_all_persons(self):
        if self.PATH.exists():
            with open(self.PATH, 'r', newline='') as file:
                reader = csv.DictReader(file)
                rows = list(reader)
                # print(f"[DEBUG] Прочитано строк: {len(rows)}")
                if rows:
                    to_add = []
                    for row in rows:
                        # print(f"[DEBUG] raw row: {repr(row)}")
                        to_add.append(f"{row['id']};{row['name']}")
                    return to_add
                else:
                    return False
        else:
            self.PATH.parent.mkdir(parents=True, exist_ok=True)
            self.PATH.touch()
            with open(self.PATH, 'w') as file:
                writer = DictWriter(file, fieldnames=self.FIELDNAMES)
                writer.writeheader()
                print("Хранилище студентов инициализированно")
                return False

    def get_person_info(self, person_id):
        with open(self.PATH, 'r') as file:
            reader = csv.DictReader(file)
            for i in reader:
                if i['id'] == str(person_id):
                    return f"{i['id']};{i['name']};{i['marks']};{i['info']}"
            return False

    def add_person(self, person_info: str):
        # print(f"[DEBUG] received: {person_info}")
        student_info = person_info.split(';')
        # print(f"[DEBUG] split: {student_info}")
        with open(self.PATH, 'r') as file:
            reader = csv.DictReader(file)
            rows = list(reader)
            last_row_id = int(rows[-1]['id']) if rows else 0

        new_student = {
            self.FIELDNAMES[0]: str(last_row_id + 1),
            self.FIELDNAMES[1]: student_info[0],
            self.FIELDNAMES[2]: student_info[1],
            self.FIELDNAMES[3]: student_info[2]
        }


        with open(self.PATH, 'a') as file:
            writer = csv.DictWriter(file, fieldnames=self.FIELDNAMES)
            writer.writerow(new_student)
        return True

    def update_person_info(self, person_id: int, option: int, person_info: str):
        updated = False

        with open(self.PATH, 'r') as file:
            reader = csv.DictReader(file)
            rows = list(reader)

            for i in rows:
                if i['id'] == str(person_id):
                    updated = True
                    if option == 1:
                        for row in rows:
                            if row['id'] == str(person_id):
                                row['name'] = person_info
                                break
                    elif option == 2:
                        for row in rows:
                            if row['id'] == str(person_id):
                                row['info'] = person_info
                                break
                    elif option == 3:
                        name_and_info = person_info.split(';')
                        for row in rows:
                            if row['id'] == str(person_id):
                                row['name'] = name_and_info[0]
                                row['info'] = name_and_info[1]
                                break

        if updated:
            with open(self.PATH, 'w') as file:
                writer = csv.DictWriter(file, fieldnames=self.FIELDNAMES)
                writer.writeheader()
                writer.writerows(rows)
                return updated
        return False

    def delete_person(self, person_id: str):
        deleted = False

        with open(self.PATH, 'r') as file:
            reader = csv.DictReader(file)
            rows = list(reader)

        for idx, row in enumerate(rows):
            if row['id'] == str(person_id):
                del rows[idx]
                deleted = True
                break

        if deleted:
            with open(self.PATH, 'w') as file:
                writer = csv.DictWriter(file, fieldnames=self.FIELDNAMES)
                writer.writeheader()
                writer.writerows(rows)
                return deleted
        return False

    def add_marks(self, person_id: int, marks: str):
        with open(self.PATH, 'r') as file:
            reader = csv.DictReader(file)
            rows = list(reader)

        for row in rows:
            if row['id'] == str(person_id):
                marks_to_add = row['marks'][:-1] + ',' + marks + ']'
                row['marks'] = marks_to_add
                break
            else:
                return False

        with open(self.PATH, 'w') as file:
            writer = csv.DictWriter(file, fieldnames=self.FIELDNAMES)
            writer.writeheader()
            writer.writerows(rows)
        return True