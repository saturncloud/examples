
### 1. The Network (Click-by-Click Guide)

To guarantee complete isolation, we will build a VPC that physically cannot route traffic to the public internet.

#### Step 1.1: Create the Isolated VPC

1. Log into the AWS Management Console and navigate to the **VPC Dashboard**.
2. Click the orange **Create VPC** button.
3. Under *Resources to create*, select **VPC and more**.
4. **Name tag auto-generation:** Enter `airgapped-vpc`.
5. **IPv4 CIDR block:** Leave as default (usually `10.0.0.0/16`).
6. **Number of Availability Zones:** Select **1** (to keep costs down).
7. **Number of public subnets:** Select **0** *(CRITICAL: This ensures no Internet Gateway is created).*
8. **Number of private subnets:** Select **1**.
9. **NAT gateways ($):** Select **None** *(CRITICAL: This ensures the private subnet cannot leak to the internet).*
10. **VPC endpoints:** Select **None** (We will configure these explicitly in the next steps).
11. Click **Create VPC**.

#### Step 1.2: Create the Internal Security Group

Before we create our endpoints, we need a firewall rule that allows our VPC to talk to itself internally.

1. On the left sidebar of the VPC Dashboard, click **Security Groups**.
2. Click **Create security group**.
3. **Security group name:** `airgapped-internal-sg`.
4. **VPC:** Select your new `airgapped-vpc` from the dropdown.
5. **Inbound rules:** Click **Add rule**.
* **Type:** Select `HTTPS` (Port 443 is required for SSM Interface Endpoints).
* **Source:** Select `Custom` and type in your VPC's CIDR block (e.g., `10.0.0.0/16`).


6. Click **Create security group**.

#### Step 1.3: Create the S3 Gateway Endpoint

This endpoint acts as a secret backdoor, allowing your EC2 instance to reach S3 securely without traversing the public internet.

1. On the left sidebar of the VPC Dashboard, click **Endpoints**.
2. Click **Create endpoint**.
3. **Name tag:** `s3-gateway-endpoint`.
4. **Service category:** Select **AWS services**.
5. **Services:** In the search bar, type `s3` and press Enter.
6. Look at the *Type* column. You must select the one that says **Gateway** (e.g., `com.amazonaws.eu-north-1.s3`).
7. **VPC:** Select `airgapped-vpc`.
8. **Route tables:** Check the box next to the route table associated with your private subnet. *(This automatically injects the route so your server knows how to find S3).*
9. Click **Create endpoint**.

#### Step 1.4: Create the SSM Interface Endpoints

Because your EC2 instance has no internet, you cannot SSH into it normally. AWS Systems Manager (SSM) allows secure terminal access, but it requires three specific "Interface" endpoints to function offline.

You will repeat this exact process **three times**, once for each required service:

1. Click **Create endpoint**.
2. **Name tag:** `ssm-endpoint-1` (then 2, then 3).
3. **Service category:** **AWS services**.
4. **Services:** Search for and select the following services one by one (Ensure the *Type* says **Interface**):
* First endpoint: `com.amazonaws.[your-region].ssm`
* Second endpoint: `com.amazonaws.[your-region].ssmmessages`
* Third endpoint: `com.amazonaws.[your-region].ec2messages`


5. **VPC:** Select `airgapped-vpc`.
6. **Subnets:** Check the box for your one Availability Zone, then select your private subnet.
7. **Security groups:** Check the box for the `airgapped-internal-sg` you created in Step 1.2.
8. Click **Create endpoint**. *(Repeat until all 3 are created).*

---

### 2. Identity & Security (IAM Role & S3 Policy)

Before we launch the server, we need to give it an "ID Badge" (IAM Role) and lock down the S3 bucket so it strictly trusts that badge and your internal network.

#### Step 2.1: Create the EC2 IAM Role

1. Navigate to the **IAM Dashboard** in the AWS Console.
2. On the left sidebar, click **Roles**, then click the orange **Create role** button.
3. **Trusted entity type:** Select **AWS service**.
4. **Use case:** Select **EC2** and click **Next**.
5. **Add permissions:** Use the search bar to find and check the boxes next to these two exact policies:
* `AmazonSSMManagedInstanceCore` *(Allows the SSM tunnel to connect)*
* `AmazonS3FullAccess` *(Allows the server to read/write to your bucket)*


6. Click **Next**.
7. **Role name:** Type `Airgapped-EC2-Role`.
8. Click **Create role**.

#### Step 2.2: Create and Lock Down the S3 Bucket

1. Navigate to the **S3 Dashboard**.
2. Click **Create bucket**.
3. **Bucket name:** Choose a globally unique name (e.g., `airgapped-vpc-ssm`).
4. Leave all other settings as default (Ensure "Block all public access" remains **checked**) and click **Create bucket**.
5. Open your new bucket by clicking its name, then navigate to the **Permissions** tab.
6. Scroll down to **Bucket policy** and click **Edit**.
7. Paste the strict Zero-Trust policy below. **CRITICAL:** You must replace the `YOUR_BUCKET_NAME` with your actual bucket name, and replace `vpce-XXXXXXXXXXXXXXXXX` with the actual ID of the S3 Gateway Endpoint you created in Step 1.3!

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VPCOnlyAccess",
            "Effect": "Deny",
            "Principal": "*",
            "Action": "s3:*",
            "Resource": [
                "arn:aws:s3:::YOUR_BUCKET_NAME",
                "arn:aws:s3:::YOUR_BUCKET_NAME/*"
            ],
            "Condition": {
                "StringNotEquals": {
                    "aws:sourceVpce": "vpce-XXXXXXXXXXXXXXXXX"
                }
            }
        }
    ]
}

