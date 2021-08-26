"""
PyTorch Snowflake Image Folder Data Class

This class is an extension of PyTorch image data objects to allow 
loading image files from a Snowflake unstructured table. 
Learn more at https://quickstarts.snowflake.com/.
"""

import tempfile
from os.path import basename, dirname
from typing import List, Callable, Optional
from PIL import Image
from torch.utils.data import Dataset
import numpy as np, pandas as pd # pylint: disable=import-error
import requests, io, os, datetime, re # pylint: disable=import-error


def _list_all_files(table_name: str, relative_path_col: str, stage: str, conn):
    """
    Get dataframe of all items from table
    """

    df = pd.read_sql(
        f"select *, get_presigned_url(@{stage}, {relative_path_col}) as SIGNEDURL from {table_name}",
        conn,
    )
    return df


def _load_image_obj(fileobj):
    """
    Turn a byte file object into an image
    """

    return Image.open(io.BytesIO(fileobj)).convert("RGB")


class SnowflakeImageFolder(Dataset):
    """
    An image table that lives in Snowflake.
    relative path: the path containing the label for the image as the lowest folder
    url: the authenticated link allowing download of the file
    """

    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-arguments

    def __init__(
        self,
        table_name: str,
        relative_path_col: str,
        stage: str,
        connection,
        transform: Optional[Callable] = None,
        target_transform: Optional[Callable] = None,
    ):
        self.table_name = table_name
        self.connection = connection
        self.stage = stage
        self.relative_path_col = relative_path_col
        self.all_files = _list_all_files(
            self.table_name, self.relative_path_col, self.stage, self.connection
        )
        self.classes = sorted(
            {self._get_class(x[self.relative_path_col]) for j, x in self.all_files.iterrows()}
        )

        self.class_to_idx = {k: idx for idx, k in enumerate(self.classes)}
        self.transform = transform
        self.target_transform = target_transform

    @classmethod
    def _get_class(cls, path):
        """
        Parse the relative path to extract the class name
        """
        return basename(dirname(path))

    def __getitem__(self, idx):
        """
        Get the nth (idx) row
        """
        path = self.all_files.iloc[idx]
        label = self.class_to_idx[self._get_class(path[self.relative_path_col])]

        with tempfile.TemporaryFile() as f:
            f = requests.get(path["SIGNEDURL"]).content
            img = _load_image_obj(f)
        if self.transform is not None:
            img = self.transform(img)
        if self.target_transform is not None:
            label = self.target_transform(label)
        return img, label

    def __len__(self):
        """
        Total number of images
        """
        return len(self.all_files)
