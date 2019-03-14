#!/bin/bash
#set -x
source ./bin/env.sh

mkdir -p ~/bin
mkdir -p $_WORKDIR
rm -rf $_WORKDIR/*

cp -R ./resources $_WORKDIR/

chmod +x ./bin/*
cp ./bin/* ~/bin

cd /tmp

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
if ! type "k3s" > /dev/null; then
	echo "Installing k3s..."
	wget https://github.com/rancher/k3s/releases/download/v0.2.0/k3s -O k3s
	chmod +x k3s
	sudo mv vault /usr/local/bin
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
if ! type "python3.7" > /dev/null; then
	echo "Installing python3.7..."
	sudo apt-get install build-essential checkinstall
	sudo apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev

	cd /usr/src
	sudo wget https://www.python.org/ftp/python/3.7.2/Python-3.7.2.tgz
	sudo tar xzf Python-3.7.2.tgz

	cd Python-3.7.2
	sudo ./configure --enable-optimizations
	sudo make altinstall

	#alias python=python3.7
	#sudo ln -sf /usr/local/bin/python3.7 /usr/bin/python3
fi

# intall telepresence
if ! type "telepresence" > /dev/null; then
	echo "Install telepresence..."
	curl -s https://packagecloud.io/install/repositories/datawireio/telepresence/script.deb.sh | sudo bash
	sudo apt install --no-install-recommends telepresence

	#curl -sO https://packagecloud.io/install/repositories/datawireio/telepresence/script.deb.sh
	#sudo env os=ubuntu dist=xenial bash script.deb.sh
	#sudo apt install --no-install-recommends telepresence
	#rm script.deb.sh
fi

# intall atom
if ! type "atom" > /dev/null; then
	echo "Installing atom..."
	wget https://github.com/atom/atom/releases/download/v1.35.1/atom-amd64.deb -O /tmp/atom.deb
	sudo dpkg -i /tmp/atom.deb
fi
