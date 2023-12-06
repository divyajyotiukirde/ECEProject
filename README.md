# ECEProject

# Execution

To execute the Task 3 code:

Clone this repository and cd into the directory.

Start the proxy server. Our metrics server depends on it.

```
kubectl proxy &
```

```
python3 main.py <job_simulation_file.txt>
```

Make sure to run `cleanup.py` before and after executing the above main file, to cleanup and make nodes active.

For monitoring of cluster, execute:

```
python3 start_monitor.py
```

## Code Structure
  
Files

- **main.py**: This is start of the program. It starts the job scheduling and Global controller takes over for assignment of jobs.
- **start_monitor.py**: The driver code for monitoring. Should be started parallely.
- **monitor.py**: The functions in these return the utlization metrics to feed to the Controllers.
- **middleware.py**: The code that administrates pod creation.
- **LocalController.py**: The Controller class for individual nodes.
- **GlobalController.py**: The Controller class for the cluster.
- **cleanup.py**: To cleanup the pods and enable nodes.

# Extra Credit - REST APIs

Do this for all nodes

For creating image

```bash
cd python-docker
docker build -t python-docker .
docker images
```


## Metal LB (Network Load Balancer)

```
kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.13.12/config/manifests/metallb-native.yaml
```


### Apply the following yaml file

```
apiVersion: metallb.io/v1beta1
kind: IPAddressPool
metadata: 
  name: first-pool
  namespace: metallb-system
spec:
  addresses: 
  - 128.110.217.70-128.110.217.75
```


### Applying the following L2 advertisement

```
apiVersion: metallb.io/v1beta1
kind: L2Advertisement
metadata:
  name: group5
  namespace: metallb-system
spec:
  ipAddressPools:
  - first-pool
```



### Applying nginx ingress

```
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.2/deploy/static/provider/cloud/deploy.yaml
```


### Apply the deployment yaml file


### Add the External IP from the ingress-controller

```
$ kubectl get service ingress-nginx-controller --namespace=ingress-ngin
$ kubectl get ingress
```


```
sudo vi /etc/hosts 
```


```
128.110.217.71 	cloud-controller.com
```

# Extra Credit - Logs from Fluentbit
To install Fluentbit and run it as containers in node1 and node2.

The installing command have beed added into Makefile:
```bash
sudo make
```
Create a configuration file for Fluent Bit, which is fluent-bit-config.yaml.
Deploy Fluent Bit as a DaemonSet so that it runs on every node in your Kubernetes cluster by ceating fluent-bit-daemonset.yaml.
Both files have beed added into repo.

Get necessary permission to list events at the luster scope, fix role-based access control (RBAC) issue:
Create a ClusterRole that grants access to the events resources. 
Create a ClusterRoleBinding to grant the events-reader role to the default service account in the logging namespace.
```bash
kubectl apply -f events-clusterrole.yaml
kubectl apply -f events-clusterrolebinding.yaml
```

Apply configure files.
```bash
kubectl create namespace logging
kubectl apply -f fluent-bit-config.yaml
kubectl apply -f fluent-bit-daemonset.yaml
```
To check, run command. It should show two pods running in node1 and node2.
```bash
kubectl get pods -n logging
```
To get logs, run command
```bash
sudo kubectl logs -n logging [Pod name, like fluent-bit-xxx]
```
