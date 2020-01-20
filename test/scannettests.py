import unittest
from datalib.datasets import DatasetConfigContainer
import open3d as o3d

path_to_scannet_dataset = "/mnt/1C562D12562CEDE8/DATASETS/csv_conf/scenenn_mock_hd.csv"


class TestScannetDataset(unittest.TestCase):
    def test_scenes_load(self):
        dataset_config = DatasetConfigContainer(dataset={
            "ID": "Scannet",
            "file_map": path_to_scannet_dataset,
        })
        assert len(dataset_config.dataset.scenes) == 3

    def test_show_pcd(self):
        dataset_config = DatasetConfigContainer(dataset={
            "ID": "Scannet",
            "file_map": path_to_scannet_dataset,
        })
        pcd = dataset_config.dataset.scenes[0].reconstruction.pcd
        o3d.display((pcd,))