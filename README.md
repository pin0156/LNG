# LNG

## Requirement
 * python2.7

## How to use
 * colone git
```
git clone https://github.com/pin0156/LNG.git
```
 * build dic
```
cd script
sh build_lotto_dic.sh
```
 * test
```
cd src
./search_lotto_number.py

input test:
case1: 1
case2: 45
case3: 1,45
case4: 45,1
case5: 1,2,3
case6: 3,1,2
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
