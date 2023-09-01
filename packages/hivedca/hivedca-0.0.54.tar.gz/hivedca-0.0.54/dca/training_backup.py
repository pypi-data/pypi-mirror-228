import torch
import numpy as np
import os

import metrics
from dataloader import get_dataloaders
from utils import fix_seeds, plot_segmentation_images
from sampler import get_sampler
from patch_core import get_patchcore

def fit_training(data_path,
             batch_size,
             resize,
             sampler_percentage,
             num_workers,
             augment,
             seed,
             backbone_name,
             run_backbone_cpu,
             sampler_name,
             Save_heatmap,
             save_patchcore_model,
             save_path):
    fix_seeds(seed)
    run_save_path = save_path
    try:
        os.makedirs(save_path, exist_ok=True)
    except:
        print("save path error")

    dataloaders = get_dataloaders(
        data_path=data_path,
        batch_size=batch_size,
        resize = resize,
        num_workers=num_workers,
        augment=augment)

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
        imagesize = dataloaders["training"].dataset.imagesize
        sampler = get_sampler(device,percentage=sampler_percentage,name =sampler_name)
        PatchCore = get_patchcore(imagesize,sampler,backbone_name,device)
        print("Training Start ========================================================================================")

        torch.cuda.empty_cache()
        PatchCore.fit(dataloaders["training"])


        aggregator = {"scores": [], "segmentations": []}

        torch.cuda.empty_cache()
        scores, segmentations, labels_gt, masks_gt = PatchCore.predict(
            dataloaders["testing"]
        )
        aggregator["scores"].append(scores)
        aggregator["segmentations"].append(segmentations)


        scores = np.array(aggregator["scores"])
        min_scores = scores.min(axis=-1).reshape(-1, 1)
        max_scores = scores.max(axis=-1).reshape(-1, 1)
        scores = (scores - min_scores) / (max_scores - min_scores)

        scores = np.mean(scores, axis=0)
        print(scores)
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

        anomaly_labels = [
            x[1] != "good" for x in dataloaders["testing"].dataset.data_to_iterate
        ]

        # (Optional) Plot example images.
        if Save_heatmap:
            image_paths = [
                x[2] for x in dataloaders["testing"].dataset.data_to_iterate
            ]
            mask_paths = [
                x[3] for x in dataloaders["testing"].dataset.data_to_iterate
            ]

            def image_transform(image):
                in_std = np.array([0.229, 0.224, 0.225]).reshape(-1, 1, 1)
                in_mean = np.array([0.485, 0.456, 0.406]).reshape(-1, 1, 1)
                image = dataloaders["testing"].dataset.transform_img(image)
                return np.clip(
                    (image.numpy() * in_std + in_mean) * 255, 0, 255
                ).astype(np.uint8)
            def mask_transform(mask):
                return dataloaders["testing"].dataset.transform_mask(mask).numpy()

            image_save_path = os.path.join(
                run_save_path, "segmentation_images")
            os.makedirs(image_save_path, exist_ok=True)
            plot_segmentation_images(
                image_save_path,
                image_paths,
                segmentations,
                scores,
                mask_paths,
                image_transform=image_transform,
                mask_transform=mask_transform,
            )

        print("Computing evaluation metrics.")
        auroc = metrics.compute_imagewise_retrieval_metrics(
            scores, anomaly_labels
        )["auroc"]

        # Compute PRO score & PW Auroc for all images
        pixel_scores = metrics.compute_pixelwise_retrieval_metrics(
            segmentations, masks_gt
        )
        full_pixel_auroc = pixel_scores["auroc"]

        # Compute PRO score & PW Auroc only images with anomalies
        sel_idxs = []
        for i in range(len(masks_gt)):
            if np.sum(masks_gt[i]) > 0:
                sel_idxs.append(i)
        pixel_scores = metrics.compute_pixelwise_retrieval_metrics(
            [segmentations[i] for i in sel_idxs],
            [masks_gt[i] for i in sel_idxs],
        )
        anomaly_pixel_auroc = pixel_scores["auroc"]
        print(auroc,full_pixel_auroc,anomaly_pixel_auroc)

        # (Optional) Store PatchCore model for later re-use.
        # SAVE all patchcores only if mean_threshold is passed?
        if save_patchcore_model:
            patchcore_save_path = os.path.join(
                run_save_path, "models" )
            os.makedirs(patchcore_save_path, exist_ok=True)
            prepend = ""
            PatchCore.save_to_path(patchcore_save_path, prepend)
