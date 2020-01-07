from .dataset import BaseDataset, Literal, Iterable
import lazy_import
import os
h5py = lazy_import.lazy_module("h5py")
groupby = lazy_import.lazy_callable("itertools.groupby")
ZipFile = lazy_import.lazy_callable("zipfile.ZipFile")
re = lazy_import.lazy_module("re")


class NYUDataset(BaseDataset):
    ID: Literal['NYU']
    zip_file_loc: str
    gt_file_loc: str

    @property
    def scenes(self) -> Iterable:
        """
        Loads the various scenes in the NYU dataset
        :return: None
        """
        zip_f = ZipFile(self.zip_file_loc)
        scene_frames = {k: self.synchronise_frames(frames) for k, frames in
                        self.split_namelist_into_scenes(zip_f.namelist()).items()}

        with h5py.File(self.gt_file_loc, 'r') as f:
            depth_frame_names = [f[frame][()].tobytes().decode('utf16') for frame in f.get('rawDepthFilenames')[0]]
            color_frame_names = [f[frame][()].tobytes().decode('utf16') for frame in f.get('rawRgbFilenames')[0]]
            scene_names = [f[frame][()].tobytes().decode('utf16') for frame in f.get('scenes')[0]]
            unique_scenes = sorted(set(scene_names))
            gt_scene_name_mapping = {k: [] for k in unique_scenes}
            for scene_name, depth_frame_name, color_frame_name in \
                    zip(scene_names, depth_frame_names, color_frame_names):
                gt_scene_name_mapping[scene_name].append((depth_frame_name, color_frame_name))

        # Note some scenes do not seem to have raw datasets. Todo check in parts
        scenes = []
        for k in unique_scenes:
            if k in scene_frames:
                scene = [k, zip_f, scene_frames[k], gt_scene_name_mapping[k], self.gt_file_loc]
                scenes.append(scene)

        return scenes

    @staticmethod
    def synchronise_frames(frame_names):
        """Constructs a list of synchronised depth and RGB frames.

        Returns a list of pairs, where the first is the path of a depth image,
        and the second is the path of a color image.
        """

        # Regular expressions for matching depth and color images
        depth_img_prog = re.compile(r'.+/d-.+\.pgm')
        color_img_prog = re.compile(r'.+/r-.+\.ppm')

        # Applies a regex program to the list of names
        def match_names(prog):
            return map(prog.match, frame_names)

        # Filters out Nones from an iterator
        def filter_none(iter):
            return filter(None.__ne__, iter)

        # Converts regex matches to strings
        def match_to_str(matches):
            return map(lambda match: match.group(0), matches)

        # Retrieves the list of image names matching a certain regex program
        def image_names(prog):
            return list(match_to_str(filter_none(match_names(prog))))

        depth_img_names = image_names(depth_img_prog)
        color_img_names = image_names(color_img_prog)

        # By sorting the image names we ensure images come in chronological order
        depth_img_names.sort()
        color_img_names.sort()

        def name_to_timestamp(name):
            """Extracts the timestamp of a RGB / depth image from its name."""
            _, time, _ = name.split('-')
            return float(time)

        frames = []
        color_count = len(color_img_names)
        color_idx = 0

        for depth_img_name in depth_img_names:
            depth_time = name_to_timestamp(depth_img_name)
            color_time = name_to_timestamp(color_img_names[color_idx])

            diff = abs(depth_time - color_time)

            # Keep going through the color images until we find
            # the one with the closest timestamp
            while color_idx + 1 < color_count:
                color_time = name_to_timestamp(color_img_names[color_idx + 1])

                new_diff = abs(depth_time - color_time)

                # Moving forward would only result in worse timestamps
                if new_diff > diff:
                    break

                color_idx = color_idx + 1

            frames.append((depth_img_name, color_img_names[color_idx], depth_time))

        return frames

    @staticmethod
    def split_namelist_into_scenes(name_list):
        # assert all(fr_n[0] >= fr[0] for fr_n, fr in zip(name_list[1:], name_list))  # TODO remove later
        grouped_vals = [(k, list(g)) for k, g in groupby(name_list, key=lambda x: os.path.split(x)[0])]
        out_dict = {}
        for k, g in grouped_vals:
            if k in out_dict:
                out_dict[k].extend(g)
            else:
                out_dict[k] = g
        return out_dict
