# LNG

## build dic
```
cd script
sh build_lotto_dic.sh
```

## test
```
cd src
./search_lotto_number.py --lotto_dic=../data/lotto_statistics.json

input test:
case1: 1
case2: 45
case3: 1,45
case4: 1,2,3
```

## web service test
 * install www package
```
sudo pip install tornado
```

 *  start service
```
cd www
./start.sh -v -v 0 1
```
