from .seg import Seg


class Seg2D(Seg):
    def __init__(self, image_shape, instance_masks, instance_classes, confidence_scores):
        self.image_shape = image_shape
        super().__init__(
            instance_masks.reshape((instance_masks.shape[0], -1)),
            instance_classes,
            confidence_scores,
        )
