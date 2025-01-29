from rich import pretty, print

pretty.install()

FAB_FOUR = ["John", "Paul", "George", "Ringo"]


def meet_the_beetles(members) -> None:
    members.sort()
    print(f"   ...  {members}")


def main():
    print(f"Before: {FAB_FOUR}")
    meet_the_beetles(FAB_FOUR)
    print(f" After: {FAB_FOUR}")


if __name__ == "__main__":
    main()
