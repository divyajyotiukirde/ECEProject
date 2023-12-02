import requests
from kubernetes import client, config

# Configuration
METRICS_SERVER_URL = "http://localhost:8001"
# KUBERNETES_API_URL = "https://128.110.217.55:6443"
SAMPLING_RATE = 60  # in seconds

def get_pod_status():
    config.load_kube_config()
    v1 = client.CoreV1Api()
    try:
        pods = v1.list_pod_for_all_namespaces()
        for pod in pods.items:
            print(f"Pod: {pod.metadata.name}, Status: {pod.status.phase}")
    except Exception as e:
        print(f"Error fetching pod status: {e}")


def process_pod_metrics(pod_metrics):
    for item in pod_metrics['items']:
        pod_name = item['metadata']['name']
        namespace = item['metadata']['namespace']
        for container in item['containers']:
            container_name = container['name']
            cpu_usage_nano = int(container['usage']['cpu'].rstrip('n'))
            cpu_usage_milli = cpu_usage_nano / 1e6  # Convert nanocores to millicores
            print(f"Pod: {pod_name}, Namespace: {namespace}, Container: {container_name}, CPU Usage: {cpu_usage_milli:.2f} millicores")

def process_node_metrics(node_metrics):
    for item in node_metrics['items']:
        node_name = item['metadata']['name']
        cpu_usage_nano = int(item['usage']['cpu'].rstrip('n'))
        cpu_usage_milli = cpu_usage_nano / 1e6  # Convert nanocores to millicores
        print(f"Node: {node_name}, CPU Usage: {cpu_usage_milli:.2f} millicores")

def get_cpu_utilization():
    pod_metrics_url = f"{METRICS_SERVER_URL}/apis/metrics.k8s.io/v1beta1/pods"
    node_metrics_url = f"{METRICS_SERVER_URL}/apis/metrics.k8s.io/v1beta1/nodes"

    try:
        # Fetch Pod metrics
        pod_response = requests.get(pod_metrics_url)
        pod_metrics = pod_response.json()
        process_pod_metrics(pod_metrics)

        # Fetch Node metrics
        node_response = requests.get(node_metrics_url)
        node_metrics = node_response.json()
        process_node_metrics(node_metrics)

    except requests.RequestException as e:
        print(f"Error fetching metrics: {e}")

def get_node_cpu_utilization(node):
    node_metrics_url = f"{METRICS_SERVER_URL}/apis/metrics.k8s.io/v1beta1/nodes"
    node_response = requests.get(node_metrics_url)
    node_metrics = node_response.json()
    for i in range(len(node_metrics['items'])):
        item = node_metrics['items'][i]
        node_name = item['metadata']['name']
        cpu_usage_nano = int(item['usage']['cpu'].rstrip('n'))
        cpu_usage_milli = cpu_usage_nano / 1e6  # Convert nanocores to millicores
        if node==i:
            break
    cpu = cpu_usage_milli
    cpu_capacity = 16000
    return cpu/cpu_capacity

def get_cluster_utilization():
    node_metrics_url = f"{METRICS_SERVER_URL}/apis/metrics.k8s.io/v1beta1/nodes"
    node_response = requests.get(node_metrics_url)
    node_metrics = node_response.json()
    cpu_capacity = 16000
    cpu = 0
    for i in range(len(node_metrics['items'])):
        if i==0:
            continue
        item = node_metrics['items'][i]
        node_name = item['metadata']['name']
        cpu_usage_nano = int(item['usage']['cpu'].rstrip('n'))
        cpu_usage_milli = cpu_usage_nano / 1e6  # Convert nanocores to millicores
        cpu += (cpu_usage_milli/cpu_capacity)
    # return overall
    return cpu/2
        