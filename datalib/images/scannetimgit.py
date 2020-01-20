from enum import Enum
from typing import Set
from datalib.filehandlers.scannetsens import SensFileHandler, RGBDFrame
from datetime import datetime


class ReturnableItem(Enum):
    DEPTH_IMAGE = 1
    COLOR_IMAGE = 2
    CAMERA_TO_WORLD = 3
    TIMESTAMP = 4
    FRAME_NR = 5
    SEGMENTATION_2D = 6
    REPROJECTION = 7


class ScannetImgIt:
    def __init__(self, items_to_return: Set[ReturnableItem], sens_file: SensFileHandler, label_converter=None):
        self.items_to_return = items_to_return
        self.label_converter = label_converter
        self.sens_file = sens_file

        self.start_time = datetime.timestamp(datetime.now())
        self.time_increments = 1 / 60.0

    def extract_data(self, rgbd_frame: RGBDFrame, frame_nr: int):
        ret = []
        for item in self.items_to_return:
            if item == ReturnableItem.DEPTH_IMAGE:
                ret.append( rgbd_frame.get_depth_image() )
            elif item == ReturnableItem.COLOR_IMAGE:
                ret.append( rgbd_frame.get_color_image() )
            elif item == ReturnableItem.CAMERA_TO_WORLD:
                ret.append( rgbd_frame.camera_to_world() )
            elif item == ReturnableItem.TIMESTAMP:
                ret.append( self.time_increments * frame_nr + self.start_time )
            elif item == ReturnableItem.FRAME_NR:
                ret.append( frame_nr )
            elif item == ReturnableItem.SEGMENTATION_2D:
                raise NotImplementedError  # TODO
            elif item == ReturnableItem.REPROJECTION:
                raise NotImplementedError  # TODO

    def __getitem__(self, index):
        with self.sens_file.open() as sfp:
            return self.extract_data(sfp[index], index)

    def __iter__(self):
        with self.sens_file as sfp:
            for i, val in enumerate(self.sfp):
                yield self.extract_data(val, i)

    def __len__(self):
        return len(self.sens_file)

    @property
    def intrinsic_rgb(self):
        if self.sens_file.intrinsic_color is None:
            self.sens_file.read_header()
        return self.sens_file.intrinsic_color

    @property
    def intrinsic_depth(self):
        if self.sens_file.intrinsic_depth is None:
            self.sens_file.read_header()
        return self.sens_file.intrinsic_depth

    @property
    def extrinsic_rgb(self):
        if self.sens_file.extrinsic_color is None:
            self.sens_file.read_header()
        return self.sens_file.extrinsic_color

    @property
    def extrinsic_depth(self):
        if self.sens_file.extrinsic_depth is None:
            self.sens_file.read_header()
        return self.sens_file.extrinsic_depth

    @property
    def depth_scale(self):
        if self.sens_file.depth_shift is None:
            self.sens_file.read_header()
        return self.sens_file.depth_shift

    @property
    def rgb_size(self):
        if self.sens_file.color_height is None:
            self.sens_file.read_header()
        return self.sens_file.color_height, self.sens_file.color_width

    @property
    def depth_size(self):
        if self.sens_file.depth_height is None:
            self.sens_file.read_header()
        return self.sens_file.depth_height, self.sens_file.depth_width
