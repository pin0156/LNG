#!/bin/bash

# get update data
last_lotto_num_in_file=`tail -1 ../data/lotto_data.json | python -c 'import json; import sys; line=sys.stdin.readline(); data=json.loads(line); print data["drwNo"]'`
start_lotto_num=$(($last_lotto_num_in_file + 1));

date=`date "+%Y.%m.%d"`
end_y=`date "+%Y"`
end_m=`date "+%m"`
end_d=`date "+%d"`
end_lotto_num=`python -c 'import sys; from datetime import date; d=date(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])) - date(2002,12,07); print d.days/7' $end_y $end_m $end_d`

echo "last lotto number in lotto_data file : $last_lotto_num_in_file"
echo "last lotto number (today: $date): $end_lotto_num"
if [ $last_lotto_num_in_file -eq $end_lotto_num ]; then
	echo "Do not update"
	exit
fi

URL="https://www.nlotto.co.kr/common.do"
#URL="https://dhlottery.co.kr/common.do"
outfile=../data/lotto_data.json
echo "download lotto date: $start_lotto_num ~ $end_lotto_num"
echo "update lotto data file: $outfile"
for i in `seq $start_lotto_num $end_lotto_num`
do
	wget --no-check-certificate -O- "${URL}?method=getLottoNumber&drwNo=$i" >> $outfile
	echo "" >> $outfile
done
