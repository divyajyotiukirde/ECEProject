# read job from job queues
# assign job to pod

import subprocess
import time

# delete completed pods - 
# kubectl delete pod --field-selector=status.phase==Succeeded
# kubectl get pods --no-headers=true | grep "^stress-pod" | awk '{print $1}' | xargs kubectl delete pod

node_map = {
    1: "node1.group5project.ufl-eel6871-fa23-pg0.utah.cloudlab.us",
    2: "node2.group5project.ufl-eel6871-fa23-pg0.utah.cloudlab.us"
}

import random
import string

def generate_random_string(length=4):
    characters = string.ascii_lowercase + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string


def write_yaml(pod_name, args, node, out_file):
    pod_str = f'''
apiVersion: v1
kind: Pod
metadata:
  name: {pod_name}
spec:
  restartPolicy: Never
  containers:
  - image: docker.io/polinux/stress-ng:latest
    name: stress-container
    env:
    - name: DELAY_STARTUP
      value: "20"
    ports:
    - containerPort: 8080
    livenessProbe:
      httpGet:
        path: /actuator/health
        port: 8080
      initialDelaySeconds: 30
    args: [{args}]
  nodeSelector:
    kubernetes.io/hostname: {node_map[node]}
    '''
    with open(out_file, 'w') as f:
        f.write(pod_str)


def start_pod(args, node):
    pod_name = "stress-pod-"+generate_random_string()
    out_file = pod_name + ".yaml"
    write_yaml(pod_name, args, node, out_file)
    command = f"kubectl apply -f {out_file}"
    time.sleep(2)
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print("executed ",result.stdout)


def kill_pod():
    pass

def kill_node():
    pass



