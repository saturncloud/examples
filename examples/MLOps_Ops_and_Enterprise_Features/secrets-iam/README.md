# 🔐 Template: Secrets & IAM Patterns

*Powered by [Saturn](https://saturncloud.io) — Secure Cloud Architectures.*

**Hardware:** CPU (Amazon Linux 2023) | **Resource:** Jupyter Notebook | **Tech Stack:** Vault (AWS SSM), Env (`.env`), Python (Boto3) | **Goal:** Secure S3 Access

## 📖 Overview

Hardcoded credentials (`AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`) are the number one cause of cloud security breaches. This template provides the gold-standard architecture for securely accessing Amazon S3 from a Jupyter Notebook.

Instead of typing secret keys into your code, this architecture uses:

1. **IAM Role Assumption:** Grants the notebook temporary, native permissions to AWS resources without static keys.
2. **Vault Integration (AWS SSM Parameter Store):** Securely fetches sensitive configuration (like target bucket names or database connection strings) at runtime.
3. **Env (`.env`):** Loads non-sensitive local environment states seamlessly, keeping code and configuration completely separate.

---

## 🏗️ Phase 1: AWS Cloud Setup

### Step 1.1: Create the Target S3 Bucket

1. Go to the **S3 Dashboard** in the AWS Console and click **Create bucket**.
2. **Name:** Give it a unique name (e.g., `jupyter-vault-data-12345`).
3. Leave all default settings (ensure **Block all public access** remains checked).
4. Click **Create bucket**.
5. Upload a simple test file (like a `.txt` or `.csv`) into the bucket so you have data to read later.

### Step 1.2: Store the Bucket Name in the Vault

We will store the bucket name in AWS Systems Manager (SSM) Parameter Store as an encrypted `SecureString` so it is never hardcoded in our Python script.

1. Go to the **Systems Manager Dashboard**.
2. On the left sidebar, click **Parameter Store**, then click **Create parameter**.
3. **Name:** Type `/jupyter/config/s3_bucket_name`
4. **Tier:** Standard (Free).
5. **Type:** Select **SecureString** *(This encrypts the data using AWS KMS).*
6. **Value:** Type the exact name of your new S3 bucket (e.g., `jupyter-vault-data-12345`).
7. Click **Create parameter**.

### Step 1.3: Create the EC2 IAM Role (Zero-Trust)

1. Go to the **IAM Dashboard**, click **Roles** on the left, and click **Create role**.
2. **Trusted entity type:** Select **AWS service** -> **EC2**. Click Next.
3. **Permissions:** Search for and check these exactly three policies:
* `AmazonS3ReadOnlyAccess` *(Allows reading the S3 data)*
* `AmazonSSMReadOnlyAccess` *(Allows reading the Vault)*
* `AmazonSSMManagedInstanceCore` *(Allows us to connect a secure terminal to the server)*


4. Click Next, name the role `Jupyter-Vault-Role`, and click **Create role**.

---

## 💻 Phase 2: Compute Deployment

### Step 2.1: Launch the EC2 Instance

1. Go to the **EC2 Dashboard** and click **Launch instance**.
2. **Name:** `Jupyter-Vault-Server`
3. **AMI:** Amazon Linux 2023.
4. **Instance Type:** `t2.micro` or `t3.micro`.
5. **Key pair:** Select **Proceed without a key pair** (We will use SSM for secure access).
6. **Advanced Details:** Scroll down to **IAM instance profile** and select the `Jupyter-Vault-Role`.
7. Click **Launch instance**.

### Step 2.2: Install the Tech Stack & Fix Directory Permissions

AWS SSM connections can sometimes drop your terminal into the root system directory (which triggers "Permission Denied" errors in Jupyter). We will explicitly create a user workspace to prevent this.

1. Once running, select the instance and click **Connect** -> **Session Manager** -> **Connect**.
2. Run these commands to install Jupyter, Boto3, and python-dotenv:
```bash
sudo dnf install python3-pip -y
python3 -m pip install jupyterlab boto3 python-dotenv

```


3. Create the workspace and the `.env` file explicitly:
```bash
# Create and enter the exact user directory
mkdir -p /home/ssm-user/notebooks
cd /home/ssm-user/notebooks

# Write environment variables
echo "APP_ENV=production" > .env
echo "REGION=eu-north-1" >> .env 

```


*(Note: Change `eu-north-1` to the region where you built your bucket!)*
4. Start the Jupyter Notebook server securely in the background, enforcing the correct directory:
```bash
/home/ssm-user/.local/bin/jupyter-lab --ip=0.0.0.0 --port=8888 --no-browser --notebook-dir=/home/ssm-user/notebooks &

```


5. Press `Enter`, then grab your unique login token:
```bash
/home/ssm-user/.local/bin/jupyter server list

```


*(Copy the long string of characters after `token=`)*

---

## 🚇 Phase 3: Access the Notebook (Local Tunnel Automation)

Instead of typing out a complex AWS CLI command every time you want to access your notebook, we will create a local shell script to automate the secure tunnel.

**1. Create the Tunnel Script**
On your **local machine** (ensure the AWS CLI is configured and the Session Manager Plugin is installed), open a terminal and create a new script:

```bash
nano start_tunnel.sh

```

**2. Paste the Automation Code**
Paste the following code into the file. **CRITICAL: Update the `TARGET_INSTANCE_ID` and `REGION` variables to match your EC2 instance!**

```bash
#!/bin/bash

# ==========================================
# CONFIGURATION (UPDATE THESE VARIABLES!)
# ==========================================
TARGET_INSTANCE_ID="i-xxxxxxxxxxxxxxxxx"
REGION="eu-north-1"
PORT="8888"
# ==========================================

echo "🚀 Starting Secure SSM Tunnel to EC2 Instance: $TARGET_INSTANCE_ID..."
echo "🌐 Region: $REGION"
echo "🔌 Port Forwarding: Local $PORT -> Remote $PORT"
echo "⚠️  Keep this terminal open! Press Ctrl+C to close the tunnel."
echo ""

aws ssm start-session \
    --target $TARGET_INSTANCE_ID \
    --document-name AWS-StartPortForwardingSession \
    --parameters "portNumber"=["$PORT"],"localPortNumber"=["$PORT"] \
    --region $REGION

```

*(Save and exit: `Ctrl+O`, `Enter`, `Ctrl+X`)*

**3. Run the Tunnel**
Make the script executable and run it:

```bash
chmod +x start_tunnel.sh
./start_tunnel.sh

```

**4. Log In**
Once your terminal says "Port 8888 opened," open your local web browser and explicitly navigate to: `http://localhost:8888`
*(Paste your token from Phase 2 into the password box to log in).*

---

## 📓 Phase 4: The Secure Code Pattern

Create a new Python 3 notebook in Jupyter. Paste and run this exact code block to see the architecture in action.

```python
import os
import boto3
from dotenv import load_dotenv

# ==========================================
# 1. ENV INTEGRATION
# Load local environment configuration
# ==========================================
load_dotenv()
environment = os.getenv("APP_ENV", "development")
region = os.getenv("REGION", "eu-north-1")

print(f"🚀 Initializing Notebook in [{environment}] mode...")

# ==========================================
# 2. VAULT INTEGRATION
# Fetch secure data from AWS Parameter Store
# ==========================================
ssm_client = boto3.client('ssm', region_name=region)

try:
    vault_response = ssm_client.get_parameter(
        Name='/jupyter/config/s3_bucket_name', 
        WithDecryption=True
    )
    SECURE_BUCKET = vault_response['Parameter']['Value']
    print("✅ Vault query successful. Secure configuration loaded.")
except Exception as e:
    print(f"❌ Vault Error: {e}")

# ==========================================
# 3. SECURE S3 ACCESS
# Query the bucket using the decrypted Vault data
# ==========================================
s3_client = boto3.client('s3', region_name=region)

print(f"\n📁 Accessing S3 Bucket: {SECURE_BUCKET}")
try:
    s3_response = s3_client.list_objects_v2(Bucket=SECURE_BUCKET, MaxKeys=5)
    
    if 'Contents' in s3_response:
        for obj in s3_response['Contents']:
            size_kb = round(obj['Size'] / 1024, 2)
            print(f"  - 📄 {obj['Key']} ({size_kb} KB)")
    else:
        print("  - Bucket is empty. (Upload a test file in the AWS Console to see it here!)")
except Exception as e:
    print(f"❌ S3 Access Error: {e}")

```

---

## 🏁 Conclusion

This template successfully demonstrates a **Zero-Trust Architecture** for data science workloads. By entirely removing static access keys and hardcoded secrets from the codebase, we eliminate the risk of accidental credential leaks via GitHub or shared scripts.

The integration of `python-dotenv` ensures local environment flexibility, while **AWS Systems Manager Parameter Store** acts as a robust, encrypted vault for sensitive infrastructure details. Finally, binding permissions directly to the EC2 compute instance via **IAM Roles** guarantees that access rights remain strictly confined to authorized AWS resources, setting a gold standard for secure cloud development.

### 🔗 Verifiable Resources

* **AWS Parameter Store Documentation:** [AWS Systems Manager User Guide](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html)
* **Boto3 SSM Integration:** [Boto3 Docs - SSM Client](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html)
* **Explore More Secure Architectures:** [Saturn Cloud Templates](https://saturncloud.io)

---