#!/bin/bash

set -o nounset
set -o errexit

VERBOSE_MODE=0

function error_handler()
{
  local STATUS=${1:-1}
  [ ${VERBOSE_MODE} == 0 ] && exit ${STATUS}
  echo "Exits abnormally at line "`caller 0`
  exit ${STATUS}
}
trap "error_handler" ERR

PROGNAME=`basename ${BASH_SOURCE}`
DRY_RUN_MODE=0

function print_usage_and_exit()
{
  set +x
  local STATUS=$1
  echo "Usage: ${PROGNAME} [-v] [-v] [--dry-run] [-h] [--help] [mode] [process]"
  echo ""
  echo " mode                0 : devel,  1 : service"
  echo " process             0 : max to #core, [1...n] : number of process"
  echo " Options -"
  echo "  -v                 enables verbose mode 1"
  echo "  -v -v              enables verbose mode 2"
  echo "      --dry-run      show what would have been dumped"
  echo "  -h, --help         shows this help message"
  exit ${STATUS:-0}
}

function debug()
{
  if [ "$VERBOSE_MODE" != 0 ]; then
    echo $@
  fi
}

GETOPT=`getopt -o vh --long dry-run,help -n "${PROGNAME}" -- "$@"`
if [ $? != 0 ] ; then print_usage_and_exit 1; fi

eval set -- "${GETOPT}"

while true
do case "$1" in
     -v)            let VERBOSE_MODE+=1; shift;;
     --dry-run)     DRY_RUN_MODE=1; shift;;
     -h|--help)     print_usage_and_exit 0;;
     --)            shift; break;;
     *) echo "Internal error!"; exit 1;;
   esac
done

if (( VERBOSE_MODE > 1 )); then
  set -x
fi


# template area is ended.
# -----------------------------------------------------------------------------
if [ ${#} != 2 ]; then print_usage_and_exit 1; fi

# current dir of this script
CDIR=`pwd`

[[ -f ${CDIR}/env.sh ]] && . ${CDIR}/env.sh || exit

# -----------------------------------------------------------------------------
# functions

function check_running
{
	progname=$1
	count_pgrep=`pgrep -f ${progname} | wc -l`
	count_pgrep=$(( ${count_pgrep} - 1 ))
	if (( count_pgrep > 0 )); then
		revert_calmness
		echo "count_pgrep = ${count_pgrep}"
		echo "${progname} is already running"
		exit 0
	fi
}


# end functions
# -----------------------------------------------------------------------------



# -----------------------------------------------------------------------------
# main 

make_calmness
child_verbose=""
if (( VERBOSE_MODE > 1 )); then
	revert_calmness
	child_verbose="-v -v"
fi

MODE=$1
PROCESS=$2

check_running ${daemon_name}

# copy resources
function copy_resources {
	cp -rf ${PDIR}/src/*.py ${CDIR}/lib/.
	cp -rf ${PDIR}/data/lotto_statistics.json ${CDIR}/data/.
}
copy_resources

cd ${CDIR}

if (( MODE == 0 )); then
	nohup ${python} ${CDIR}/${daemon_name} --debug=True --port=${port_devel} --log_file_prefix=${CDIR}/log/access.log > /dev/null 2> /dev/null &
else
	sudo ${python}  ${CDIR}/${daemon_name} --debug=False --port=${port_service} --process=${PROCESS} --log_file_prefix=${CDIR}/log/access.log > /dev/null 2> /dev/null &
fi
cd ${CDIR}

close_fd

# end main
# -----------------------------------------------------------------------------
