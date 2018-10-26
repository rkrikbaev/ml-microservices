#! /bin/bash

function get_pid {
	echo "get pid"
	PID1=$(pgrep -f 'python ./app/app.py')
}

function stop {
   get_pid
   if [ -z $PID1 ]; then
      echo "server is not running."
      exit 1
   else
      echo -n "Stopping server.."
      kill -9 $PID1
      sleep 1
      echo ".. Done."
   fi
}

function start {
   get_pid
   if [ -z $PID1 ]; then
      echo  "Starting server.."
      ./app/app.py &
      get_pid
      echo "Done. PID1=$PID"
   else
      echo "script "./app/app.py" is already running, PID=$PID1"
   fi
}

function restart {

   echo  "Restarting server.."
   get_pid
   if [ -z $PID ]; then
      start
   else
      stop
      sleep 5
      start
   fi
}

function status {

   get_pid
   if [ -z  $PID ]; then
      echo "script "./app/app.py" is not running."
      exit 1
   else
      echo "script "./app/app.py" is running, PID=$PID1"
   fi
}

case "$1" in

   start)
      start
   ;;
   stop)
      stop
   ;;
   restart)
      restart
   ;;
   status)
      status
   ;;

   *)
      echo "Usage: $0 {start|stop|restart|status}"

esac
