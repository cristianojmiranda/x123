#!/bin/bash
#set -x
source ./bin/env.sh

mkdir -p ~/bin
mkdir -p $_WORKDIR
mkdir -p $_CONFIG
#rm -rf $_WORKDIR/*

cp -R ./resources $_WORKDIR/

echo "Installing scripts into ~/bin..."
chmod +x ./bin/*
cp ./bin/* ~/bin
echo_green "Done"


#echo
#echo
#sleep 1
#source confirm "Do you want to install the softwares?"
#cd /tmp

# intall jq
if ! type "jq" > /dev/null; then
	echo "Installing jq..."
	sudo apt-get install jq
fi

# intall uuid
if ! type "uuid" > /dev/null; then
	echo "Installing uuid..."
  sudo apt-get install uuid
fi

# intall curl
if ! type "curl" > /dev/null; then
	echo "Installing curl..."
	sudo apt-get install curl
fi

# intall zsh
if ! type "zsh" > /dev/null; then
	echo "Installing zsh..."
	#sh -c "$(wget https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh -O -)"
	sudo apt-get install zsh
fi

# intall k3s
#if ! type "k3s" > /dev/null; then
#	echo "Installing k3s..."
#	wget https://github.com/rancher/k3s/releases/download/v0.2.0/k3s -O k3s
#	chmod +x k3s
#	sudo mv k3s /usr/local/bin
#fi

# install k9s
if ! type "k9s" > /dev/null; then
	echo "Installing k9s..."
	wget https://github.com/derailed/k9s/releases/download/0.2.6/k9s_0.2.6_Linux_x86_64.tar.gz -O k9s.tar.gz
	tar -xvzf k9s.tar.gz
	chmod +x k9s
	sudo mv k9s /usr/local/bin
fi

# intall kubectl
if ! type "kubectl" > /dev/null; then
	echo "Installing kubectl..."
	curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl
	chmod +x ./kubectl
	sudo mv ./kubectl /usr/local/bin/kubectl
fi

# intall vault
if ! type "vault" > /dev/null; then
	echo "Installing vault..."
	wget https://releases.hashicorp.com/vault/1.0.3/vault_1.0.3_linux_amd64.zip -O vault.zip
	unzip vault.zip
	sudo mv vault /usr/local/bin
	chmod +x /usr/local/bin/vault
	rm vault.zip
fi

# intall consul
if ! type "consul" > /dev/null; then
echo "Fetching Consul..."
	CONSUL=1.4.3
	wget https://releases.hashicorp.com/consul/${CONSUL}/consul_${CONSUL}_linux_amd64.zip -O consul.zip --quiet
	echo "Installing Consul..."
	unzip consul.zip >/dev/null
	chmod +x consul
	sudo mv consul /usr/local/bin/consul
	rm consul.zip
fi

# install python3.7
#if ! type "python3.7" > /dev/null; then
#	echo "Installing python3.7..."
#	sudo apt-get install build-essential checkinstall
#	sudo apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev

#	cd /usr/src
#	sudo wget https://www.python.org/ftp/python/3.7.2/Python-3.7.2.tgz
#	sudo tar xzf Python-3.7.2.tgz

#	cd Python-3.7.2
#	sudo ./configure --enable-optimizations
#	sudo make altinstall

	#alias python=python3.7
	#sudo ln -sf /usr/local/bin/python3.7 /usr/bin/python3
#fi

# intall telepresence
#if ! type "telepresence" > /dev/null; then
#	echo "Install telepresence..."
#	curl -s https://packagecloud.io/install/repositories/datawireio/telepresence/script.deb.sh | sudo bash
#	sudo apt install --no-install-recommends telepresence

	#curl -sO https://packagecloud.io/install/repositories/datawireio/telepresence/script.deb.sh
	#sudo env os=ubuntu dist=xenial bash script.deb.sh
	#sudo apt install --no-install-recommends telepresence
	#rm script.deb.sh
#fi

# intall atom
if ! type "atom" > /dev/null; then
	echo "Installing atom..."
	wget https://github.com/atom/atom/releases/download/v1.35.1/atom-amd64.deb -O /tmp/atom.deb
	sudo dpkg -i /tmp/atom.deb
fi

# intall terminator
if ! type "terminator" > /dev/null; then
	echo "Installing terminator..."
	sudo apt-get install terminator
fi


# intall graphviz / dot
if ! type "dot" > /dev/null; then
	echo "Installing graphviz/dot..."
	sudo apt-get install graphviz
	dot -V
fi

# intall helm
#if ! type "helm" > /dev/null; then
#	echo "Installing helm..."
#	wget https://storage.googleapis.com/kubernetes-helm/helm-v2.13.1-linux-amd64.tar.gz -O helm.tar.gz
#	tar -xvzf helm.tar.gz
#	sudo mv linux-amd64/helm /usr/local/bin/helm
#	helm -h
#fi

# intall redis-cli
if ! type "redis-cli" > /dev/null; then
  echo "Installing redis-cli..."
  sudo apt-get install redis-tools
fi

# intall rqlited
if ! type "rqlited" > /dev/null; then
	curl -L https://github.com/rqlite/rqlite/releases/download/v4.4.0/rqlite-v4.4.0-linux-amd64.tar.gz -o rqlite-v4.4.0-linux-amd64.tar.gz
	tar xvfz rqlite-v4.4.0-linux-amd64.tar.gz
	#cd rqlite-v4.4.0-linux-amd64
	sudo mv rqlite-v4.4.0-linux-amd64/rqlited /usr/local/bin/rqlited
	sudo mv rqlite-v4.4.0-linux-amd64/rqlite /usr/local/bin/rqlite
	rm -f *.tar.gz
	rm -rf rqlite-*
fi

# intall asciinema
#if ! type "asciinema" > /dev/null; then
#	echo "Installing asciinema..."
#	sudo apt-add-repository ppa:zanchey/asciinema
#	sudo apt-get update
#  sudo apt-get install asciinema
#fi
