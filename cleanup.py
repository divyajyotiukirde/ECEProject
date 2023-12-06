import subprocess
import time

# delete completed pods - 
# kubectl delete pod --field-selector=status.phase==Succeeded
# kubectl get pods --no-headers=true | grep "^stress-pod" | awk '{print $1}' | xargs kubectl delete pod

# delete status-completed pods
def clean_pods():
    command = f"kubectl delete pod --field-selector=status.phase==Succeeded"
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print(result.stdout)
    command = f"rm stress-pod-*.yaml"
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def enable_nodes():
    command = f"kubectl uncordon node1.group5project.ufl-eel6871-fa23-pg0.utah.cloudlab.us"
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print(result.stdout)
    command = f"kubectl uncordon node2.group5project.ufl-eel6871-fa23-pg0.utah.cloudlab.us"
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print(result.stdout)


if __name__ == '__main__':
    clean_pods()
    enable_nodes()