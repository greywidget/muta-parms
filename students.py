from rich import pretty, print

pretty.install()


def enroll_student(name, students=None):
    if students is None:
        students = []
    students.append(name)
    return students


def main():
    print(enroll_student("Biffa", students=["Spadger", "Morris"]))
    print(enroll_student("Moose"))
    print(enroll_student("Cheeseman"))


if __name__ == "__main__":
    main()
