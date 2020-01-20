from datalib.reconstruction.scannetrec import ScannetRec
from datalib.images.scannetimgit import ScannetImgIt, ReturnableItem
from typing import Set
from datalib.filehandlers.scannetsens import SensFileHandler


class ScannetScene:
    def __init__(self, scene_id, info_path, sens_path, mesh_path, segmentation_map, aggregation_map,
                 projected_instance_archive, projected_label_file, labelled_pcd_file, label_converter=None):
        super().__init__()
        self.scene_id = scene_id
        self.info_path = info_path
        self.sens_path = sens_path
        self.mesh_path = mesh_path
        self.segmentation_map = segmentation_map
        self.aggregation_map = aggregation_map
        self.projected_instance_archive = projected_instance_archive
        self.projected_label_file = projected_label_file
        self.labelled_pcd_file = labelled_pcd_file
        self.label_converter = label_converter

    def get_image_it(self, items_to_return: Set[ReturnableItem], sens_file: SensFileHandler, label_converter=None) -> \
            ScannetImgIt:
        return ScannetImgIt(items_to_return, sens_file, label_converter)

    @property
    def reconstruction(self) -> ScannetRec:
        return ScannetRec(self)




