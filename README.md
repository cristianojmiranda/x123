# x123

## Install

```
curl -sfL https://raw.githubusercontent.com/cristianojmiranda/x123/master/install.sh | sh -
```

## Scripts

### k3s

 Script tools to work easily with k3s cluster locally
 * **start_k3s** - start a local cluster running inside docker (keep your machine clean from containerds)
 * **stop_k3s** - stop the k3s cluster
 * **remove_k3s** - remove the cluster
 * **reset_k3s** - remove Not Ready nodes from cluster
 * **ssh_k3s** - ssh to cluster node. eg ssh_k3s node_1, ssh_k3s node, ssh_k3s server
 * **scale_k3s** - scale up or down the number of cluster nodes 
 * **bounce_k3s_nodes** - restart all cluster nodes, usefull to bind new images from your local repository
 * **push_k3s_image** - push image from your local docker repo to k3s nodes (`docker save <image> -o /tmp/images/<image>.tar`)


### kubernetes

 Usefull tools to manage kubernetes cluster.

 * **deployment_bounce** - bounce pod by pod from deployment. No downtime.
 * **pod_pf** - port-forward to partial pod name, eg `pod_pf my_app[name] 8080:8081`
 * **svc_pf** - service port-forward
 * **pod_logs** - pod logs by partial pod name
 * **pod_rm** - remove all pods by partial name
 * **pod_ssh** - pod ssh by partial name
 * **kubeconfig_backup** - backup your current kubeconfig file to env name `~/.kube/config_<ENV_NAME>`
 * **kubeconfig_load** - load the kubeconfig file by env (saved by **kubeconfig_backup**)
 * **kk** - kubectl alias
 * **kke** - kubectl by env
 * **kkn** - kubect by namespace
 * **kken** - kubect by env and namespace

### git

 * **gitcl** - `git clone`
 * **gitnb** - create a new branch `git checkout -b <branch>`
 * **gita** - `git add .`
 * **gitco** - `git commit -m`
 * **gitpu** - `git push`
 * **gitacopu** - git add, commit and push
