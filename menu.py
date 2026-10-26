import dataclasses
from typing import Callable


@dataclasses.dataclass
class MenuItem:
    id: int
    behavior: str


MENU: list[MenuItem] = [
    # MenuItem(1, "download_from_dir"),
    # MenuItem(2, "upload_to_dir"),
    # MenuItem(3, "just_decipher"),
    # MenuItem(4, "unarchive"),
    MenuItem(1, "Yandex"),
    MenuItem(2, "Decipher"),
    MenuItem(3, "Unarchive")
]


def print_menu() -> str:
    for item in MENU:
        print(f"{item.id} | {item.behavior}")

    valid_ids = {item.id for item in MENU}
    while True:
        answer = input("> ").strip()
        if answer.lower() in ("q", "quit", "exit", "n", "e"):
            raise SystemExit(0)
        
        return str(answer)
        # if answer.isdigit() and int(answer) in valid_ids:
        #     return int(answer)
        # print(f"Invalid choice. Pick one of {sorted(valid_ids)} or 'q' to quit.")