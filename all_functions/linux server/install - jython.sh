#!/bin/sh
# Change this to the last working Libs (may be you have to try and error)
mkdir  $OPENSHIFT_HOMEDIR/app-root/runtime/srv
mkdir $OPENSHIFT_HOMEDIR/app-root/runtime/tmp/
mkdir  $OPENSHIFT_HOMEDIR/app-root/runtime/srv/jython
#mkdir $OPENSHIFT_HOMEDIR/app-root/runtime/srv/jython/cash
mkdir  $OPENSHIFT_HOMEDIR/app-root/runtime/srv/java

if [ ! -d ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/java/bin ]; then
	cd $OPENSHIFT_HOMEDIR/app-root/runtime/srv/java
	wget --no-check-certificate --no-cookies --header "Cookie: oraclelicense=accept-securebackup-cookie" http://download.oracle.com/otn-pub/java/jdk/7u55-b13/jdk-7u55-linux-x64.tar.gz
	tar -zxf jdk-7u55-linux-x64.tar.gz
	rm jdk-7u55-linux-x64.tar.gz
	mv jdk1.7.0_55/* .
	rm -rf jdk1.7.0_55
	#update-alternatives --install /usr/bin/java java $OPENSHIFT_HOMEDIR/app-root/runtime/srv/java/bin/java 100  
	#update-alternatives --config java
	#wget http://www.java.net/download/jdk7u40/archive/b40/binaries/jdk-7u40-fcs-bin-b40-linux-x64-16_aug_2013.tar.gz
	export PATH=${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/java/bin:$PATH
	export JAVA_HOME="${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/java"
	export JRE_HOME="${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/java/jre"
fi

if [ ! -d ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/jython/bin ]; then
	cd $OPENSHIFT_HOMEDIR/app-root/runtime/tmp
	#rm -rf *
	
	# Download siege
	mkdir  $OPENSHIFT_HOMEDIR/app-root/runtime/srv/htmlunit
	wget http://downloads.sourceforge.net/project/htmlunit/htmlunit/2.22/htmlunit-2.22-bin.zip
	unzip htmlunit-2.22-bin.zip
	rm htmlunit-2.22-bin.zip
	mv htmlunit-2.22/* $OPENSHIFT_HOMEDIR/app-root/runtime/srv/htmlunit
	export CLASSPATH=$CLASSPATH:$OPENSHIFT_HOMEDIR/app-root/runtime/srv/htmlunit/lib/*
	#export CLASSPATH=$OPENSHIFT_HOMEDIR/app-root/runtime/srv/htmlunit/lib/*:$CLASSPATH
	
	# Download siege
	cd $OPENSHIFT_TMP_DIR
	rm -rf $OPENSHIFT_TMP_DIR/*
	wget --no-clobber --trust-server-names -c "http://search.maven.org/remotecontent?filepath=org/python/jython-installer/2.7.0/jython-installer-2.7.0.jar"
 
	#wget http://search.maven.org/remotecontent?filepath=org/python/jython-standalone/2.7.0/jython-standalone-2.7.0.jar
	
	#wget http://downloads.sourceforge.net/jython/jython_installer-2.5.2.jar
	#mv *  jython_installer.jar
    export DISPLAY=:0.0
	#cd $OPENSHIFT_HOMEDIR/app-root/runtime/srv/java/bin/
	$OPENSHIFT_HOMEDIR/app-root/runtime/srv/java/bin/java -jar jython-installer-2.7.0.jar -s -d "$OPENSHIFT_HOMEDIR/app-root/runtime/srv/jython"
	#$OPENSHIFT_HOMEDIR/app-root/runtime/srv/java/bin/java -jar $OPENSHIFT_TMP_DIR/jython_installer-2.5.2.jar # -d $OPENSHIFT_HOMEDIR/app-root/runtime/srv/jython # -Dpython.cachedir=/tmp -A
	ls $OPENSHIFT_HOMEDIR/app-root/runtime/srv/jython
	
	$OPENSHIFT_HOMEDIR/app-root/runtime/srv/jython/bin/jython --print
	export PATH=${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin:${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/lib/python2.7:$PATH
	$OPENSHIFT_HOMEDIR/app-root/runtime/srv/jython/bin/jython -Dpython.home="${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python" -Dpython.executable="${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/python" -S
	
	$OPENSHIFT_HOMEDIR/app-root/runtime/srv/jython/bin/jython  -Dpython.executable="${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/python"
		
		$OPENSHIFT_HOMEDIR/app-root/runtime/srv/jython/bin/jython    $OPENSHIFT_HOMEDIR/app-root/runtime/tmp/gartner.py # -Dpython.cachedir=/tmp -Dpython.path=${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/*  #  -z noexecstack
		$OPENSHIFT_HOMEDIR/app-root/runtime/srv/jython/bin/jython    $OPENSHIFT_HOMEDIR/app-root/runtime/repo/nginx-php-fp-in-openshift-tornado-added/misc/gartner.py  # -J-classpath "${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/htmlunit/lib/*"
		
		#$OPENSHIFT_HOMEDIR/app-root/runtime/srv/java/bin/java -jar $OPENSHIFT_HOMEDIR/app-root/runtime/srv/jython/jython.jar   -J-classpath "${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/htmlunit/lib/*"  $OPENSHIFT_HOMEDIR/app-root/runtime/repo/nginx-php-fp-in-openshift-tornado-added/misc/gartner.py  
	cd $OPENSHIFT_TMP_DIR
	wget http://entrian.com/goto/goto-1.0.zip
	unzip goto-1.0.zip
	cd goto-1.0
	${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/jython/bin/jython setup.py install
	rm -rf *
	
	git clone https://github.com/jythontools/wheel.git
	cd wheel
	${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/jython/bin/jython setup.py install
	rm -rf *
	
	
	
	
	
	git clone https://github.com/jythontools/pip.git
	cd pip 
	${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/jython/bin/jython setup.py install
	rm -rf *
	
	git clone https://github.com/jythontools/setuptools.git
	cd setuptools
	${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/jython/bin/jython setup.py install
	rm -rf *
	
	 git clone https://github.com/cython/backports_abc.git
	 cd backports_abc
	 ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/jython/bin/jython setup.py install
	rm -rf *
	
	git clone https://github.com/certifi/python-certifi.git 
	cd python-certifi
	${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/jython/bin/jython setup.py install
	rm -rf *
	
	git clone https://github.com/bdoms/beautifulsoup.git
	cd beautifulsoup
	${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/jython/bin/jython setup.py install
	rm -rf *
	
	git clone https://github.com/cython/cython.git
	cd cython
	${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/jython/bin/jython setup.py install
	rm -rf *
	
	git clone https://github.com/ctb/twill.git
	cd twill
	${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/jython/bin/jython setup.py install
	rm -rf *
	
	
	git clone https://github.com/lxml/lxml.git
	cd lxml
	${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/jython/bin/jython setup.py install
	rm -rf *
	
	wget https://communities.cisco.com/servlet/JiveServlet/download/150596-65641/fcntl.py.zip
	unzip fcntl.py.zip
	${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/jython/bin/jython fcntl.py install
	rm -rf *
	git clone https://github.com/tornadoweb/tornado.git 
	cd tornado 
	${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/jython/bin/jython setup.py install
	rm -rf *
	
	#$OPENSHIFT_HOMEDIR/app-root/runtime/srv/jython/bin/jython --print
	
	#$OPENSHIFT_HOMEDIR/app-root/runtime/srv/jython/bin/easy_install pip
	git clone https://github.com/kelp404/six.git
	cd six 
	${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/jython/bin/jython setup.py install
	rm -rf *
	
	git clone https://github.com/ambv/singledispatch.git
	cd singledispatch
	${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/jython/bin/jython setup.py install
	rm -rf *
	
	kill -9 `lsof -t -i :8080`
	${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/jython/bin/jython ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/tornado3/tornado-get.py  --port '8080' --root '${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/tornado3/' --wtdir '/static'
	
	:'
	cd $OPENSHIFT_HOMEDIR/app-root/runtime/tmp
	wget http://peak.telecommunity.com/dist/ez_setup.py
	$OPENSHIFT_HOMEDIR/app-root/runtime/srv/jython/bin/jython ez_setup.py
	
	cd $OPENSHIFT_HOMEDIR/app-root/runtime/tmp
	wget https://pypi.python.org/packages/source/s/setuptools/setuptools-2.2.tar.gz
	tar -xzf setuptools-2.2.tar.gz
	cd setuptools-2.2
	$OPENSHIFT_HOMEDIR/app-root/runtime/srv/jython/bin/jython setup.py install --prefix=${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/jython
	
	cd $OPENSHIFT_TMP_DIR
	curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
	$OPENSHIFT_HOMEDIR/app-root/runtime/srv/jython/bin/jython get-pip.py
	'
fi


cd $OPENSHIFT_HOMEDIR/app-root/runtime/tmp
#rm -rf *
### The url list will be written in ~/urls.txt, you can override this using he flag -o: for example:
#$OPENSHIFT_HOMEDIR/app-root/runtime/srv/sproxy -o /home/user/benchmark/urls.txt
echo "*****************************"
echo "***  		  USAGE         ***"

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
