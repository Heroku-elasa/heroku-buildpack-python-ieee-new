#!/bin/sh
# Change this to the last working Libs (may be you have to try and error)

mkdir $OPENSHIFT_HOMEDIR/app-root/runtime/tmp/
mkdir  $OPENSHIFT_HOMEDIR/app-root/runtime/srv/lftp

if [ ! -d "$OPENSHIFT_HOMEDIR/app-root/runtime/srv/lftp/bin" ]; then
	cd $OPENSHIFT_HOMEDIR/app-root/runtime/tmp
	rm -rf *

	# Download and install readline
	wget http://mirror.anl.gov/pub/gnu/readline/readline-6.0.tar.gz # (or latest stable version)
	
	tar zxvf readline-6.0.tar.gz
	cd readline-6.0
	nohup sh -c "./configure --prefix=$OPENSHIFT_HOMEDIR/app-root/runtime/srv/lftp"  > $OPENSHIFT_LOG_DIR/php_install_conf.log /dev/null 2>&1 &  
	tail -f $OPENSHIFT_LOG_DIR/php_install_conf.log
	nohup sh -c "make && make install && make clean"  > $OPENSHIFT_LOG_DIR/php_install.log 2>&1 &  
	tail -f $OPENSHIFT_LOG_DIR/php_install.log
	
	cd ..
	# Download lftp
	wget http://ftp.yars.free.net/pub/source/lftp/lftp-3.7.15.tar.gz # (or latest stable version)
	wget http://home.comcast.net/~andrex2/cygwin/lftp/lftp-3.7.15-1-src.tar.bz2
	tar xf lftp-3.7.15-1-src.tar.bz2
	tar zxvf lftp-3.7.15.tar.gz
	# Here comes the magic
	CXXFLAGS="-O0 -Wall -fno-exceptions -fno-rtti -fno-implement-inlines" \
	LDFLAGS="-Xlinker -search_paths_first -L/usr/local/lib" \
	CPPFLAGS="-I/usr/local/include" \
	nohup sh -c "./configure --with-openssl --disable-shared --disable-nls --prefix=$OPENSHIFT_HOMEDIR/app-root/runtime/srv/lftp"  > $OPENSHIFT_LOG_DIR/php_install_conf.log /dev/null 2>&1 &  
	tail -f $OPENSHIFT_LOG_DIR/php_install_conf.log
	nohup sh -c "make && make install && make clean"  > $OPENSHIFT_LOG_DIR/php_install.log 2>&1 &  
	tail -f $OPENSHIFT_LOG_DIR/php_install.log
	export PATH=${PATH}:$OPENSHIFT_HOMEDIR/app-root/runtime/srv/lftp/bin/  
	
	
fi
echo "*****************************"
echo "***  		  USAGE         ***"

lftp -u $1,$2 $3 <<EOF

mkdir $4
lcd $5 
cd $6 
mirror --reverse  
EOF 

cat <<'EOF'  >> lftp_sync.py
#! /usr/bin/python
import subprocess

subprocess.call(["bash", ftp_script, username, password, ftp, folder_to_move, src,folder_name_in_destination])
EOF



echo "*****************************"
#nohup sh -c " wget --mirror --user=u220290147 --password=ss123456 ftp://93.188.160.83:21/"  > $OPENSHIFT_LOG_DIR/wget_ftp.log 2>&1 &  
#tail -f $OPENSHIFT_LOG_DIR/wget_ftp.log

echo "*****************************"
echo "***  F I N I S H E D !!   ***"
echo "*****************************"
