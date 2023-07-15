from typing import List, Dict
import os
from grapemask.utils.json import load_file_json
from detectron2.structures import BoxMode


class Detectron2Data:
    def __init__(
        self,
        base_pth: str,
        anno_rel_path: str,
        bbox_mode: BoxMode = BoxMode.XYWH_ABS,
        filter_empty: bool = True,
    ):
        super().__init__()
        self.base_pth = base_pth
        self.anno_rel_path = anno_rel_path
        self.bbox_mode = bbox_mode
        self.filter_empty = filter_empty

        annotation_pth = os.path.join(base_pth, "annotations", anno_rel_path)
        anno_json = load_file_json(annotation_pth)

        self.dataset_dicts = self.cocoformat_to_detectron2(anno_json)

    def cocoformat_to_detectron2(self, anno_json: Dict) -> List[Dict]:
        images = anno_json["images"]
        all_annotations = anno_json["annotations"]
        detectron2_annos = []
        for image in images:
            file_name = image["file_name"]
            file_name = os.path.join(self.base_pth, file_name)
            height = image["height"]
            width = image["width"]
            image_id = image["id"]
            image_annotations = [
                annotation
                for annotation in all_annotations
                if annotation["image_id"] == image_id
            ]
            annotations = []
            for anno in image_annotations:
                bbox = anno["bbox"]
                bbox_mode = self.bbox_mode

                # Coco categories start at 1 while Detectron2 categories start at 0
                category_id = int(anno["category_id"]) - 1
                segmentation = anno["segmentation"]
                annotations.append(
                    {
                        "bbox": bbox,
                        "bbox_mode": bbox_mode,
                        "category_id": category_id,
                        "segmentation": segmentation,
                        "iscrowd": 0,
                    }
                )
            if not self.filter_empty or len(annotations) > 0:
                detectron2_annos.append(
                    {
                        "file_name": file_name,
                        "height": height,
                        "width": width,
                        "image_id": image_id,
                        "annotations": annotations,
                    }
                )
        return detectron2_annos

    def dataset_function(self) -> List[Dict]:
        return self.dataset_dicts
