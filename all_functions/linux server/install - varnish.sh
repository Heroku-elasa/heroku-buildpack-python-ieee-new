#!/bin/sh
# Change this to the last working Libs (may be you have to try and error)

mkdir $OPENSHIFT_HOMEDIR/app-root/runtime/tmp/
mkdir  $OPENSHIFT_HOMEDIR/app-root/runtime/srv/varnish
mkdir $OPENSHIFT_HOMEDIR/app-root/runtime/srv/pcre

if [ ! -d "$OPENSHIFT_HOMEDIR/app-root/runtime/srv/varnish/bin" ]; then
	cd $OPENSHIFT_HOMEDIR/app-root/runtime/tmp
	rm -rf *
	
	PCRE_VERSION="8.35"
	wget http://ftp.cs.stanford.edu/pub/exim/pcre/pcre-${PCRE_VERSION}.tar.gz
	tar zxf pcre-${PCRE_VERSION}.tar.gz
	rm pcre-${PCRE_VERSION}.tar.gz
	cd pcr*
	./configure --prefix=${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/pcre
	make && make test && make install && make clean
	
	
	# Download varnish
	
	cd $OPENSHIFT_HOMEDIR/app-root/runtime/tmp
	rm -rf *
	#wget https://repo.varnish-cache.org/source/varnish-4.1.2.tar.gz
	#wget https://repo.varnish-cache.org/source/varnish-3.0.7.tar.gz
	
	wget https://repo.varnish-cache.org/source/varnish-2.1.5.tar.gz
	
	tar -zxvf varnish-*.*.*.tar.gz
	rm varnish-*.*.*.tar.gz
	cd varnish-*.*.*	
	export PKG_CONFIG_PATH=${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/pcre/lib/pkgconfig:$PKG_CONFIG_PATH
	./configure --prefix=${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/varnish  --with-rst2man=${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/rst2man.py  --with-pcre-config=${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/pcre/bin/pcre-config
	make &&   make install && make clean
	
	cd ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/varnish/sbin
	rm my.vcl
cat << "EOF" >> my.vcl
backend nginx01 {
	.host = "diy-tornado4ss.rhcloud.com";
	.port = "8080";
}
# define our second nginx server
backend nginx02 {
	.host = "diy-phantomjs4so.rhcloud.com";
	.port = "8080";
}
# configure the load balancer
director backend_director round-robin {
	{ .backend = nginx01; }
	{ .backend = nginx02; }
}
sub vcl_recv {
	set req.backend = backend_director;
	
	# loads more stuff
}
EOF
	kill -9 `lsof -t -i :8080`
	kill `ps -ef | grep varnishd | grep -v grep | awk '{ print $2 }'` > /dev/null 2>&1

	#cd ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/varnish/sbin/ && ./varnishd -a $OPENSHIFT_DIY_IP:8080 -T  $OPENSHIFT_DIY_IP:15001 -b $OPENSHIFT_DIY_IP:15001 
	cd ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/varnish/sbin/ && ./varnishd -a $OPENSHIFT_DIY_IP:8080  -f ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/varnish/sbin/my.vcl
	#nohup sh -c "make && make test && make install && make clean"  > $OPENSHIFT_LOG_DIR/varnish_install.log 2>&1 &  
	#tail -f $OPENSHIFT_LOG_DIR/varnish_install.log
	
	
	
	
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
