import torch
import os
import sys

from dataloader_list import get_train_dataloaders_list
from utils import fix_seeds
from sampler import get_sampler
from patch_core import get_patchcore
import contextlib

def fit_training(data_list,
             batch_size,
             resize,
             sampler_percentage,
             num_workers,
             seed,
             backbone_name,
             run_backbone_cpu,
             sampler_name,
             save_patchcore_model,
             save_path):
    fix_seeds(seed)


    dataloaders = get_train_dataloaders_list(
        data_list=data_list,
        batch_size=batch_size,
        resize = resize,
        num_workers=num_workers,
        augment=True)

    if run_backbone_cpu == False:
        device = torch.device("cuda:{}".format(0))
    elif run_backbone_cpu == True:
        device = torch.device("cpu")
    device_context = (
        torch.cuda.device("cuda:{}".format(device.index))
        if "cuda" in device.type.lower()
        else contextlib.suppress()
    )

    with device_context:
        torch.cuda.empty_cache()
        imagesize = dataloaders["training"].dataset.imagesize
        sampler = get_sampler(device,percentage=sampler_percentage,name =sampler_name)
        PatchCore = get_patchcore(imagesize,sampler,backbone_name,device)
        # print("Training Start ========================================================================================")
        torch.cuda.empty_cache()
        PatchCore.fit(dataloaders["training"])
        # print("Training End ==========================================================================================")
        torch.cuda.empty_cache()
        # (Optional) Store PatchCore model for later re-use.
        # SAVE all patchcores only if mean_threshold is passed?
        if save_patchcore_model:
            prepend = ""
            PatchCore.save_to_path(save_path, prepend)
