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