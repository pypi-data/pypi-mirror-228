import logging
import os
import pickle
import warnings
from typing import Sequence
from . import env

import h5py

if env.package_available("pandas"):
    import pandas as pd

__all__ = ["mkdirs", "save_pik", "load_pik", "save_h5", "load_h5", "save_tables"]


def mkdirs(dir_path: str):
    """Make directory is directory does not exist.

    Args:
        dir_path (str): Directory path to make.

    Returns:
        str: path to directory
    """
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)

    return dir_path


def save_pik(file_path: str, data):
    """Save data using `pickle`.

    Pickle is not be stable across Python 2/3.

    Args:
        file_path (str): File path to save to.
        data (Any): Data to serialize.
    """
    mkdirs(os.path.dirname(file_path))
    with open(file_path, "wb") as f:
        pickle.dump(data, f)


def load_pik(file_path: str):
    """Load data using `pickle`.

    Should be used with :any:`save_pik`.

    Pickle is not be stable across Python 2/3.

    Args:
        file_path (str): File path to load from.

    Returns:
        Any: Loaded data.

    Raises:
        FileNotFoundError: If `file_path` does not exist.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError("{} does not exist".format(file_path))

    with open(file_path, "rb") as f:
        return pickle.load(f)


def save_h5(file_path: str, data_dict: dict):
    """Save data in H5DF format.

    Args:
        file_path (str): File path to save to.
        data_dict (dict): Dictionary of data to store. Dictionary can only have depth of 1.
    """
    mkdirs(os.path.dirname(file_path))
    with h5py.File(file_path, "w") as f:
        for key in data_dict.keys():
            f.create_dataset(key, data=data_dict[key])


def load_h5(file_path):
    """Load data in H5DF format.

    Args:
        file_path (str): File path to save to.

    Returns:
        dict: Loaded data.

    Raises:
        FileNotFoundError: If `file_path` does not exist.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError("{} does not exist".format(file_path))

    data = {}
    with h5py.File(file_path, "r") as f:
        for key in f.keys():
            data[key] = f.get(key).value

    return data


save_tables = None

if env.package_available("pandas"):
    def save_tables(
        file_path: str, data_frames: Sequence[pd.DataFrame], sheet_names: Sequence[str] = None
    ):
        """Save data in excel tables.

        Args:
            file_path (str): File path to excel file.
            data_frames (Sequence[pd.DataFrame]): Tables to store to excel file.
                One table stored per sheet.
            sheet_names (:obj:`Sequence[str]`, optional): Sheet names for each data frame.
        """

        mkdirs(os.path.dirname(file_path))
        writer = pd.ExcelWriter(file_path)

        if sheet_names is None:
            sheet_names = []
            for i in range(len(data_frames)):
                sheet_names.append("Sheet%d" % (i + 1))

        if len(data_frames) != len(sheet_names):
            raise ValueError("Number of data_frames and sheet_frames should be the same")

        for i in range(len(data_frames)):
            df = data_frames[i]
            df.to_excel(writer, sheet_names[i], index=False)

        writer.save()
else:
    def save_tables(*args, **kwargs):
        raise ImportError("Pandas is not installed. Install it with `pip install pandas`")
