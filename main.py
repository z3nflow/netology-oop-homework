class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def rate_lecturer(self, lecturer, course, grade):
        if (
                not isinstance(lecturer, Lecturer)
                or course not in self.courses_in_progress
                or course not in lecturer.courses_attached
                or not isinstance(grade, int)
                or not 1 <= grade <= 10
        ):
            return 'Ошибка'

        if course in lecturer.grades:
            lecturer.grades[course] += [grade]
        else:
            lecturer.grades[course] = [grade]
        return None

    def _avg_hw(self):
        all_grades = []
        for grades in self.grades.values():
            for grade in grades:
                all_grades.append(grade)
        if all_grades:
            return sum(all_grades) / len(all_grades)
        return 0.0

    def __str__(self):
        avg = self._avg_hw()
        in_progress = ", ".join(self.courses_in_progress)
        finished = ", ".join(self.finished_courses)
        return (
            f"Имя: {self.name}\n"
            f"Фамилия: {self.surname}\n"
            f"Средняя оценка за домашние задания: {avg:.1f}\n"
            f"Курсы в процессе изучения: {in_progress}\n"
            f"Завершенные курсы: {finished}"
        )

    def __lt__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self._avg_hw() < other._avg_hw()

    def __le__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self._avg_hw() <= other._avg_hw()

    def __gt__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self._avg_hw() > other._avg_hw()

    def __ge__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self._avg_hw() >= other._avg_hw()

    def __eq__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return round(self._avg_hw(), 2) == round(other._avg_hw(), 2)


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def _avg_lectures(self):
        all_grades = []
        for grades in self.grades.values():
            for grade in grades:
                all_grades.append(grade)
        if all_grades:
            return sum(all_grades) / len(all_grades)
        return 0.0

    def __str__(self):
        avg = self._avg_lectures()
        return (
            f"Имя: {self.name}\n"
            f"Фамилия: {self.surname}\n"
            f"Средняя оценка за лекции: {avg:.1f}"
        )

    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self._avg_lectures() < other._avg_lectures()

    def __le__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self._avg_lectures() <= other._avg_lectures()

    def __gt__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self._avg_lectures() > other._avg_lectures()

    def __ge__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self._avg_lectures() >= other._avg_lectures()

    def __eq__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return round(self._avg_lectures(), 2) == round(other._avg_lectures(), 2)


class Reviewer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)

    def rate_hw(self, student, course, grade):
        if (
                not isinstance(student, Student)
                or course not in self.courses_attached
                or course not in student.courses_in_progress
                or not isinstance(grade, int)
                or not 1 <= grade <= 10
        ):
            return 'Ошибка'

        if course in student.grades:
            student.grades[course] += [grade]
        else:
            student.grades[course] = [grade]
        return None

    def __str__(self):
        return f"Имя: {self.name}\nФамилия: {self.surname}"


def avg_hw_for_course(students, course):
    """Средняя оценка за ДЗ по всем студентам на конкретном курсе."""
    all_grades = []
    for student in students:
        if isinstance(student, Student) and course in student.grades:
            for g in student.grades[course]:
                all_grades.append(g)
    if all_grades:
        return sum(all_grades) / len(all_grades)
    return 0.0


def avg_lectures_for_course(lecturers, course):
    """Средняя оценка за лекции по всем лекторам на конкретном курсе."""
    all_grades = []
    for lecturer in lecturers:
        if isinstance(lecturer, Lecturer) and course in lecturer.grades:
            for g in lecturer.grades[course]:
                all_grades.append(g)
    if all_grades:
        return sum(all_grades) / len(all_grades)
    return 0.0


# Создаём по 2 экземпляра каждого класса
s1 = Student("Иван", "Петров", "m")
s2 = Student("Мария", "Иванова", "f")

l1 = Lecturer("Анна", "Смирнова")
l2 = Lecturer("Павел", "Кузнецов")

r1 = Reviewer("Олег", "Будин")
r2 = Reviewer("Елена", "Ромашина")

# Привязываем курсы
python = "Python"
git = "Git"
intro_course = "Введение в программирование"

s1.courses_in_progress += [python, git]
s2.courses_in_progress += [python]

l1.courses_attached += [python]
l2.courses_attached += [git, python]

r1.courses_attached += [python]
r2.courses_attached += [git]

# всем студентам — завершённый курс
s1.finished_courses.append(intro_course)
s2.finished_courses.append(intro_course)

# Выставляем оценки
r1.rate_hw(s1, python, 10)
r1.rate_hw(s1, python, 9)
r1.rate_hw(s2, python, 8)

r2.rate_hw(s1, git, 7)
r2.rate_hw(s1, git, 8)

s1.rate_lecturer(l1, python, 10)
s2.rate_lecturer(l1, python, 9)

s1.rate_lecturer(l2, git, 8)
s1.rate_lecturer(l2, python, 9)

# Печать с отступами между объектами
print("--- Reviewers ---")
print(r1, end="\n\n")
print(r2, end="\n\n")

print("--- Lecturers ---")
print(l1, end="\n\n")
print(l2, end="\n\n")

print("--- Students ---")
print(s1, end="\n\n")
print(s2, end="\n\n")

# Сравнения
print("s1 > s2:", s1 > s2)
print("l1 < l2:", l1 < l2, end="\n\n")

# Средние оценки по курсам
avg_students_python = avg_hw_for_course([s1, s2], python)
avg_lecturers_python = avg_lectures_for_course([l1, l2], python)

avg_students_git = avg_hw_for_course([s1, s2], git)
avg_lecturers_git = avg_lectures_for_course([l1, l2], git)

print(f"Средняя оценка за выполнение ДЗ по {python}: {avg_students_python:.2f}")
print(f"Средняя оценка проведенных лекций по {python}: {avg_lecturers_python:.2f}")
print(f"Средняя оценка за выполнение ДЗ по {git}: {avg_students_git:.2f}")
print(f"Средняя оценка проведенных лекций по {git}: {avg_lecturers_git:.2f}")
