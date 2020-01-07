import unittest
from datalib.datasets import DatasetConfigContainer

path_to_nyu_dataset_zip = "/media/sholto/Datasets/datasets/NYUv2/nyu_depth_v2_raw.zip"
path_to_nyu_dataset_gt_mat = "/media/sholto/Datasets/datasets/NYUv2/nyu_depth_v2_labeled.mat"


class TestNYUDataset(unittest.TestCase):
    def test_scenes_load(self):
        dataset_config = DatasetConfigContainer(dataset={
            "ID": "NYU",
            "zip_file_loc": path_to_nyu_dataset_zip,
            "gt_file_loc": path_to_nyu_dataset_gt_mat
        })
        assert len(dataset_config.dataset.scenes) == 412

