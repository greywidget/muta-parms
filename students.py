from rich import pretty, print

pretty.install()


def enroll_student(name, students=None):
    if students is None:
        students = []
    print(f"ID of students: {id(students)}")
    students.append(name)
    return students


def main():
    enroll_student("Moose")
    print(f"Function Default Values: {enroll_student.__defaults__}")
    print(f"ID of default_students: {id(enroll_student.__defaults__[0])}")


if __name__ == "__main__":
    main()
