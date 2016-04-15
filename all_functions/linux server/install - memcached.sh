#!/bin/sh
# Change this to the last working Libs (may be you have to try and error)

mkdir $OPENSHIFT_HOMEDIR/app-root/runtime/tmp/
mkdir  $OPENSHIFT_HOMEDIR/app-root/runtime/srv/memcached

if [ ! -d "$OPENSHIFT_HOMEDIR/app-root/runtime/srv/memcached/bin" ]; then
	cd $OPENSHIFT_HOMEDIR/app-root/runtime/tmp
	rm -rf *

	# Download memcached
	wget http://memcached.org/latest
	mv latest  memcached-1.x.x.tar.gz
	tar -zxvf memcached-1.x.x.tar.gz
	cd memcached-1.*.*	
	nohup sh -c "./configure --prefix=$OPENSHIFT_HOMEDIR/app-root/runtime/srv/memcached"  > $OPENSHIFT_LOG_DIR/memcached_install_conf.log /dev/null 2>&1 &  
	tail -f $OPENSHIFT_LOG_DIR/memcached_install_conf.log
	nohup sh -c "make && make test && make install && make clean"  > $OPENSHIFT_LOG_DIR/memcached_install.log 2>&1 &  
	tail -f $OPENSHIFT_LOG_DIR/memcached_install.log
	
	#memcached for python
	wget ftp://ftp.tummy.com/pub/python-memcached/python-memcached-latest.tar.gz
	tar -zxvf python-memcached-latest.tar.gz
	cd python-memcached-*
	export PATH=${PATH}:$OPENSHIFT_HOMEDIR/app-root/runtime/srv/python/bin/
	$OPENSHIFT_HOMEDIR/app-root/runtime/srv/python/bin/python setup.py install
	
	
	
	
	
fi
mkdir  $OPENSHIFT_HOMEDIR/app-root/runtime/srv/sproxy

if [ ! -d "$OPENSHIFT_HOMEDIR/app-root/runtime/srv/sproxy/bin" ]; then
	cd $OPENSHIFT_HOMEDIR/app-root/runtime/tmp
	rm -rf *


	wget ftp://ftp.joedog.org/pub/sproxy/sproxy-latest.tar.gz
	tar xzvf  sproxy-latest.tar.gz
	nohup sh -c "./configure --prefix=$OPENSHIFT_HOMEDIR/app-root/runtime/srv/sproxy"  > $OPENSHIFT_LOG_DIR/sproxy_install_conf.log /dev/null 2>&1 &  
	tail -f $OPENSHIFT_LOG_DIR/sproxy_install_conf.log
	nohup sh -c "make && make install && make clean"  > $OPENSHIFT_LOG_DIR/sproxy_install.log 2>&1 &  
	tail -f $OPENSHIFT_LOG_DIR/sproxy_install.log
	
fi
cd $OPENSHIFT_HOMEDIR/app-root/runtime/tmp
rm -rf *
### The url list will be written in ~/urls.txt, you can override this using he flag -o: for example:
#sproxy -o /home/user/benchmark/urls.txt
echo "*****************************"
echo "***  		  USAGE         ***"

#$OPENSHIFT_HOMEDIR/app-root/runtime/srv/memcached/bin/memcached -u http://ponisha.ir -d1 -r200 -c25
#$OPENSHIFT_HOMEDIR/app-root/runtime/srv/memcached/bin/memcached  --header='Host: ponisha.ir' --reps=1000 --time=300H --concurrent=10 --quiet --delay=1 http://ponisha.ir 
#$OPENSHIFT_HOMEDIR/app-root/runtime/srv/memcached/bin/memcached  --header='Host: ponisha.ir' --reps=1000 --time=300H --concurrent=1 --quiet --delay=0 http://bigfishs.tk/


###FROM https://usu.li/simulate-real-users-load-on-a-webserver-using-memcached-and-sproxy/
#$OPENSHIFT_HOMEDIR/app-root/runtime/srv/memcached/bin/memcached -v -c 50 -i -t 3M -f uniq_urls.txt -d 10
echo "*****************************"


echo "*****************************"
echo "***  F I N I S H E D !!   ***"
echo "*****************************"
