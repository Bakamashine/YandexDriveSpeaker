import menu
from yandex_drive import YandexDrive
from env import get_value, try_get_value
from cipher import Cipher
from os import path
import shutil
from archive import Archive


def main():
    default_dir = "downloads"
    ydrive = YandexDrive(try_get_value("access_key"))
    cph = Cipher(try_get_value("public"), try_get_value("private"))
    arc = Archive(cph.deciphered_dir)
    answer = menu.print_menu()
    answer_arr: list[int] = []
    for n in range(len(answer)):
        answer_arr.append(int(answer[n]))
    for n in answer_arr:
        if int(n) == 1:
            if (
                path.exists(default_dir)
                and input("Downloads folder exists. Remove? [y/n] ") == "y"
            ):
                shutil.rmtree(default_dir)
            ydrive.parse_answer(
                int(input("[Yandex drive] What are you want? (just int) "))
            )
        if n == 2:
            cph.all_decipher()
        if n == 3:
            arc.unzip_all()


if __name__ == "__main__":
    main()
