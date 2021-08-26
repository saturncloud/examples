# pylint: disable=unused-import, trailing-whitespace, multiple-imports, F841
# # Train Model with Snowflake unstructured files

# This script trains an image classification model based on ResNet50, using source image files from a Snowflake unstructured table. Learn more at https://quickstarts.snowflake.com/.


import numpy as np, pandas as pd
import requests, io, os, datetime, re, math
import torch
from torch import nn, optim
from torchvision import datasets, transforms, models
from torch.utils.data.sampler import (
    RandomSampler,
)
from pytorchsnowflake import SnowflakeImageFolder
import snowflake.connector
from fastprogress.fastprogress import master_bar, progress_bar
import multiprocessing as mp


def simple_train_single(batch_size, downsample_to, n_epochs, base_lr, conn_kwargs):

    # --------- Format params --------- #
    device = torch.device("cuda")
    net = models.resnet50(pretrained=False)  # True means we start with the imagenet version
    # net.load_state_dict(
    #     torch.load("model/modeltrained.pt")
    # )  # Start from the existing model state if desired
    model = net.to(device)

    # --------- Set up eval --------- #
    criterion = nn.CrossEntropyLoss().cuda()
    optimizer = optim.AdamW(model.parameters(), lr=base_lr, eps=1e-06)

    # --------- Retrieve data for training --------- #
    transform = transforms.Compose(
        [transforms.Resize(256), transforms.CenterCrop(250), transforms.ToTensor()]
    )

    with snowflake.connector.connect(**conn_kwargs) as conn:
        whole_dataset = SnowflakeImageFolder(
            table_name="clothing_train",
            relative_path_col="RELATIVE_PATH",
            stage="clothing_dataset_train",
            connection=conn,
            transform=transform,
        )

    # ------ Create dataloader ------- #
    train_loader = torch.utils.data.DataLoader(
        whole_dataset,
        sampler=RandomSampler(
            whole_dataset,
            replacement=True,
            num_samples=math.floor(len(whole_dataset) * downsample_to),
        ),
        batch_size=batch_size,
        num_workers=4,
        multiprocessing_context=mp.get_context("fork"),
    )

    # Using the OneCycleLR learning rate schedule
    scheduler = optim.lr_scheduler.OneCycleLR(
        optimizer, max_lr=base_lr, steps_per_epoch=len(train_loader), epochs=n_epochs
    )

    # --------- Start Training ------- #
    mb = master_bar(range(n_epochs))
    for epoch in mb:
        count = 0
        model.train()

        for inputs, labels in progress_bar(train_loader, parent=mb):
            # zero the parameter gradients
            optimizer.zero_grad()

            dt = datetime.datetime.now().isoformat()
            inputs, labels = inputs.to(device), labels.to(device)

            # Run model iteration
            outputs = model(inputs)

            # Format results
            pred_idx, preds = torch.max(outputs, 1)
            perct = [
                torch.nn.functional.softmax(el, dim=0)[i].item() for i, el in zip(preds, outputs)
            ]

            loss = criterion(outputs, labels)
            correct = (preds == labels).sum().item()

            loss.backward()
            optimizer.step()
            scheduler.step()

            # Log your metrics
            logs = {
                "train_loss": loss.item(),
                "learning_rate": scheduler.get_last_lr()[0],
                "correct": correct,
                "epoch": epoch + count / len(train_loader),
                "count": count,
            }

            #  Print logs every so often
            if count % 10 == 0:
                print(logs)
                torch.save(model.state_dict(), "model/modeltrained.pt")
            count += 1
    torch.save(model.state_dict(), "model/modeltrained.pt")


if __name__ == "__main__":

    conn_kwargs = dict(
        user=os.environ["SNOWFLAKE_USER"],
        password=os.environ["SNOWFLAKE_PASSWORD"],
        account="mf80263.us-east-2.aws",
        warehouse="COMPUTE_WH",
        database="clothing_dataset",
        schema="PUBLIC",
        role="datascience_examples_writer",
    )

    model_params = {
        "n_epochs": 25,
        "batch_size": 64,
        "base_lr": 0.003,
        "downsample_to": 1,  # Value represents percent of training data you want to use
        "conn_kwargs": conn_kwargs,
    }

    simple_train_single(**model_params)
