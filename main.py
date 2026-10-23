import menu
from yandex_drive import YandexDrive
from env import get_value, try_get_value
from cipher import Cipher
from os import path
import shutil


def main():
    default_dir = "downloads"
    ydrive = YandexDrive(input("Your dir name: "), get_value("access_key"))
    cph = Cipher(try_get_value("public"), try_get_value("private"))

    if (
        path.exists(default_dir)
        and input("Downloads folder exists. Remove? [y/n] ") == "y"
    ):
        shutil.rmtree(default_dir)

    ydrive.parse_answer(menu.print_menu())
    cph.all_decipher(default_dir)


if __name__ == "__main__":
    main()
