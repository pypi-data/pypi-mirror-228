import os
from enum import Enum

import PIL
import torch
from torchvision import transforms

IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]

class DatasetSplit(Enum):
    TRAIN = "train"
    VAL = "val"
    TEST = "test"


def get_test_dataloaders_list(data_list,batch_size,resize,num_workers):
    test_dataset = CustomDataset_list(data_list,resize=resize,
                                 split=DatasetSplit.TEST,
                                 seed=0,augment=False)
    test_dataloader = torch.utils.data.DataLoader(
        test_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=True,
    )

    dataloader_dict = {
        "testing": test_dataloader,
    }

    return dataloader_dict

def get_train_dataloaders_list(data_list, batch_size, resize, num_workers, augment=True):
    train_dataset = CustomDataset_list(source=data_list, resize=resize,
                                  split=DatasetSplit.TRAIN,
                                  seed=0, augment=augment)

    train_dataloader = torch.utils.data.DataLoader(train_dataset,
                                                   batch_size=batch_size,
                                                   shuffle=False,
                                                   num_workers=num_workers,
                                                   pin_memory=True,
                                                   )

    dataloader_dict = {
        "training": train_dataloader,
    }

    return dataloader_dict

class CustomDataset_list(torch.utils.data.Dataset):
    def __init__(
        self,
        source,
        resize=(256,256),
        split=DatasetSplit.TRAIN,
        train_val_split=1.0,
        **kwargs,
    ):
        """
        Args:
            source: [str]. Path to the MVTec data folder.
            classname: [str or None]. Name of MVTec class that should be
                       provided in this dataset. If None, the datasets
                       iterates over all available images.
            resize: [int]. (Square) Size the loaded image initially gets
                    resized to.
            imagesize: [int]. (Square) Size the resized loaded image gets
                       (center-)cropped to.
            split: [enum-option]. Indicates if training or test split of the
                   data should be used. Has to be an option taken from
                   DatasetSplit, e.g. mvtec.DatasetSplit.TRAIN. Note that
                   mvtec.DatasetSplit.TEST will also load mask data.
        """
        super().__init__()
        self.source = source
        self.split = split
        self.train_val_split = train_val_split

        self.data_to_iterate = self.get_image_data()
        print(self.data_to_iterate)
        self.transform_img = [
            transforms.Resize(resize),
            transforms.ToTensor(),
            transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
        ]
        self.transform_img = transforms.Compose(self.transform_img)

        self.transform_mask = [
            transforms.Resize(resize),
            transforms.ToTensor(),
        ]
        self.transform_mask = transforms.Compose(self.transform_mask)

        self.imagesize = (3, resize[0], resize[1])

    def __getitem__(self, idx):
        classname, anomaly, image_path, mask_path = self.data_to_iterate[idx]
        image = PIL.Image.open(image_path).convert("RGB")
        image = self.transform_img(image)

        if self.split == DatasetSplit.TEST and mask_path is not None:
            mask = PIL.Image.open(mask_path)
            mask = self.transform_mask(mask)
        else:
            mask = torch.zeros([1, *image.size()[1:]])

        return {
            "image": image,
            "mask": mask,
            "classname": classname,
            "anomaly": anomaly,
            "is_anomaly": int(anomaly != "good"),
            "image_name": "/".join(image_path.split("/")[-4:]),
            "image_path": image_path,
        }

    def __len__(self):
        return len(self.data_to_iterate)

    def get_image_data(self):
        data_to_iterate = []
        for s in self.source:
            if s[2] == "":
                data_to_iterate.append([".","good",s[1],None])
            elif s[2] != "":
                data_to_iterate.append([".","NG",s[1],s[2]])
        return data_to_iterate

def main():

    test_data_list = [ [0,"C:/Users/jjkjy/Desktop/anomaly_sample/Data_toptec_center/test/NG/AL_CROP_VIDI_0-000019.jpg","C:/Users/jjkjy/Desktop/anomaly_sample/Data_toptec_center/ground_truth/NG/AL_CROP_VIDI_0-000019.jpg"],
                       [1,"C:/Users/jjkjy/Desktop/anomaly_sample/Data_toptec_center/test/good/AL_CROP_VIDI_0-092144.jpg",""],
                       [2,"C:/Users/jjkjy/Desktop/anomaly_sample/Data_toptec_center/test/NG/AL_CROP_VIDI_0-000724.jpg","C:/Users/jjkjy/Desktop/anomaly_sample/Data_toptec_center/ground_truth/NG/AL_CROP_VIDI_0-000724.jpg"],
                       [3,"C:/Users/jjkjy/Desktop/anomaly_sample/Data_toptec_center/test/NG/AL_CROP_VIDI_0-000749.jpg","C:/Users/jjkjy/Desktop/anomaly_sample/Data_toptec_center/ground_truth/NG/AL_CROP_VIDI_0-000749.jpg"],
                       [4,"C:/Users/jjkjy/Desktop/anomaly_sample/Data_toptec_center/test/NG/AL_CROP_VIDI_0-001304.jpg","C:/Users/jjkjy/Desktop/anomaly_sample/Data_toptec_center/ground_truth/NG/AL_CROP_VIDI_0-001304.jpg"]]
    b = get_test_dataloaders_list(data_list=test_data_list,batch_size=2,resize=(256,256),num_workers=8)
    print(b)
    train_data_list = [[0,"C:/Users/jjkjy/Desktop/anomaly_sample/Data_toptec_center/train/good/AL_CROP_VIDI_0-000003.jpg",""],
                       [1,"C:/Users/jjkjy/Desktop/anomaly_sample/Data_toptec_center/train/good/AL_CROP_VIDI_0-000011.jpg",""],
                       [2,"C:/Users/jjkjy/Desktop/anomaly_sample/Data_toptec_center/train/good/AL_CROP_VIDI_0-000521.jpg",""],
                       [3,"C:/Users/jjkjy/Desktop/anomaly_sample/Data_toptec_center/train/good/AL_CROP_VIDI_0-000529.jpg",""]]
    #
    a = get_train_dataloaders_list(data_list=train_data_list,batch_size=2,resize=(256,256),num_workers=0,augment=True)
    print(a)
if __name__ == "__main__":
    main()