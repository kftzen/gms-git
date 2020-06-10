from download_asa import WebBrowser
import pandas as pd
from zipfile import ZipFile
from pathlib import Path


class FileManager:

    asa_path = Path("./files/asa/").resolve()
    tmp_path = Path("./files/tmp/").resolve()

    def __init__(self):
        data_frame = FileManager._get_data_frame()
        acels = set(data_frame['Aceleracion max (cm/s**2)'])
        self.acels = acels
        self.data_frame = data_frame

    @staticmethod
    def _get_data_frame():
        data_frame = pd.read_csv('./files/data_base.csv',
                                 header=0,
                                 engine='c')
        return data_frame

    @staticmethod
    def _extract_asa():

        asa_path = FileManager.asa_path
        tmp_path = FileManager.tmp_path

        while True:
            try:
                file = tmp_path.iterdir().__next__()
                with ZipFile(file) as zip_file:
                    zip_file.extractall(asa_path)
                file.unlink()
                break
            except:
                pass

    def download_files(self):
        acels = self.acels
        tmp_path = FileManager.tmp_path
        tmp_path.mkdir()

        web_browser = WebBrowser(tmp_path)
        print("login in browser")
        web_browser.login()
        for accel in acels:
            print(f"Download files for an acceleration of {accel}")
            web_browser.download(accel)
            print("Extracting files")
            FileManager._extract_asa()

if __name__ == '__main__':
    fm = FileManager()
    fm.download_files()
