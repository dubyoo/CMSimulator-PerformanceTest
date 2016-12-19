#!/bin/bash

function CheckIfStarted()
{
	count=`ps -ef | grep -E "sendtosg.py $1$" | grep -v grep | wc -l`
	return $count
}


function StartSG()
{
	CheckIfStarted $1
	if [ $? -gt 0 ]; then
		echo "Already started $1"
	else
		python sendtosg.py $1 > /dev/null 2>&1 &
		sleep 0.3
		CheckIfStarted $1
		if [ $? -gt 0 ]; then
			echo "Successfully to start $1"
		else
			echo "Failed to start $1"
		fi
	fi
}

function StopSG()
{
	upper=$(echo $1 | tr [A-Z] [a-z])
	if [ $upper == "all" ]; then
		ps -ef | grep "sendtosg.py" | grep -v grep | awk '{print $2}' | xargs kill -9 > /dev/null 2>&1
	else
		ps -ef | grep -E "sendtosg.py $1$" | grep -v grep | awk '{print $2}' | xargs kill -9 > /dev/null 2>&1
	fi

	if [ $? -eq 0 ]; then
        	echo "Successfully to stop $1"
	else
		echo "Failed to stop $1"
	fi
}


path=`dirname $0`
cd $path

#case 1: status
if [[ $# -eq 1 && $1 == "status" ]]; then
	ps -ef | grep "sendtosg.py" | grep -v grep

#case 2: start
elif [[ $# -gt 1 && $1 == "start" ]]; then
	for i in ${@:2:$#}; do
		StartSG $i
	done

#case 3: stop
elif [[ $# -gt 1 && $1 == "stop" ]]; then
	for i in ${@:2:$#}; do
		StopSG $i
	done

#case 4: usage
else
	echo -e "USAGE:\n\t$0 status\n\t$0 start [SGID1] [SGID2] ...\n\t$0 stop [all] | [SGID1] ...\n"
	echo -e "SAMPLE:\n\t$0 status\n\t$0 start 100 101\n\t$0 stop 100 101\n\t$0 stop all\n"
fi


