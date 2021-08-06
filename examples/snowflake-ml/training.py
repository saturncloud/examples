# Train Model with Snowflake unstructured files

import numpy as np, pandas as pd
import requests, io, os, datetime, re, math
import torch
from torch import nn, optim
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader
from torch.utils.data.sampler import SubsetRandomSampler, RandomSampler
from pytorch_snowflake_class import SnowflakeImageFolder
import snowflake.connector
from fastprogress.fastprogress import master_bar, progress_bar


def simple_train_single(batch_size, downsample_to, n_epochs, base_lr, conn_kwargs):

    # --------- Format params --------- #
    device = torch.device("cuda")
    net = models.resnet50(pretrained=False)  # True means we start with the imagenet version

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
            table_name="clothing_data",
            relative_path_col="RELATIVE_PATH",
            url_col="URL",
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
                torch.save(model.state_dict(), "model/model_trained.pt")
            count += 1
    torch.save(model.state_dict(), "model/model_trained.pt")


if __name__ == "__main__":

    conn_kwargs = dict(
        user=os.environ["SNOWFLAKE_USER"],  # This will draw from your Saturn Cloud credentials
        password=os.environ[
            "SNOWFLAKE_PASSWORD"
        ],  # This will draw from your Saturn Cloud credentials
        account="mf80263.us-east-2.aws",  # Fill in your own account here!
        warehouse="COMPUTE_WH",  # Fill in your own warehouse here!
        database="clothing",  # You created this earlier!
        schema="PUBLIC",
        role="datascience",  # Fill in your own role here!
    )

    model_params = {
        "n_epochs": 20,
        "batch_size": 32,
        "base_lr": 0.003,
        "downsample_to": 1,  # Value represents percent of training data you want to use
        "conn_kwargs": conn_kwargs,
    }

    simple_train_single(**model_params)
