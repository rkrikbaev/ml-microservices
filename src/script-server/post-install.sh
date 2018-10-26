#!/bin/bash

#BIN_DIR=
#DATA_DIR=
#LOG_DIR=
SCRIPT_DIR=/opt/script-server/src/script-server
#LOGROTATE_DIR=/etc/logrotate.d

#function install_init {
#    cp -f $SCRIPT_DIR/init.sh /etc/init.d/flask-core
#    chmod +x /etc/init.d/influxdb-relay
#}

function install_systemd {
	echo 0
    	cp -f $SCRIPT_DIR/flask-core.service /etc/systemd/system/flask-core.service
    	systemctl enable flask-core.service
	}

function install_chkconfig {
    	chkconfig --add flask-core
	}

if [[ $? -eq 0 ]]; then
		install_systemd
		echo 1
	else
		#install_init
		install_chkconfig
		echo 2
	fi

