import types as t
import dataclasses


@dataclasses.dataclass
class Menu:
    id: int
    behavior: str


menu: list[Menu] = [
    Menu(
        1,
        "download_from_dir",
    ),
    Menu(
        2,
        "upload_to_dir",
    ),
]


def print_menu() -> int:
    for n in menu:
        print(f"{n.id} | {n.behavior}")
    answer = input()
    if answer == "n":
        exit(0)

    return int(answer)
