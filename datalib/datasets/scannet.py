from .dataset import BaseDataset, Literal, Iterable
import lazy_import
from datalib.util.logging import logger

os = lazy_import.lazy_module("os")
csv = lazy_import.lazy_module("csv")


class ScannetDataset(BaseDataset):
    # Used to identify the dataset
    ID: Literal['Scannet']
    # Used to map all the files in the dataset. Contains 2 columns "SCENE_PATH" and "USE_HD"
    file_map: str
    HD_PATHS = ("{scene_id}.txt", "{scene_id}.sens", "{scene_id}_vh_clean.ply", "{scene_id}_vh_clean.segs.json",
                "{scene_id}.aggregation.json", "{scene_id}_2d-instance-filt.zip",
                "{scene_id}_2d-label-filt.zip", "{scene_id}_vh_clean_2.labels.ply")
    # using other agg file but either should be fine
    DEDIMATED_PATHS = ("{scene_id}.txt", "{scene_id}.sens", "{scene_id}_vh_clean_2.ply",
                       "{scene_id}_vh_clean_2.0.010000.segs.json", "{scene_id}_vh_clean.aggregation.json",
                       "{scene_id}_2d-instance-filt.zip", "{scene_id}_2d-label-filt.zip",
                       "{scene_id}_vh_clean_2.labels.ply")

    @property
    def scenes(self) -> Iterable:
        """
        Loads the various scenes in the Scannet dataset
        :return: None
        """

        self.base_path = os.path.split(self.file_map)[0]
        self.scenes = []

        with open(self.file_map, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                scene_path = row['SCENE_PATH']
                scene_id = os.path.split(scene_path)[-1]
                use_hd = row['USE_HD']
                scene_paths = ScannetDataset.HD_PATHS if use_hd else ScannetDataset.DEDIMATED_PATHS
                formatted_paths = [f"{self.base_path}/{scene_path}/{pth.format(scene_id=scene_id)}"
                                   for pth in scene_paths]
                scene = ScannetScene(scene_id, *formatted_paths)
                self.scenes.append(scene)

        logger.info(f"Loaded {len(self.scenes)} scenes from {self.file_map}")