```

8. Click **Save changes**. *(Note: You will immediately see an "Access Denied" error in your browser. This proves the airgap is working, as your browser is not inside the VPC!)*

---

## 💾 Phase 2: EC2 Deployment & S3 Mountpoint (Click-by-Click)

Now we drop the server straight into the airgapped vault.

#### Step 2.1: Launch the Airgapped EC2 Instance

1. Navigate to the **EC2 Dashboard** and click **Launch instance**.
2. **Name:** `Airgapped-Dashboard-Server`.
3. **Application and OS Images (AMI):** Select **Amazon Linux 2023 AMI**.
4. **Instance type:** Select **t2.micro** or **t3.micro** (CPU is all we need).
5. **Key pair (login):** Select **Proceed without a key pair** from the dropdown. *(We do not need SSH keys because we are using SSM!)*
6. **Network settings:** Click the **Edit** button in this box.
* **VPC:** Select your `airgapped-vpc`.
* **Subnet:** Select your private subnet.
* **Auto-assign public IP:** Select **Disable**. *(Crucial for the airgap).*
* **Firewall (security groups):** Click **Select existing security group** and choose your `airgapped-internal-sg`.


7. **Advanced details:** Expand this bottom section, scroll down to **IAM instance profile**, and select your `Airgapped-EC2-Role`.
8. Click the orange **Launch instance** button.

#### Step 2.2: Connect and Mount S3

1. Wait a few minutes for the instance state to show "Running".
2. Select the instance, click the **Connect** button at the top of the screen.
3. Select the **Session Manager** tab and click **Connect**. A black terminal will open in your browser.
4. Run these exact commands to attach your S3 bucket as a local folder:

```bash
sudo mkdir -p /mnt/s3-data
sudo chmod 777 /mnt/s3-data
sudo dnf install mount-s3 -y
mount-s3 YOUR_BUCKET_NAME /mnt/s3-data

```

---

## 📦 Phase 3: The "Airgap Bypass" (Dependency Smuggling)

Because the server has zero internet access, standard Python package installations will fail. We must smuggle them in.

#### Step 3.1: Package the Files Locally

Open a terminal on your **local, internet-connected laptop** (e.g., your Kali Linux terminal) and run:

```bash
mkdir sm_packages_linux
pip download --only-binary=:all: --platform manylinux2014_x86_64 --python-version 39 streamlit boto3 -d sm_packages_linux
zip -r sm_packages_linux.zip sm_packages_linux

```

#### Step 3.2: Smuggle via S3

1. Go to your **EC2 Session Manager Terminal** and temporarily delete the strict bucket policy so you can upload from your browser:
```bash
aws s3api delete-bucket-policy --bucket YOUR_BUCKET_NAME

```


2. Go back to your **AWS S3 Console** in your web browser. Refresh the page.
3. Click **Upload** and drop your `sm_packages_linux.zip` file into the bucket.
4. **CRITICAL:** Once uploaded, immediately go back to the S3 **Permissions** tab and paste your strict Bucket Policy back in to lock the vault!

#### Step 3.3: Offline Installation

Go back to your **EC2 Session Manager Terminal** and unpack the smuggled files:

```bash
# Install pip securely via Amazon's internal S3 repos
sudo dnf install python3-pip -y

# Move the zip file out of the S3 mount to allow unzipping
cd ~
cp /mnt/s3-data/sm_packages_linux.zip .
unzip sm_packages_linux.zip

# Install strictly offline, bypassing any OS-level conflicts
python3 -m pip install --user --no-index --find-links=sm_packages_linux/ streamlit boto3

```

---

## 📊 Phase 4: Application Deployment & Tunneling

#### Step 4.1: Create and Run the Dashboard

In your **EC2 Session Manager Terminal**, create the file:

```bash
nano app.py

```

*(Paste the Python code from the Overview section here, save with `Ctrl+O` -> `Enter`, and exit with `Ctrl+X`)*.

Run the dashboard using the explicit user path:

```bash
/home/ssm-user/.local/bin/streamlit run app.py

```

*(Leave this terminal running!)*

#### Step 4.2: Build the Secure Tunnel (Local Laptop)

Open a new terminal on your **local laptop**. Ensure your AWS CLI is configured (`aws configure`) with an IAM user that has Administrative or SSM access.

Run the tunnel command:

```bash
aws ssm start-session \
    --target i-XXXXXXXXXXXXXXXXX \
    --document-name AWS-StartPortForwardingSession \
    --parameters "portNumber"=["8501"],"localPortNumber"=["8501"] \
    --region eu-north-1

```

*(Replace `i-XXXXXXXXXXXXXXXXX` with your actual EC2 Instance ID, found on the EC2 Dashboard).*

#### Step 4.3: View the Dashboard

Once your local terminal says `Waiting for connections...`, open your local web browser and explicitly type **HTTP** (not HTTPS):

```text
http://localhost:8501

```