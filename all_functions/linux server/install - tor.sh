#!/bin/sh
# Change this to the last working Libs (may be you have to try and error)

mkdir $OPENSHIFT_HOMEDIR/app-root/runtime/tmp/
mkdir  $OPENSHIFT_HOMEDIR/app-root/runtime/srv/tor

if [ ! -d "$OPENSHIFT_HOMEDIR/app-root/runtime/srv/tor/bin" ]; then
	cd $OPENSHIFT_HOMEDIR/app-root/runtime/tmp
	rm -rf *

	# Download tor 32 bit ubunto
	wget https://www.torproject.org/dist/torbrowser/4.0.3/tor-browser-linux32-4.0.3_en-US.tar.xz
	# Download tor 64 bit ubunto
	wget https://www.torproject.org/dist/torbrowser/4.0.3/tor-browser-linux64-4.0.3_en-US.tar.xz
	tar -xJvf tor-browser-linux*.tar.xz
	rm tor-browser-linux*.tar.xz
	cd tor-browser_en-US
	./start-tor-browser
	ln -sf ~/tor-browser_en-US/start-tor-browser /usr/bin/tor
	cd tor-3.0.6/
	
	nohup sh -c "./configure --prefix=$OPENSHIFT_HOMEDIR/app-root/runtime/srv/tor"  > $OPENSHIFT_LOG_DIR/tor_install_conf.log /dev/null 2>&1 &  
	tail -f $OPENSHIFT_LOG_DIR/tor_install_conf.log
	nohup sh -c "make && make install && make clean"  > $OPENSHIFT_LOG_DIR/tor_install.log 2>&1 &  
	tail -f $OPENSHIFT_LOG_DIR/tor_install.log
	
	
	
	
	
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

#$OPENSHIFT_HOMEDIR/app-root/runtime/srv/tor/bin/tor -u http://ponisha.ir -d1 -r200 -c25
#$OPENSHIFT_HOMEDIR/app-root/runtime/srv/tor/bin/tor  --header='Host: ponisha.ir' --reps=1000 --time=300H --concurrent=10 --quiet --delay=1 http://ponisha.ir 
#$OPENSHIFT_HOMEDIR/app-root/runtime/srv/tor/bin/tor  --header='Host: ponisha.ir' --reps=1000 --time=300H --concurrent=1 --quiet --delay=0 http://bigfishs.tk/


###FROM https://usu.li/simulate-real-users-load-on-a-webserver-using-tor-and-sproxy/
#$OPENSHIFT_HOMEDIR/app-root/runtime/srv/tor/bin/tor -v -c 50 -i -t 3M -f uniq_urls.txt -d 10
echo "*****************************"


echo "*****************************"
echo "***  F I N I S H E D !!   ***"
echo "*****************************"
