#!/bin/bash
cd /tmp
git clone https://github.com/cristianojmiranda/x123.git
cd x123
./install_me.sh
cd ..
rm -rf x123
echo "Done"
