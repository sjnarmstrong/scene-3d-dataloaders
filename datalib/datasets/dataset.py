from typing_extensions import Literal
from pydantic import BaseModel
from typing import Iterable


class BaseDataset(BaseModel):
    ID: Literal['BaseDataset']

    @property
    def scenes(self) -> Iterable:
        """
        Loads the various scenes in a dataset
        :return: None
        """
        raise NotImplementedError

    @staticmethod
    def save(dataset: 'Dataset'):
        """
        Saves the dataset in the current format
        :param dataset: The dataset to save
        :return: None
        """
        raise NotImplementedError
