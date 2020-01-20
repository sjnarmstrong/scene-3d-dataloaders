import numpy as np
import json
import open3d as o3d
from datalib.segmentation.seg3d import Seg3D
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from datalib.scenes.scannetscene import ScannetScene


class ScannetRec:
    def __init__(self, scene: 'ScannetScene'):
        self.scene = scene

    def get_accociated_pcd(self):
        raise NotImplementedError

    def show_pcd(self, pcd=None):
        if pcd is None:
            pcd_to_show = [self.pcd]
        elif isinstance(pcd, list) or isinstance(pcd, tuple):
            pcd_to_show = pcd
        else:
            pcd_to_show = [pcd]
        o3d.visualization.draw_geometries(pcd_to_show)

    @property
    def pcd(self):
        return o3d.io.read_point_cloud(self.scene.mesh_path)

    @property
    def labelled_pcd(self):
        with open(self.scene.segmentation_map) as fp:
            seg_indices = np.array(json.load(fp)['segIndices'])
        with open(self.scene.aggregation_map) as fp:
            seg_groups = json.load(fp)['segGroups']
        instance_masks = np.array([np.in1d(seg_indices, seg_group['segments']) for seg_group in seg_groups])
        mask_labels = [seg_group['label'] for seg_group in seg_groups]
        return Seg3D(self.pcd, instance_masks, mask_labels)
