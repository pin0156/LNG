#!/bin/bash

set -o errexit

export LC_ALL=ko_KR.UTF-8
export LANG=ko_KR.UTF-8

# directory
## current dir of this script
CDIR=`pwd`
PDIR=`dirname $CDIR`

# server 
daemon_name='lng_dm.py'
port_devel=8080
port_service=80

# resources
DATA_DIR=${PDIR}/data

# command setting
python='/usr/bin/python2.7'

# functions

function make_calmness()
{
	exec 3>&2 # save 2 to 3
	exec 2> /dev/null
}

function revert_calmness()
{
	exec 2>&3 # restore 2 from previous saved 3(originally 2)
}

function close_fd()
{
	exec 3>&-
}

function jumpto
{
	label=$1
	cmd=$(sed -n "/$label:/{:a;n;p;ba};" $0 | grep -v ':$')
	eval "$cmd"
	exit
}
