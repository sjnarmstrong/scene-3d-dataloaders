

class Seg:
    def __init__(self, instance_masks, instance_classes, confidence_scores=None):
        """

        :param classes: (N) -> int class_id
        :param instance_masks: (I, N) -> bool contains
        :param instance_classes: (I) -> int class_id
        :param confidence_scores: None | (I) -> float confidence
        """
        self.instance_masks = instance_masks
        self.instance_classes = instance_classes
        self.confidence_scores = confidence_scores
