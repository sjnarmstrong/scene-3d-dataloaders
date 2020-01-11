class ScannetScene:
    def __init__(self, scene_id, info_path, sens_path, mesh_path, segmentation_map, aggregation_map,
                 projected_instance_archive, projected_label_file, labelled_pcd_file):
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

    # 2D information
    ## depth_images
    ## colour_images
    ## camera_to_worlds
    ## timestamps
    ## frame_numbers
    ## 2D Segmentation
    ## 3D Reprojection


    # camera_params
    ## intrinsic RGB
    ## extrinsic RGB
    ## intrinsic Depth
    ## extrinsic depth
    ## Depth multiplier (val to meters)




