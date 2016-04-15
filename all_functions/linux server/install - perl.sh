#!/bin/sh
# Change this to the last working Libs (may be you have to try and error)

mkdir $OPENSHIFT_HOMEDIR/app-root/runtime/tmp/
mkdir  $OPENSHIFT_HOMEDIR/app-root/runtime/srv/perl

if [ ! -d "$OPENSHIFT_HOMEDIR/app-root/runtime/srv/perl/bin" ]; then
	cd $OPENSHIFT_HOMEDIR/app-root/runtime/tmp
	rm -rf *

	# Download perl
	wget http://www.cpan.org/src/5.0/perl-5.20.1.tar.gz
    tar -xzf perl-5.20.1.tar.gz
    cd perl-5.20.1
    
	nohup sh -c "./Configure   -des --Dprefix=$OPENSHIFT_HOMEDIR/app-root/runtime/srv/perl"  > $OPENSHIFT_LOG_DIR/perl_install_conf.log /dev/null 2>&1 &  
	tail -f $OPENSHIFT_LOG_DIR/perl_install_conf.log
	nohup sh -c "make &&make test && make install && make clean"  > $OPENSHIFT_LOG_DIR/perl_install.log 2>&1 &  
	tail -f $OPENSHIFT_LOG_DIR/perl_install.log
	
	#GD2 perl module
	#sudo apt-get install libgd-graph-perl
	#Chart-2.x
	
	cd $OPENSHIFT_HOMEDIR/app-root/runtime/tmp
	wget http://www.cpan.org/authors/id/C/CH/CHARTGRP/Chart-2.4.6.tar.gz
	tar zxf  Chart-2.4.6.tar.gz && cd Chart-2.4.6 
	nohup sh -c "$OPENSHIFT_HOMEDIR/app-root/runtime/srv/perl/bin/perl Makefile.PL && make && make test  && sudo make install"  > $OPENSHIFT_LOG_DIR/perl_install2.log 2>&1 &  
	tail -f $OPENSHIFT_LOG_DIR/perl_install2.log
	
fi

### The url list will be written in ~/urls.txt, you can override this using he flag -o: for example:
#sproxy -o /home/user/benchmark/urls.txt
echo "*****************************"
echo "***  		  USAGE         ***"

#$OPENSHIFT_HOMEDIR/app-root/runtime/srv/perl/bin/perl -u http://ponisha.ir -d1 -r200 -c25
#$OPENSHIFT_HOMEDIR/app-root/runtime/srv/perl/bin/perl  --header='Host: ponisha.ir' --reps=1000 --time=300H --concurrent=10 --quiet --delay=1 http://ponisha.ir 
#$OPENSHIFT_HOMEDIR/app-root/runtime/srv/perl/bin/perl  --header='Host: ponisha.ir' --reps=1000 --time=300H --concurrent=1 --quiet --delay=0 http://bigfishs.tk/


###FROM https://usu.li/simulate-real-users-load-on-a-webserver-using-perl-and-sproxy/
#$OPENSHIFT_HOMEDIR/app-root/runtime/srv/perl/bin/perl -v -c 50 -i -t 3M -f uniq_urls.txt -d 10
echo "*****************************"


echo "*****************************"
echo "***  F I N I S H E D !!   ***"
echo "*****************************"
