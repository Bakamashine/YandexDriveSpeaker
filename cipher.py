import os
import shutil

import gnupg

from env import try_get_value


def find_gpg() -> str | None:
    """Locate the gpg executable, even when it is not on PATH."""
    for name in ("gpg", "gpg2"):
        path = shutil.which(name)
        if path:
            return path
    for base in (os.environ.get("ProgramFiles"), os.environ.get("ProgramFiles(x86)")):
        if base:
            path = os.path.join(base, "GnuPG", "bin", "gpg.exe")
            if os.path.exists(path):
                return path
    return None


class Cipher:
    def __init__(self, public: str | None = None, private: str | None = None):
        self.public = public or "public.asc"
        self.private = private or "private.asc"
        self.passphrase = try_get_value("cipher_passphrase")
        self.deciphered_dir = "dec"
        self.gnupghome = ".gnupg"

        gpgbinary = find_gpg()
        if gpgbinary is None:
            raise RuntimeError("gpg was not found. Install GnuPG or add it to PATH.")

        os.makedirs(self.gnupghome, exist_ok=True)
        self.gpg = gnupg.GPG(gpgbinary=gpgbinary, gnupghome=self.gnupghome)
        self.import_key(self.public)
        self.import_key(self.private)
        if os.path.exists(self.deciphered_dir) == False:
            os.makedirs(self.deciphered_dir)

    def import_key(self, path: str):
        if not os.path.exists(path):
            raise FileNotFoundError(f"Key file not found: {path}")
        with open(path, "rb") as f:
            result = self.gpg.import_keys(f.read())
        if result.count == 0:
            raise RuntimeError(f"Failed to import key: {path} ({result.stderr})")

    def decipher(self, fpfile: str) -> bool:
        name = os.path.basename(fpfile)
        stem, ext = os.path.splitext(name)
        if ext.lower() in (".gpg", ".pgp", ".asc"):
            name = stem
        new_file = os.path.join(self.deciphered_dir, f"{name}.zip")
        if os.path.exists(new_file):
            os.remove(new_file)

        with open(fpfile, "rb") as f:
            status = self.gpg.decrypt_file(
                f,
                passphrase=self.passphrase,
                output=new_file,
            )

        if not status.ok:
            print(f"Failed to decipher {fpfile}: {status.status} {status.stderr}")
            if os.path.exists(new_file):
                os.remove(new_file)
            return False

        print(f"Deciphered: {fpfile} -> {new_file}")
        return True

    def all_decipher(self, dir_name: str = "downloads") -> int:
        if not os.path.isdir(dir_name):
            print(f"Directory does not exist: {dir_name}")
            return 0

        files = sorted(
            name
            for name in os.listdir(dir_name)
            if name.lower().endswith((".gpg", ".pgp", ".asc"))
            and os.path.isfile(os.path.join(dir_name, name))
        )
        if not files:
            print("No encrypted files found")
            return 0

        deciphered = 0
        for name in files:
            file = os.path.join(dir_name, name)
            print(f"Deciphering file: {file}")
            if self.decipher(file):
                deciphered += 1

        print(
            f"Deciphered {deciphered} of {len(files)} file(s) into '{self.deciphered_dir}'"
        )
        return deciphered

    def cipher(self):
        pass
