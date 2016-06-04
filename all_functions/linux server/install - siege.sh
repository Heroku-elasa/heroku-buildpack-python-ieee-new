#!/bin/sh
# Change this to the last working Libs (may be you have to try and error)
mkdir  $OPENSHIFT_HOMEDIR/app-root/runtime/srv
mkdir $OPENSHIFT_HOMEDIR/app-root/runtime/tmp/
mkdir  $OPENSHIFT_HOMEDIR/app-root/runtime/srv/siege

if [ ! -d ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/siege/bin ]; then
	cd $OPENSHIFT_HOMEDIR/app-root/runtime/tmp
	rm -rf *

	# Download siege
	wget http://download.joedog.org/siege/siege-3.0.6.tar.gz
    tar -xvpzf siege-3.0.6.tar.gz
    cd siege-3.0.6/
	
	nohup sh -c "./configure --prefix=$OPENSHIFT_HOMEDIR/app-root/runtime/srv/siege"  > $OPENSHIFT_LOG_DIR/siege_install_conf.log /dev/null 2>&1 &  
	bash -i -c 'tail -f $OPENSHIFT_LOG_DIR/siege_install_conf.log'
	nohup sh -c "make && make install && make clean"  > $OPENSHIFT_LOG_DIR/siege_install.log 2>&1 &  
	bash -i -c 'tail -f $OPENSHIFT_LOG_DIR/siege_install.log'
	

fi

mkdir  $OPENSHIFT_HOMEDIR/app-root/runtime/srv/sproxy

if [ ! -d ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/sproxy/bin ]; then
	cd $OPENSHIFT_HOMEDIR/app-root/runtime/tmp
	rm -rf *


	wget http://download.joedog.org/sproxy/sproxy-latest.tar.gz
	tar xzvf  sproxy-latest.tar.gz
	cd sproxy*
	nohup sh -c "./configure --prefix=$OPENSHIFT_HOMEDIR/app-root/runtime/srv/sproxy"  > $OPENSHIFT_LOG_DIR/sproxy_install_conf.log /dev/null 2>&1 &  
	bash -i -c 'tail -f $OPENSHIFT_LOG_DIR/sproxy_install_conf.log'
	nohup sh -c "make && make install && make clean"  > $OPENSHIFT_LOG_DIR/sproxy_install.log 2>&1 &  
	bash -i -c 'tail -f $OPENSHIFT_LOG_DIR/sproxy_install.log'
	
fi
cd $OPENSHIFT_HOMEDIR/app-root/runtime/tmp
rm -rf *
### The url list will be written in ~/urls.txt, you can override this using he flag -o: for example:
#$OPENSHIFT_HOMEDIR/app-root/runtime/srv/sproxy -o /home/user/benchmark/urls.txt
echo "*****************************"
echo "***  		  USAGE         ***"

#$OPENSHIFT_HOMEDIR/app-root/runtime/srv/siege/bin/siege -u http://5040.ir -d1 -r200 -c25
#$OPENSHIFT_HOMEDIR/app-root/runtime/srv/siege/bin/siege -u http://ponisha.ir
#$OPENSHIFT_HOMEDIR/app-root/runtime/srv/siege/bin/siege -u http://elasa.ir
#$OPENSHIFT_HOMEDIR/app-root/runtime/srv/siege/bin/siege -u http://elasa2ir.tk
#$OPENSHIFT_HOMEDIR/app-root/runtime/srv/siege/bin/siege -u http://elasa2ir.tk -d1 -r200 -c25

#$OPENSHIFT_HOMEDIR/app-root/runtime/srv/siege/bin/siege -u http://arianeng.ir 
#$OPENSHIFT_HOMEDIR/app-root/runtime/srv/siege/bin/siege -u http://free-papers.elasa.ir/index/url=%22http://dl.acm.org/citation.cfm?id=99977.100000&coll=DL&dl=ACM%22 -d1 -r200 -c25
#$OPENSHIFT_HOMEDIR/app-root/runtime/srv/siege/bin/siege -u http://diy2-elasa2.rhcloud.com/index/url="http://dl.acm.org/citation.cfm?id=99977.100000&coll=DL&dl=ACM" -d1 -r225 -c25

#$OPENSHIFT_HOMEDIR/app-root/runtime/srv/siege/bin/siege -u http://arianeng.ir -d1 -r20000 -c20
#$OPENSHIFT_HOMEDIR/app-root/runtime/srv/siege/bin/siege -u http://shop.arianeng.ir -d1 -r200 -c15 --time=300H
#$OPENSHIFT_HOMEDIR/app-root/runtime/srv/siege/bin/siege  --header='Host: shop.arianeng.ir' --reps=1000 --time=300H --concurrent=10 --quiet --delay=1 http://shop.arianeng.ir
#$OPENSHIFT_HOMEDIR/app-root/runtime/srv/siege/bin/siege  --header='Host: arianeng.ir' --reps=500 --time=300H --concurrent=10 --quiet --delay=1 http://arianeng.ir

#$OPENSHIFT_HOMEDIR/app-root/runtime/srv/siege/bin/siege  --header='Host: ponisha.ir' --reps=1000 --time=300H --concurrent=10 --quiet --delay=1 http://ponisha.ir 
#$OPENSHIFT_HOMEDIR/app-root/runtime/srv/siege/bin/siege  --header='Host: free-papers.elasa.ir' --reps=1000 --time=300H --concurrent=1 --quiet --delay=0 http://free-papers.elasa.ir/

 ps ax | grep siege
###FROM https://usu.li/simulate-real-users-load-on-a-webserver-using-siege-and-sproxy/
#$OPENSHIFT_HOMEDIR/app-root/runtime/srv/siege/bin/siege -v -c 50 -i -t 3M -f uniq_urls.txt -d 10
echo "*****************************"

while [ true ]; do
 sleep 30
 # do what you need to here
 #$OPENSHIFT_HOMEDIR/app-root/runtime/srv/siege/bin/siege -u http://arianeng.ir -d1 -r200 -c25
 nohup sh -c "$OPENSHIFT_HOMEDIR/app-root/runtime/srv/siege/bin/siege -u http://arianeng.ir -d1 -r200 -c25"  > $OPENSHIFT_LOG_DIR/sproxy_install_conf.log /dev/null 2>&1 &  
done

echo "*****************************"
echo "***  F I N I S H E D !!   ***"
echo "*****************************"
