# x123

## Install

```
curl -sfL https://raw.githubusercontent.com/cristianojmiranda/x123/master/install.sh | sh -
```

## scripts

### k3s

 Script tools to handle easly with k3s cluster locally
 *start_k3s* - start a local cluster running inside docker (keep your machine clean from containerds)
 *stop_k3s* - stop the k3s cluster
 *remove_k3s* - remove the
 *ssh_k3s* - ssh to cluster node. eg ssh_k3s node_1, ssh_k3s node, ssh_k3s server
 *scale_k3s* - scale up or down the number of cluster nodes 
 *bounce_k3s_nodes* - restart all cluster nodes, usefull to bind new images from your local repository
 *push_k3s* - push image from your local docker repo to k3s nodes (docker save <image> -o /tmp/images/<image>.tar)

### kubernetes

### git

gitcl - git clone
gitnb - git checkout -b <branch>
gita - git add .
