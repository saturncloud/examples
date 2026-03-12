import streamlit as st
import os
import boto3

MOUNT_PATH = "${MOUNT_DIR}"
BUCKET_NAME = "${BUCKET_NAME}"
REGION = "${REGION}"

st.set_page_config(page_title="Secure VPC Dashboard", layout="wide")
st.title("🔒 Airgapped S3 Data Gateway")
st.markdown("This dashboard runs securely inside a private VPC, completely isolated from the public internet.")

col1, col2 = st.columns(2)

with col1:
    st.header("📁 Local S3 Mount Viewer")
    try:
        files = os.listdir(MOUNT_PATH)
        st.success(f"Connected to mount: \`{MOUNT_PATH}\`")
        if files:
            for file in files:
                st.write(f"📄 {file}")
        else:
            st.info("The bucket is currently empty.")
    except Exception as e:
        st.error(f"Mount read error. Error: {e}")

with col2:
    st.header("📡 AWS SDK Health Monitor")
    try:
        s3_client = boto3.client('s3', region_name=REGION)
        response = s3_client.list_objects_v2(Bucket=BUCKET_NAME, MaxKeys=5)
        st.success("✅ VPC Endpoint Connection Active")
        
        if 'Contents' in response:
            st.write("**Recent Objects via SDK:**")
            for obj in response['Contents']:
                st.write(f"☁️ \`{obj['Key']}\` ({round(obj['Size'] / 1024, 2)} KB)")
        else:
            st.info("No objects found via SDK.")
    except Exception as e:
        st.error(f"VPC Endpoint connection failed. Error: {e}")