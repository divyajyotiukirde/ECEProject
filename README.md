# ECEProject


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