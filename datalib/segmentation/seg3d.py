from .seg import Seg


class Seg3D(Seg):
    def __init__(self, pcd, instance_masks, instance_classes, confidence_scores=None):
        super().__init__(instance_masks, instance_classes, confidence_scores)
        self.pcd = pcd
        self.search_tree = None
