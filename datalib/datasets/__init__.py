from typing import Union
from pydantic import BaseModel
from .nyudataset import NYUDataset

Dataset = Union['NYUDataset']


class DatasetConfigContainer(BaseModel):
    dataset: Dataset
