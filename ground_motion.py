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
        path = Path(f"./files/asa/{self.name}")
        if not path.exists():
            raise FileNotFoundError
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

    def _save_hdf5(self, data_frame):
        path = Path("./files/accel.h5")
        name = self.name.replace(".", "")
        with pd.HDFStore(path) as hdf_storage:
            hdf_storage[name] = data_frame

    def export_to_hdf5(self):
        data_frame = self._read_asa()
        self._save_hdf5(data_frame)
