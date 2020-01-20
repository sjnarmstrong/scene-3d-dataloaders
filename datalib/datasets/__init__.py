from typing import Union
from pydantic import BaseModel
from .nyudataset import NYUDataset
from .scannet import ScannetDataset

Dataset = Union[NYUDataset, ScannetDataset]


class DatasetConfigContainer(BaseModel):
    dataset: Dataset
