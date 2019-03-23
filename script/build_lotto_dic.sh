#!/bin/bash

echo "download data"
sh download_data.sh

echo ""
echo "build lotto dic"
python build_lotto_dic.py < ../data/lotto_data.json > ../data/lotto_statistics.json
