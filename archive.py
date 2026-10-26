import os
import zipfile


class Archive:
    def __init__(self, dec_dir: str) -> None:
        if os.path.exists(dec_dir):
            self.dec_dir = dec_dir
            self.unarc_dir = "unarc"
        else:
            raise FileNotFoundError("dec_dir is not found")

    def unzip_all(self):
        os.makedirs(self.unarc_dir, exist_ok=True)
        for arc in os.listdir(self.dec_dir):
            print(f"Unarchive {arc} file..")
            with zipfile.ZipFile(os.path.join(self.dec_dir) + f"/{arc}", "r") as zip_ref:
                zip_ref.extractall(self.unarc_dir)
                print(f"Unarchive to {self.unarc_dir}/{os.path.basename(arc)}.zip")
