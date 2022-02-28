import os
import torch
import torch.nn as nn

from torchvision import datasets, models, transforms

############################################################
# Loads the data into DataLoaders

# Input: the data directory and the batch size
# Output: dataloaders for train, validation, and test; dataset sizes; and the number of classes

# This code is identical to what you would expect in a PyTorch workflow
############################################################


def load_data(data_dir, batch_size):
    data_transforms = {
        "train": transforms.Compose(
            [
                transforms.RandomResizedCrop(224),
                transforms.RandomHorizontalFlip(),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
            ]
        ),
        "valid": transforms.Compose(
            [
                transforms.Resize(256),
                transforms.CenterCrop(224),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
            ]
        ),
        "test": transforms.Compose(
            [
                transforms.Resize(256),
                transforms.CenterCrop(224),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
            ]
        ),
    }

    image_datasets = {
        x: datasets.ImageFolder(os.path.join(data_dir, x), data_transforms[x])
        for x in ["train", "valid", "test"]
    }

    dataloaders = {
        x: torch.utils.data.DataLoader(
            image_datasets[x], batch_size=batch_size, shuffle=True, num_workers=4
        )
        for x in ["train", "valid", "test"]
    }

    dataset_sizes = {x: len(image_datasets[x]) for x in ["train", "valid", "test"]}

    classes = image_datasets["train"].classes

    return dataloaders, dataset_sizes, classes


############################################################
# Defines the PyTorch model

# Input: number of output classes
# Output: a resnet50 pretrained pytorch model
############################################################
def define_model(num_classes, pretrained=True):
    model = models.resnet50(pretrained=pretrained)
    num_ftrs = model.fc.in_features
    model.fc = nn.Linear(num_ftrs, num_classes)
    return model
