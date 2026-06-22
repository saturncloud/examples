#!/bin/bash

echo "🛑 Destroying KAOS Kubernetes namespace..."
# This deletes all pods, deployments, and services safely
kubectl delete namespace kaos-system

echo "💤 Stopping Minikube cluster..."
# This spins down the virtualized Kubernetes environment
minikube stop

echo "🧹 Clean up complete! System RAM and CPU freed."
