#!/bin/sh
# Change this to the last working Libs (may be you have to try and error)

mkdir $OPENSHIFT_HOMEDIR/app-root/runtime/tmp/
mkdir  $OPENSHIFT_HOMEDIR/app-root/runtime/srv/libtorrent

if [ ! -d "$OPENSHIFT_HOMEDIR/app-root/runtime/srv/libtorrent/bin" ]; then
	cd $OPENSHIFT_HOMEDIR/app-root/runtime/tmp
	rm -rf *

	git clone https://github.com/mohanraj-r/torrentparse.git	
	cd torrentparse
	${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/python setup.py install
	cd torrentparse
	##USAGE
	${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/python torrentparse.py  ../tests/test_data/*.torrent
	#good for django
	${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/pip install django-torrent-stream
	
	# Download and install readline
	wget http://sourceforge.net/projects/libtorrent/files/latest/download?source=files # (or latest stable version)
	
	tar zxvf download?source=files
	rm download?source=files
	cd libtorrent*
	nohup sh -c "./configure --prefix=$OPENSHIFT_HOMEDIR/app-root/runtime/srv/libtorrent\
	--enable-python-binding"  > $OPENSHIFT_LOG_DIR/libtorrent_install_conf.log /dev/null 2>&1 &  
	tail -f $OPENSHIFT_LOG_DIR/libtorrent_install_conf.log
	nohup sh -c "${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/python setup.py install "  > $OPENSHIFT_LOG_DIR/libtorrent_install.log 2>&1 &  
	tail -f $OPENSHIFT_LOG_DIR/libtorrent_install.log
	
	cd ..
	# Download libtorrent
	wget http://ftp.yars.free.net/pub/source/libtorrent/libtorrent-3.7.15.tar.gz # (or latest stable version)
	wget http://home.comcast.net/~andrex2/cygwin/libtorrent/libtorrent-3.7.15-1-src.tar.bz2
	tar xf libtorrent-3.7.15-1-src.tar.bz2
	tar zxvf libtorrent-3.7.15.tar.gz
	# Here comes the magic
	CXXFLAGS="-O0 -Wall -fno-exceptions -fno-rtti -fno-implement-inlines" \
	LDFLAGS="-Xlinker -search_paths_first -L/usr/local/lib" \
	CPPFLAGS="-I/usr/local/include" \
	nohup sh -c "./configure --with-openssl --disable-shared --disable-nls --prefix=$OPENSHIFT_HOMEDIR/app-root/runtime/srv/libtorrent"  > $OPENSHIFT_LOG_DIR/libtorrent_install_conf.log /dev/null 2>&1 &  
	tail -f $OPENSHIFT_LOG_DIR/libtorrent_install_conf.log
	nohup sh -c "make && make install && make clean"  > $OPENSHIFT_LOG_DIR/libtorrent_install.log 2>&1 &  
	tail -f $OPENSHIFT_LOG_DIR/libtorrent_install.log
	export PATH=${PATH}:$OPENSHIFT_HOMEDIR/app-root/runtime/srv/libtorrent/bin/  
	
	
fi
echo "*****************************"
echo "***  		  USAGE         ***"

libtorrent -u $1,$2 $3 <<EOF

mkdir $4
lcd $5 
cd $6 
mirror --reverse  
EOF 

cat <<'EOF'  >> libtorrent_sync.py
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
