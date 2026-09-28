import sqlite3


def get_status(grade):
    if grade >= 18:
        return "عالی"
    elif 14 <= grade < 18:
        return "خوب"
    elif 10 <= grade < 14:
        return "قبول"
    else:
        return "مردود"



class Student:
    def __init__(self, name, grade, class_name):
        self.name = name
        self.grade = grade
        self.class_name = class_name

    @property
    def grade(self):
        return self._grade


    @grade.setter
    def grade(self, new_grade):
        if new_grade < 0 or new_grade > 20:
            print("نمره باید بین 0 تا 20 باشد")
            return
        self._grade = new_grade

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        if new_name.strip() == "":
            print("نام نمی‌تواند خالی باشد")
            return
        self._name = new_name



    def show_info(self):
        print(f"نام: {self.name}")
        print(f"نمره: {self.grade}")
        print(f"کلاس: {self.class_name}")
        print(f"وضعیت: {get_status(self.grade)}")

    def is_passed(self):
        return self.grade >= 10


class StudentManager:

    def __init__(self):
        self.connection = sqlite3.connect("students.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS students(id INTEGER PRIMARY KEY, name TEXT, grade REAL, class_name TEXT)")
        self.connection.commit()

    def add_student(self, student):
        if self.is_duplicate(student.name):
            print(f"دانش اموز از قبل ثبت شده {student.name}")
        else:
            print("دانش اموز با موفقیت ثبت شد")
            self.cursor.execute("INSERT INTO students(name, grade, class_name) VALUES(?, ?, ?)", (student.name, student.grade, student.class_name))
            self.connection.commit()

    def show_students(self):
        self.cursor.execute("SELECT * FROM students")
        rows = self.cursor.fetchall()
        for row in rows:
            print(f"نام: {row[1]}")
            print(f"نمره: {row[2]}")
            print(f"کلاس: {row[3]}")
            print(f" وضعیت :{get_status(row[2]) }")

    def find_student(self, name):
        if not name.strip():
            return

        search_pattern = "%" + name + "%"
        self.cursor.execute("SELECT * FROM students WHERE name LIKE ?", (search_pattern,))
        rows = self.cursor.fetchall()
        if not rows:
            print("دانش‌آموز پیدا نشد")
            return

        for row in rows:
            print(f"نام: {row[1]}")
            print(f"نمره: {row[2]}")
            print(f"کلاس: {row[3]}")
            print(f" وضعیت :{get_status(row[2])}")


    def remove_student(self, name):
        if not name.strip():
            print("لطفا نام دانش اموز را وارد نمایید")
            return
        try:
            self.cursor.execute("DELETE FROM students WHERE name = ?", (name,))
            self.connection.commit()
            if self.cursor.rowcount == 0:
                print("دانش اموز پیدا نشد")
            else:
                print("دانش اموز با موفقیت حذف شد")
        except sqlite3.OperationalError:
            self.connection.rollback()
            print("خطا در حذف دانش‌آموز")
            return



    def update_grade(self, name, new_grade):
        if new_grade < 0 or new_grade > 20:
            print("نمره باید بین 0 تا 20 باشد")
            return

        self.cursor.execute("UPDATE students SET grade = ? WHERE name = ?", (new_grade, name))
        self.connection.commit()
        if self.cursor.rowcount == 0:
            print("دانش اموز پیدا نشد")
        else:
            print("دانش اموز با موفقیت ویرایش شد")

    def average_grade(self):
        self.cursor.execute("SELECT AVG(grade) FROM students")
        result = self.cursor.fetchone()
        if result[0] is None:
            print("هیچ نمره ای ثبت نشده")
        else:
            print(f"میانگین نمرات: {result[0]:.2f}")


    def is_duplicate(self, name):
        self.cursor.execute("SELECT * FROM students WHERE name = ?", (name,))
        result = self.cursor.fetchone()
        if result is None:
            return False
        else:
            return True


    def best_students(self):
        self.cursor.execute("SELECT * FROM students WHERE grade = (SELECT MAX(grade) FROM students)")
        rows = self.cursor.fetchall()
        if not rows:
            print("هیچ دانش‌آموزی ثبت نشده")
        else:
            for row in rows:
                print(f"نام: {row[1]}")
                print(f"نمره: {row[2]}")
                print(f"کلاس: {row[3]}")
                print(f" وضعیت :{get_status(row[2])}")


    def worst_students(self):
        self.cursor.execute("SELECT * FROM students WHERE grade = (SELECT MIN(grade) FROM students)")
        rows = self.cursor.fetchall()
        if not rows:
            print("هیچ دانش‌آموزی ثبت نشده")
        else:
            for row in rows:
                print(f"نام: {row[1]}")
                print(f"نمره: {row[2]}")
                print(f"کلاس: {row[3]}")
                print(f" وضعیت :{get_status(row[2])}")

    def filter_by_class(self, class_name):
        self.cursor.execute("SELECT * FROM students WHERE class_name = ?", (class_name,))
        rows = self.cursor.fetchall()
        if not rows:
            print("هیچ دانش اموزی ثبت نشده")
        else:
            for row in rows:
                print(f"نام: {row[1]}")
                print(f"نمره: {row[2]}")
                print(f"کلاس: {row[3]}")
                print(f" وضعیت :{get_status(row[2])}")

    def count_students(self):
        self.cursor.execute("SELECT COUNT(*) FROM students")
        result = self.cursor.fetchone()
        print(f"تعداد دانش اموزان {result[0]} ")


    def sort_by_grade(self, order):
        if order == "1":
            direction = "ASC"
        else:
            direction = "DESC"

        self.cursor.execute(f"SELECT * FROM students ORDER BY grade {direction}")
        rows = self.cursor.fetchall()
        if not rows:
            print("هیچ دانش اموزی ثبت نشده")
        else:
            for row in rows:
                print(f"نام: {row[1]}")
                print(f"نمره: {row[2]}")
                print(f"کلاس: {row[3]}")
                print(f" وضعیت :{get_status(row[2])}")


    def edit_student(self, old_name, new_name, new_grade, new_class_name):
        if new_grade < 0 or new_grade > 20:
            print("نمره باید بین 0 تا 20 باشد")
            return
        self.cursor.execute("UPDATE students SET name = ?, grade = ?, class_name = ?  WHERE name = ? ", (new_name, new_grade, new_class_name, old_name))
        self.connection.commit()
        if self.cursor.rowcount == 0:
            print("هیچ دانش اموزی پیدا نشد")
        else:
            print("ویرایش با موفقیت انجام شد")



