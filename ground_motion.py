'''This modules provides Blah Vlah'''

from pathlib import Path
import pandas as pd
import numpy as np

class GroundMotion:
    '''This Class provides API for GroundMotion's'''
    def __init__(self, name):
        self.name = name
        self._acel = None
        self._pseudo = None

    @property
    def speudo(self):
        '''This property return the speudo value
        for that specific GroundMotion'''
        return self._pseudo

    @property
    def acel(self):
        '''This property returns the acceleration
        value for GroundMotion object'''
        self._read_acel()

    def _read_asa(self):
        path = Path("./files/asa/{}".format(self.name))
        data_frame = pd.read_csv(path,
                                 sep=r'\s+',
                                 header=None,
                                 dtype=np.float64,
                                 engine='c',
                                 skiprows=109,
                                 low_memory=False,
                                 memory_map=True,
                                 compression=None)
        return data_frame

    def _read_acel(self):
        path = Path("./files/asa.h5")
        try:
            data_frame = pd.read_hdf(path)
        except FileNotFoundError:
            path.touch()

class Manager:

    ground_motions = []

    @staticmethod
    def list_asa_files():
        path = Path("./files/asa")
        files = [f.name for f in path.iterdir()]
        return files

    @staticmethod
    def update_ground_motions():
        files = Manager.list_asa_files()
        Manager.ground_motions = [GroundMotion(f) for f in files]
        return Manager.ground_motions
