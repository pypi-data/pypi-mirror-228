import torch
import numpy as np
import os

from utils import fix_seeds, set_torch_device
import PIL

import common
import patchcore
from torchvision import transforms
import contextlib

def load_patchcore(patch_core_path):
    device = set_torch_device([0])
    n_patchcores = len(
        [x for x in os.listdir(patch_core_path) if ".faiss" in x]
    )
    if n_patchcores == 1:
        nn_method = common.FaissNN(False, 8)
        patchcore_instance = patchcore.PatchCore(device)
        patchcore_instance.load_from_path(
            load_path=patch_core_path, device=device, nn_method=nn_method
        )
        return patchcore_instance
    else:
        for i in range(n_patchcores):
            nn_method = common.FaissNN(
                False, 8
            )
            patchcore_instance = patchcore.PatchCore(device)
            patchcore_instance.load_from_path(
                load_path=patch_core_path,
                device=device,
                nn_method=nn_method,
                prepend="Ensemble-{}-{}_".format(i + 1, n_patchcores),
            )
            return patchcore_instance


def fit_inference(data_path,
             resize,
             seed,
             run_backbone_cpu,
             save_path,
                 patchcore,
                  min_score,
                  max_score):
    fix_seeds(seed)
    run_save_path = save_path
    try:
        os.makedirs(save_path, exist_ok=True)
    except:
        print("save path error")

    if run_backbone_cpu == False:
        device = torch.device("cuda:{}".format(0))
    elif run_backbone_cpu == True:
        device = torch.device("cpu")
    device_context = (
        torch.cuda.device("cuda:{}".format(device.index))
        if "cuda" in device.type.lower()
        else contextlib.suppress()
    )

    result_collect = []
    with device_context:
        torch.cuda.empty_cache()
        PatchCore = patchcore


        aggregator = {"scores": [], "segmentations": []}

        torch.cuda.empty_cache()
        IMAGENET_MEAN = [0.485, 0.456, 0.406]
        IMAGENET_STD = [0.229, 0.224, 0.225]
        image = PIL.Image.open(data_path).convert("RGB")
        transform_img = [
            transforms.Resize(resize),
            transforms.ToTensor(),
            transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
        ]
        transform_img = transforms.Compose(transform_img)
        image = transform_img(image)
        image = image.unsqueeze(0)

        scores, segmentations = PatchCore.predict(image)
        aggregator["scores"].append(scores)
        aggregator["segmentations"].append(segmentations)

        scores = np.array(aggregator["scores"])
        # min_scores = scores.min(axis=-1).reshape(-1, 1)
        # max_scores = scores.max(axis=-1).reshape(-1, 1)
        scores = (scores - min_score) / (max_score - min_score)
        scores = np.mean(scores, axis=0)
        segmentations = np.array(aggregator["segmentations"])
        min_scores = (
            segmentations.reshape(len(segmentations), -1)
            .min(axis=-1)
            .reshape(-1, 1, 1, 1)
        )
        max_scores = (
            segmentations.reshape(len(segmentations), -1)
            .max(axis=-1)
            .reshape(-1, 1, 1, 1)
        )
        segmentations = (segmentations - min_scores) / (max_scores - min_scores)
        segmentations = np.mean(segmentations, axis=0)

        return scores, segmentations