manager = StudentManager()

while True:
    print("1.اضافه کردن دانش اموز")
    print("2. نمایش دانش اموزان")
    print("3. جستو و جوی دانش اموز")
    print("4.حدف دانش اموزا")
    print("5. ویرایش نمره دانش اموز")
    print("6.میانگین نمرات")
    print("7. بهترین دانش اموز")
    print("8. ضعیف ترین دانش اموز")
    print("9. فیلتر بر اساس کلاس")
    print("10. تعداد دانش اموزان")
    print("11. مرتب‌سازی بر اساس نمره")
    print("12.ویرایش اطلاعات دانش اموز")
    print("13. خروج")

    try:
        choice = int(input("گزینه مورد نظر را وارد کنید: "))
    except ValueError:
        print("لطفاً یک عدد معتبر وارد کنید.")
        continue

    if choice == 1:
        student_name = input("نام دانش اموز: ")
        if not student_name.strip():
            print("لطفا نام دانش اموز را وارد نمایید")
            continue
        try:
            student_grade = float(input("نمره دانش اموز: "))
        except ValueError:
            print("نمره باید عدد باشد.")
            continue
        student_class_name = input("کلاس: ")
        manager.add_student(Student(student_name, student_grade, student_class_name))

    elif choice == 2:
        manager.show_students()

    elif choice == 3:
        search_name = input("اسم دانش اموز را وارد نمایید: ")
        manager.find_student(search_name)

    elif choice == 4:
        search_name = input("اسم دانش اموز را وارد نمایید: ")
        manager.remove_student(search_name)

    elif choice == 5:
        search_name = input("اسم دانش اموز را وارد نمایید: ")
        try:
            student_grade = float(input("نمره مورد نظر را وارد نمایید: "))
        except ValueError:
            print("نمره باید عدد باشد.")
            continue
        manager.update_grade(search_name, student_grade)

    elif choice == 6:
        manager.average_grade()

    elif choice == 7:
        manager.best_students()

    elif choice == 8:
        manager.worst_students()

    elif choice == 9:
        manager.filter_by_class(class_name = input("نام کلاس را وارد کنید: "))

    elif choice == 10:
        manager.count_students()

    elif choice == 11:
        order = input("  مرتب سازی بر اساس صعودی گزینه 1 و مرتب سازی بر اساس نزولی گزینه 2: ")
        manager.sort_by_grade(order)

    elif choice == 12:
        old_name = input("اسم دانش اموز مورد نظر را وارد نمایید: ")
        new_name = input("اسم دانش اوز راورد نمایید : ")
        try:
            new_grade = float(input("نمرهه انش اموز را وارد نمیایید : "))
            new_class_name = input("کلاس داش اموز را وارد نمایید")
            manager.edit_student(old_name, new_name, new_grade, new_class_name)
        except ValueError:
            print("نمره باید به عدد باشه")


    elif choice == 13:
        print("...خروج از برنامه")
        break
    else:
        print(".گزینه وارد شده معتبر نیست")

# Git test
# This change is only for test branch
# Testing Pull Request