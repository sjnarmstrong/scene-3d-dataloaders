import struct
import numpy as np
import zlib
import imageio

COMPRESSION_TYPE_COLOR = {-1: 'unknown', 0: 'raw', 1: 'png', 2: 'jpeg'}
COMPRESSION_TYPE_DEPTH = {-1: 'unknown', 0: 'raw_ushort', 1: 'zlib_ushort', 2: 'occi_ushort'}


class RGBDFrame(object):

    def __init__(self, file_handle, color_compression_type, depth_compression_type, depth_shape):
        self.camera_to_world = np.asarray(struct.unpack('f' * 16, file_handle.read(16 * 4)), dtype=np.float32).reshape(
            4, 4)
        self.timestamp_color = struct.unpack('Q', file_handle.read(8))[0]
        self.timestamp_depth = struct.unpack('Q', file_handle.read(8))[0]
        self.color_size_bytes = struct.unpack('Q', file_handle.read(8))[0]
        self.depth_size_bytes = struct.unpack('Q', file_handle.read(8))[0]
        self.color_data = file_handle.read(self.color_size_bytes)
        self.depth_data = file_handle.read(self.depth_size_bytes)

        self.get_color_image = lambda: self.decompress_color(color_compression_type)
        self.get_depth_image = lambda: np.frombuffer(self.decompress_depth(depth_compression_type), dtype=np.uint16)\
            .reshape(depth_shape)

    def decompress_depth(self, compression_type):
        if compression_type == 'zlib_ushort':
            return self.decompress_depth_zlib()
        else:
            raise

    def decompress_depth_zlib(self):
        return zlib.decompress(self.depth_data)

    def decompress_color(self, compression_type):
        if compression_type == 'jpeg':
            return self.decompress_color_jpeg()
        else:
            raise

    def decompress_color_jpeg(self):
        return imageio.imread(self.color_data)

    def get_camera_to_world(self):
        return self.camera_to_world

    def get_timestamp(self):
        raise NotImplementedError


class SensFileHandler:
    def __init__(self, file_loc):
        self.file_loc = file_loc
        self.version = 4
        self.fp = None
        self.fp_use_count = 0

        # Header attributes
        self.sensor_name = None
        self.intrinsic_color = None
        self.extrinsic_color = None
        self.intrinsic_depth = None
        self.extrinsic_depth = None
        self.color_compression_type = None
        self.depth_compression_type = None
        self.color_width = None
        self.color_height = None
        self.depth_width = None
        self.depth_height = None
        self.depth_shift = None  # conversion from float[m] to ushort (typically 1000f)
        self.num_frames = None
        self._offset_per_frame = None  # OFFSET IN FILE TO START OF FRAME DATA

    def read_header(self):
        assert self.fp is not None, "File needs to be opened before it can be read"
        version = struct.unpack('I', self.fp.read(4))[0]
        assert self.version == version
        strlen = struct.unpack('Q', self.fp.read(8))[0]
        self.sensor_name = self.fp.read(strlen).decode('utf-8')
        self.intrinsic_color = np.array(struct.unpack('f' * 16, self.fp.read(16 * 4))).reshape(4, 4)
        self.extrinsic_color = np.array(struct.unpack('f' * 16, self.fp.read(16 * 4))).reshape(4, 4)
        self.intrinsic_depth = np.array(struct.unpack('f' * 16, self.fp.read(16 * 4))).reshape(4, 4)
        self.extrinsic_depth = np.array(struct.unpack('f' * 16, self.fp.read(16 * 4))).reshape(4, 4)
        self.color_compression_type = COMPRESSION_TYPE_COLOR[struct.unpack('i', self.fp.read(4))[0]]
        self.depth_compression_type = COMPRESSION_TYPE_DEPTH[struct.unpack('i', self.fp.read(4))[0]]
        self.color_width = struct.unpack('I', self.fp.read(4))[0]
        self.color_height = struct.unpack('I', self.fp.read(4))[0]
        self.depth_width = struct.unpack('I', self.fp.read(4))[0]
        self.depth_height = struct.unpack('I', self.fp.read(4))[0]
        self.depth_shift = struct.unpack('f', self.fp.read(4))[0]# conversion from float[m] to ushort (typically 1000f)
        self.num_frames = struct.unpack('Q', self.fp.read(8))[0]
        self._offset_per_frame = [self.fp.tell()]

    def __enter__(self):
        return self

    def __getitem__(self, index):
        assert self.fp is not None, "File needs to be opened before it can be read"
        if index < 0 or index >= self.num_frames:
            raise IndexError

        if self._offset_per_frame is None:
            self.read_header()

        init_index = min(index, len(self._offset_per_frame) - 1)
        self.fp.seek(self._offset_per_frame[init_index])
        ret = None
        for i in range(init_index, index):
            if len(self._offset_per_frame) == i:
                self._offset_per_frame.append(self.fp.tell())
            ret = RGBDFrame(self.fp, self.color_compression_type, self.depth_compression_type,
                            (self.depth_height, self.depth_width))
        return ret

    def __len__(self):
        if self.num_frames is NotImplementedError:
            self.read_header()
        return self.num_frames

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def open(self):
        self.fp = open(self.file_loc, 'rb')
        self.fp_use_count += 1
        return self

    def close(self, force=False):
        self.fp_use_count -= 1
        if self.fp_use_count <= 0 or force:
            self.fp.close()
            self.fp = None
