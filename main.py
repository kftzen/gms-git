from zipfile import ZipFile, BadZipFile
from pathlib import Path
from pandas.errors import ParserError, EmptyDataError
import pandas as pd
from download_asa import WebBrowser
from ground_motion import GroundMotion


class FileManager:

    asa_path = Path("./files/asa/")
    tmp_path = Path("./files/tmp/")

    def __init__(self):

        def _retrive_downloaded_files():
            asa_path = FileManager.asa_path
            file_names = FileManager._get_data_frame('Archivo')
            files = []
            for file_name in file_names:
                file_path = asa_path / file_name
                if file_path.exists():
                    files.append(file_path.name)
            return files

        files = _retrive_downloaded_files()
        ground_motions = [GroundMotion(file) for file in files]
        self.ground_motions = ground_motions

    @staticmethod
    def _get_data_frame(column=None):
        data_frame = pd.read_csv('./files/data_base.csv',
                                 header=0,
                                 engine='c')
        if not column is None:
            data_frame = data_frame[column]
        return data_frame

    def download(self):

        tmp_path = FileManager.tmp_path
        asa_path = FileManager.asa_path

        def _retrive_remaining_accels():
            files = [file.name for file in self.ground_motions]
            data_frame = FileManager._get_data_frame()
            bool_serie = data_frame['Archivo'].isin(files)
            accels = data_frame[~bool_serie]['Aceleracion max (cm/s**2)']
            accels = set(accels)
            return accels

        def _extract_asa():
            while True:
                try:
                    file = [file for file in tmp_path.iterdir()].pop()
                    with ZipFile(file) as zip_file:
                        zip_file.extractall(asa_path)
                    print("Removing zip file")
                    file.unlink()
                    break
                except (BadZipFile, FileNotFoundError, IndexError):
                    pass

        tmp_path.mkdir()
        web_browser = WebBrowser(tmp_path.resolve())
        print("Login on to Data Base")
        web_browser.login()
        print("Retriving accelerations to be downloaded")
        accels = _retrive_remaining_accels()
        for accel in accels:
            print(f"Downloading files for an acceleration \
                of {accel}")
            web_browser.download(accel)
            print("Extracting files")
            _extract_asa()

    def convert_asa_to_hdf(self):
        ground_motions = self.ground_motions
        for events in ground_motions:
            try:
                print(f"Exporting {events.name} file")
                events.export_to_hdf5()
            except FileNotFoundError:
                print(f"File {events.name} is not downloaded")
            except (ParserError, EmptyDataError):
                print(f"File {events.name} isn't viable")

    def generate_pseudo_accel(self):
        ground_motions = self.ground_motions
        for events in ground_motions:
            events.generate_pseudo_accel()
if __name__ == '__main__':
    fm = FileManager()
    fm.convert_asa_to_hdf()
