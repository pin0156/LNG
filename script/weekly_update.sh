#!/bin/bash

HOME_PATH="/home/ec2-user/LNG"
cd "$HOME_PATH/script"
pwd
sh build_lotto_dic.sh
cp ../data/lotto_statistics.json ../www/data/lotto_statistics.json
echo "call api: LNG_reload_dic"
curl localhost/LNG_reload_dic
