# x123

 Tools to make your live easy and fast with kubernetes, k3s, git

## Install

 ```
 curl -sfL https://raw.githubusercontent.com/cristianojmiranda/x123/master/install.sh | sh -
 ```

 > New softwares will be installed in you machine and will be created new shortcuts at `~/bin`.<br />
 > Before intall this make sure that your don't have any conflict of files in `~/bin` with this repo at the risk to be overwritten.<br />
 > The shortcuts could be harmful for you production cluster, use it by your own risk.<br />
 > I recommend you to explore your `~/bin` folder after install or just check `bin` folder on this repo. The documentation could be behind of available shortcuts.<br />

 It'll installed the following softwares if you don't have it:
 * consul
 * vault
 * zsh
 * k3s
 * k9s
 * kubectl
 * atom
 * dot
 * curl
 * python3.7
 * telepresence
 * terminator
 * helm
 * redis-cli

## Scripts and Shortcuts

### k3s

 Script tools to work easily with k3s cluster locally
 * **k3s_start** - start a local cluster running inside docker (keep your machine clean from containerds, **your ~/.kube/config will be replaced**)
 * **k3s_stop** - stop the k3s cluster
 * **k3s_remove** - remove the cluster
 * **k3s_resync_nodes** - sync cluster nodes with docker containers
 * **k3s_ssh** - ssh to cluster node. eg `ssh_k3s node_1`, `ssh_k3s node`, `ssh_k3s server`
 * **k3s_scale** - scale up or down the number of cluster nodes
 * **k3s_bounce_nodes** - restart all cluster nodes, usefull to bind new images from your local repository
 * **k3s_push_image** - push image from your local docker repo to k3s nodes (`docker save <image> -o /tmp/k3s/images/<image>.tar`)
 * **resource_install** - install basic non-HA resource on k3s, like `deploy_resource vault`
 * **helm_install** - install helm chart resources on k3s(generally HA resources), example: `helm_deploy consul,jenkins,redis-ha`

#### HelmChart's

### kubernetes

 Usefull tools to manage kubernetes cluster.

 * **deployment_bounce** - bounce pod by pod from deployment. No downtime.
 * **pod_pf** - port-forward to partial pod name, eg `pod_pf my_app[name] 8080:8081`
 * **pf_holder** - keep the port-forward up, eg `pf_holder <port> <path> <sleep>`, `$(svc_pf sanic 8081:8000 &) & pf_holder 8081`
 * **svc_pf** - service port-forward
 * **pod_logs** - pod logs by partial pod name
 * **pod_rm** - remove all pods by partial name
 * **pod_ssh** - pod ssh by partial name
 * **kubeconfig_backup** - backup your current kubeconfig file to env name _~/.kube/config_<ENV_NAME>_
 * **kubeconfig_load** - load the kubeconfig file by env (saved by **kubeconfig_backup**)
 * **kk** - kubectl alias
 * **kke** - kubectl by env
 * **kkn** - kubect by namespace
 * **kken** - kubect by env and namespace

### git

 * **gitcl** - `git clone`
 * **gitnb** - create a new branch based on fresh master `git checkout -b <branch>`
 * **gitc** - `git checkout`
 * **gitd** - `git diff`
 * **gita** - `git add .`
 * **gitco** - `git commit -m`
 * **gitpu** - `git push`
 * **gitcopu** - git commit and push
 * **gitacopu** - git add -A, commit and push
 * **gitacopucu** - git add -A, commit and push at the current branch
 * **gits** - `git status`

## References
 * [k3s](https://k3s.io/)
 * [consul](https://www.consul.io/)
 * [vault](https://www.vaultproject.io/)
 * [kubernetes](https://kubernetes.io/)
 * [jq](https://stedolan.github.io/jq/)
 * [jqplay](https://jqplay.org/)
 * [cri](https://github.com/kubernetes-sigs/cri-tools/blob/master/docs/crictl.md)
 * [containerd](https://containerd.io/)
 * [runc](https://github.com/opencontainers/runc)
 * [sanic](https://sanic.readthedocs.io/en/latest/)
 * [vertex](https://vertx.io/)
 * [pyYaml](https://pyyaml.org/wiki/PyYAMLDocumentation)
 * [`dot -Tpng diagram.dot -o diagram.png`](https://graphviz.gitlab.io/)
 * [make a graph](https://graphs.grevian.org/graph)
 * [helm](https://helm.sh/)
 * [helmChart's](https://github.com/helm/charts/tree/master/stable)
