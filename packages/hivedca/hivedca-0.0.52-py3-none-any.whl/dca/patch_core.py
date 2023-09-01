import backbones
import common
import patchcore


def get_patchcore(input_shape, sampler, backbone_name, device):
    faiss_on_gpu = False
    faiss_num_workers = 8
    backbone_names = [backbone_name]
    layers_to_extract_from = ["layer2","layer3"]
    pretrain_embed_dimension = 1024
    target_embed_dimension = 1024
    preprocessing = "mean" # or "conv"
    aggregation = "mean" # or "mlp"
    patchsize = 3
    patchscore = "max"
    patchoverlap = "0.0"
    anomaly_scorer_num_nn = 5
    patchsize_aggregate = None
    backbone_names = list(backbone_names)
    
    if len(backbone_names) > 1:
        layers_to_extract_from_coll = [[] for _ in range(len(backbone_names))]
        for layer in layers_to_extract_from:
            idx = int(layer.split(".")[0])
            layer = ".".join(layer.split(".")[1:])
            layers_to_extract_from_coll[idx].append(layer)
    else:
        layers_to_extract_from_coll = [layers_to_extract_from]

    for backbone_name, layers_to_extract_from in zip(
        backbone_names, layers_to_extract_from_coll
    ):
        backbone_seed = None
        if ".seed-" in backbone_name:
            backbone_name, backbone_seed = backbone_name.split(".seed-")[0], int(
                backbone_name.split("-")[-1]
            )
        backbone = backbones.load(backbone_name)
        backbone.name, backbone.seed = backbone_name, backbone_seed

        nn_method = common.FaissNN(faiss_on_gpu, faiss_num_workers)

        patchcore_instance = patchcore.PatchCore(device)
        patchcore_instance.load(
            backbone=backbone,
            layers_to_extract_from=layers_to_extract_from,
            device=device,
            input_shape=input_shape,
            pretrain_embed_dimension=pretrain_embed_dimension,
            target_embed_dimension=target_embed_dimension,
            patchsize=patchsize,
            featuresampler=sampler,
            anomaly_scorer_num_nn=anomaly_scorer_num_nn,
            nn_method=nn_method,
        )
    
    return patchcore_instance

