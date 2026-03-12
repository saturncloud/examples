import os
import time
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader

import mlflow
import mlflow.pytorch
import numpy as np

# --- Configuration ---
# 1. MLflow Tracking URI (MLflow server or local './mlruns')
MLFLOW_TRACKING_URI = os.environ.get("MLFLOW_TRACKING_URI", "file:./mlruns")
MLFLOW_EXPERIMENT_NAME = "GPU_DeepLearning_RunPod"

# 2. Hyperparameters (These will be automatically logged by mlflow.pytorch.autolog())
# Note: Autologging handles logging the optimizer details and LR automatically.
PARAMS = {
    "learning_rate": 0.001,
    "epochs": 5,
    "batch_size": 32,
    "model_type": "SimpleConvNet",
    "optimizer": "Adam"
}

# --- PyTorch Model Definition ---
class SimpleConvNet(nn.Module):
    def __init__(self):
        super(SimpleConvNet, self).__init__()
        self.conv1 = nn.Conv2d(1, 10, kernel_size=5)
        self.relu = nn.ReLU()
        self.fc = nn.Linear(10 * 24 * 24, 1)

    def forward(self, x):
        x = self.relu(self.conv1(x))
        x = x.view(-1, 10 * 24 * 24)
        x = self.fc(x)
        return x

def train_and_log(device):
    
    # --- 1. MLflow Setup ---
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment(MLFLOW_EXPERIMENT_NAME)
    
    # 2. ENABLE AUTOLOGGING: Automatically logs model, params, and metrics (except custom loops)
    mlflow.pytorch.autolog(log_models=True, log_datasets=False) #

    # 3. START RUN: Enable system metrics logging inside the run context
    with mlflow.start_run(run_name="GPU_Train_Run", log_system_metrics=True) as run:
        
        # Log system information manually (GPU type and custom params not auto-logged)
        if device.type == 'cuda':
            mlflow.log_param("gpu_device", torch.cuda.get_device_name(0))
        mlflow.log_params(PARAMS)

        # --- Training Execution ---
        print(f"Starting training on device: {device} with LR={PARAMS['learning_rate']}")

        # Simulate Data Setup
        data = torch.randn(100, 1, 28, 28, device=device)
        labels = torch.randint(0, 2, (100, 1), dtype=torch.float32, device=device)
        dataloader = DataLoader(TensorDataset(data, labels), batch_size=PARAMS['batch_size'])

        model = SimpleConvNet().to(device)
        optimizer = optim.Adam(model.parameters(), lr=PARAMS['learning_rate'])
        criterion = nn.BCEWithLogitsLoss()

        # Training Loop
        for epoch in range(PARAMS['epochs']):
            total_loss = 0.0
            
            for inputs, targets in dataloader:
                optimizer.zero_grad()
                outputs = model(inputs)
                loss = criterion(outputs, targets)
                loss.backward()
                optimizer.step()
                total_loss += loss.item()

            avg_loss = total_loss / len(dataloader)
            
            # Manually log the primary metric (optional, as autolog might cover this in integrated loops)
            mlflow.log_metric("avg_loss_manual", avg_loss, step=epoch)
            
            print(f"Epoch {epoch+1} - Loss: {avg_loss:.4f}")

        # 4. Final Logging
        mlflow.log_metric("final_loss", avg_loss)
        
        # Note: Model and optimizer params are logged automatically by mlflow.pytorch.autolog()
        
        print("\n✅ Training complete.")
        print(f"MLflow Run ID: {run.info.run_id}")


def main():
    if torch.cuda.is_available():
        device = torch.device("cuda")
        print("💡 GPU detected and available.")
    else:
        device = torch.device("cpu")
        print("⚠️ GPU not detected. Running on CPU.")

    train_and_log(device)

if __name__ == "__main__":
    main()