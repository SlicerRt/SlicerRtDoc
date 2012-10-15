#!/bin/sh
# Continuous build - to be started by cron daemon at regular short time intervals to check for changes in the repository. It performs the tests if there is a change. If a build is already in progress (lock file exists) then it does not do anything

cd /home/perklab/Devel/SlicerRT_R64-bin
logFileName=/home/perklab/Devel/Scripts/Logs/SlicerRtLogContinuous-$(date +%F-%H%M%S).log
lockFileName=/home/perklab/Devel/Scripts/TestSlicerRtContinuous.lock

date > $logFileName
whoami >> $logFileName
env >> $logFileName
echo ------------------ >> $logFileName

if [ ! -e $lockFileName ]; then
  trap "rm -f $lockFileName; exit" INT TERM EXIT
  touch $lockFileName

  export DISPLAY=:0.0 # Enable application to use the X server
  ctest -S /home/perklab/Devel/Scripts/Perklab-Virtualbox_Linux-64bits_SlicerRt_Release_Continuous.cmake -VV | tee -a $logFileName

  rm $lockFileName
  trap - INT TERM EXIT
else
  echo "SlicerRt test is already running" >> $logFileName
fi

echo ------------------ >> $logFileName
date >> $logFileName

