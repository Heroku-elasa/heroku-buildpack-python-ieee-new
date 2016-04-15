#!/bin/sh
# Change this to the last working Libs (may be you have to try and error)

if [ ! -z $OPENSHIFT_DIY_LOG_DIR ]; then
	echo "$OPENSHIFT_LOG_DIR" > "$OPENSHIFT_HOMEDIR/.env/OPENSHIFT_DIY_LOG_DIR"
	
	nohup	OPENSHIFT_DIY_LOG_DIR2=${OPENSHIFT_LOG_DIR}   > /dev/null 2>&1
	echo $OPENSHIFT_DIY_LOG_DIR2
fi
# ========================================================
# Step 1. Download the archives.
# 1. firefox 15.0.1
# 2. java jre-7u7
# 3. flash 11.2
# ========================================================

mkdir $OPENSHIFT_HOMEDIR/app-root/runtime/srv
mkdir $OPENSHIFT_HOMEDIR/app-root/runtime/srv/PyQt4

mkdir $OPENSHIFT_HOMEDIR/app-root/runtime/tmp/
if [ ! -d "$OPENSHIFT_HOMEDIR/app-root/runtime/srv/phantomjs/bin" ]; then
	cd $OPENSHIFT_HOMEDIR/app-root/runtime/tmp/
	rm -rf *
	
	#wget http://phantomjs.googlecode.com/files/phantomjs-1.9.2-linux-i686.tar.bz2
	#bunzip2 phantomjs-1.9.2-linux-i686.tar.bz2
	#wget http://selenium-release.storage.googleapis.com/2.44/selenium-server-standalone-2.44.0.jar
	#java -jar selenium-server-standalone-2.*.*.jar -role hub
	wget http://sourceforge.net/projects/pyqt/files/sip/sip-4.16.5/sip-4.16.5.tar.gz
	tar -zxf sip-4.16.5.tar.gz
	rm -rf sip-4.16.5.tar.gz
	cd sip-4.16.5
	$OPENSHIFT_HOMEDIR/app-root/runtime/srv/python/bin/python configure.py
	nohup sh -c "make && make install "  > $OPENSHIFT_LOG_DIR/sip_install.log /dev/null 2>&1 &  
	tail -f $OPENSHIFT_LOG_DIR/sip_install.log
	
	wget http://sourceforge.net/projects/pyqt/files/PyQt4/PyQt-4.11.3/PyQt-x11-gpl-4.11.3.tar.gz	
	tar -zxf PyQt-x11-gpl-4.11.3.tar.gz
	rm -rf PyQt-x11-gpl-4.11.3.tar.gz
	cd PyQt-x11-gpl-4.11.3
	$OPENSHIFT_HOMEDIR/app-root/runtime/srv/python/bin/python configure-ng.py
	nohup sh -c "./configure\
	   --prefix=${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/nginx\
    --with-ipv6	    " > $OPENSHIFT_LOG_DIR/PyQt_config.log /dev/null 2>&1 & 
	tail -f $OPENSHIFT_DIY_LOG_DIR/PyQt_config.log
	
	nohup sh -c "make && make install && make clean"  > $OPENSHIFT_LOG_DIR/PyQt_install.log /dev/null 2>&1 &  
	tail -f $OPENSHIFT_LOG_DIR/PyQt_install.log
	#./configure --with-pcre=$OPENSHIFT_TMP_DIR/pcre-8.35 --prefix=$OPENSHIFT_DATA_DIR/nginx --with-http_realip_module
	#
	export PATH=${PATH}:$OPENSHIFT_HOMEDIR/app-root/runtime/srv/phantomjs/bin/  
	cd $OPENSHIFT_HOMEDIR/app-root/runtime/srv/
	rm -rf casperjs
	git clone git://github.com/n1k0/casperjs.git
	export PATH=${PATH}:$OPENSHIFT_HOMEDIR/app-root/runtime/srv/casperjs/bin/  
	export PATH=${PATH}:$OPENSHIFT_HOMEDIR/app-root/runtime/srv/python/bin/
	#cd $OPENSHIFT_REPO_DIR   
	#  and then run your sample code in a node "session". 
	# ========================================================
	# Step 3. Create a run script.
	# ========================================================
	

fi

echo "*****************************"
echo "***  		  USAGE         ***"
echo "{firefox_dir}/rtf/run.sh http://www.adobe.com/software/flash/about/ http://javatester.org/"
#${firefox_dir}/rtf/run.sh http://www.adobe.com/software/flash/about/ http://javatester.org/
echo "*****************************"


echo "*****************************"
echo "***  F I N I S H E D !!   ***"
echo "*****************************"
