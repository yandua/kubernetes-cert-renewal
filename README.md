# Kubernetes Certificate Renewal Tool
Inspired by Kelsey Hightower's work on Kubernetes The Hard Way, https://github.com/kelseyhightower/kubernetes-the-hard-way/commit/5c462220b7f2c03b4b699e89680d0cc007a76f91.

Re-generates all of Kubernetes' Cluster certificates (ca, kube-proxy, kubelet, kube-api-server, controller manager, etcd) using pre-existing CSR and CA-config files and cfssl tool by running  shell commands.

Tool assumes that .csr files for specific function are put in tool's local folder - otherwise it will fail.

Update clusterinfo.csv with information about your cluster:
 * information for cluster's IPs is used for API server certificate generation. Don't forget to put 127.0.0.1 and external load balancer's IP. Second column is empty
 * information for cluster's hostnames is used for API server certificate generation. Put all of cluster's hostnames here. Second column is empty
 * information about in workers row is used to generate worker-specific kubelet certificate and, in future, during certificate distribution
 * information about controllers will be eventually used during certificate distribution process

Usage:
```

python3 cert-renewal.py
``` 


Future work - automated csr creation, certificate distribution, automated service restart
