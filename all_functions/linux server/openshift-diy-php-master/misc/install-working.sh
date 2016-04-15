#!/bin/sh

	PYTHON_VERSION="2.7.4"
	VIRTUALENV_VERSION="1.9.1"
	PCRE_VERSION="8.32"
	NGINX_VERSION="1.2.2"
	MEMCACHED_VERSION="1.4.15"
	HTTPD_VERSION="2.4.18"
	APR_VERSION="1.5.1"
	ZLIB_VERSION="1.2.8"
	PHP_VERSION="5.5.9"
	XDEBUG_VERSION="2.2.3"
	APC_VERSION="3.1.13"


	OPENSHIFT_RUNTIME_DIR=$OPENSHIFT_HOMEDIR/app-root/runtime
	OPENSHIFT_REPO_DIR=$OPENSHIFT_HOMEDIR/app-root/runtime/repo
	Current_DIR="$PWD"
echo $Current_DIR

echo "Prepare directories"
cd $OPENSHIFT_RUNTIME_DIR
mkdir srv
mkdir srv/pcre
mkdir srv/httpd
mkdir srv/php
mkdir tmp
rm -rf $OPENSHIFT_RUNTIME_DIR/tmp/*

cd $OPENSHIFT_RUNTIME_DIR/tmp/

echo "Install pcre"
#if [ ! -d "$OPENSHIFT_RUNTIME_DIR/srv/pcre/bin" ]; then
	cd $OPENSHIFT_RUNTIME_DIR/tmp/
	wget ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/pcre-${PCRE_VERSION}.tar.gz
	wget http://ftp.cs.stanford.edu/pub/exim/pcre/pcre-${PCRE_VERSION}.tar.gz	
	tar -zxf pcre-${PCRE_VERSION}.tar.gz
	cd pcre-${PCRE_VERSION}
	./configure \
	--prefix=$OPENSHIFT_RUNTIME_DIR/srv/pcre
	make && make install
	cd ..
#fi
echo "Install Apache httpd"
#if [ ! -d "$OPENSHIFT_RUNTIME_DIR/srv/httpd/bin" ]; then
	cd $OPENSHIFT_RUNTIME_DIR/tmp/
	#wget http://www.dsgnwrld.com/am//httpd/httpd-${HTTPD_VERSION}.tar.gz
	wget https://www.apache.org/dist/httpd/httpd-${HTTPD_VERSION}.tar.gz
	tar -zxf httpd-${HTTPD_VERSION}.tar.gz
	#wget http://apache.petsads.us//apr/apr-${APR_VERSION}.tar.gz
	wget https://archive.apache.org/dist/apr/apr-${APR_VERSION}.tar.gz
	tar -zxf apr-${APR_VERSION}.tar.gz
	mv apr-${APR_VERSION} httpd-${HTTPD_VERSION}/srclib/apr
	#wget http://artfiles.org/apache.org/apr/apr-util-1.5.3.tar.gz
	wget https://archive.apache.org/dist/apr/apr-util-${APR_VERSION}.tar.gz
	tar -zxf apr-util-${APR_VERSION}.tar.gz
	mv apr-util-${APR_VERSION} httpd-${HTTPD_VERSION}/srclib/apr-util
	cd $OPENSHIFT_RUNTIME_DIR/tmp/httpd-${HTTPD_VERSION}
	./configure \
	--prefix=$OPENSHIFT_RUNTIME_DIR/srv/httpd \
	--with-included-apr \
	--with-pcre=$OPENSHIFT_RUNTIME_DIR/srv/pcre \
	--enable-so \
	--enable-auth-digest \
	--enable-rewrite \
	--enable-setenvif \
	--enable-mime \
	--enable-deflate \
	--enable-headers
	make && make install
	#nohup sh -c "make && make install"  > $OPENSHIFT_DIY_LOG_DIR/Apach_install.log 2>&1 &
	#bash -i -c 'tail -f  $OPENSHIFT_DIY_LOG_DIR/Apach_install.log '
	cd ..
#fi
#echo "INSTALL ICU"
#wget http://download.icu-project.org/files/icu4c/50.1/icu4c-50_1-src.tgz
#tar -zxf icu4c-50_1-src.tgz
#cd icu/source/
#chmod +x runConfigureICU configure install-sh
#./configure \
#--prefix=$OPENSHIFT_RUNTIME_DIR/srv/icu/
#make && make install
#cd ../..

echo "Install zlib"
#if [ ! -d "$OPENSHIFT_RUNTIME_DIR/srv/zlib" ]; then
	cd $OPENSHIFT_RUNTIME_DIR/tmp/
	wget http://zlib.net/zlib-${ZLIB_VERSION}.tar.gz
	tar -zxf zlib-${ZLIB_VERSION}.tar.gz
	cd zlib-${ZLIB_VERSION}
	./configure \
	--prefix=$OPENSHIFT_RUNTIME_DIR/srv/zlib/
	make && make install
	cd ..
#fi

echo "INSTALL PHP"
#if [ ! -d "$OPENSHIFT_RUNTIME_DIR/srv/php/etc/apache2" ]; then
	cd $OPENSHIFT_RUNTIME_DIR/tmp/
	wget http://ca1.php.net/get/php-${PHP_VERSION}.tar.gz/from/this/mirror -O php-${PHP_VERSION}.tar.gz
	tar -zxf php-${PHP_VERSION}.tar.gz
	rm -rf php-${PHP_VERSION}.tar.gz
	#tar -zxf php-${PHP_VERSION}.tar.gz
	cd $OPENSHIFT_RUNTIME_DIR/tmp/php-${PHP_VERSION}
	./configure \
	--prefix=$OPENSHIFT_RUNTIME_DIR/srv/php \
	--with-xmlrpc \
	--with-config-file-path=$OPENSHIFT_RUNTIME_DIR/srv/php/etc/apache2 \
	--with-apxs2=$OPENSHIFT_RUNTIME_DIR/srv/httpd/bin/apxs \
	--with-zlib=$OPENSHIFT_RUNTIME_DIR/srv/zlib \
	--with-libdir=lib64 \
    --with-mysql-sock=$HOME/mysql/socket/mysql.sock \
	--with-pdo-mysql \
	--with-layout=PHP \
	--with-gd \
	--with-curl \
	--with-mysqli \
	--with-pdo-pgsql \
	--with-openssl \
	--enable-mbstring \
	--enable-soap \
	--enable-zip \
	--enable-intl 
	#--with-icu-dir=$OPENSHIFT_RUNTIME_DIR/srv/icu \
	
	make && make install
	#nohup sh -c "make && make install"  > $OPENSHIFT_DIY_LOG_DIR/php_make_install.log 2>&1 &
	#tail -f $OPENSHIFT_DIY_LOG_DIR/php_make_install.log
	#bash -i -c 'tail -f  $OPENSHIFT_DIY_LOG_DIR/php_make_install.log'
	mkdir $OPENSHIFT_RUNTIME_DIR/srv/php/etc/apache2
	cd ..
#fi

#echo "Install APC"
#wget http://pecl.php.net/get/APC-${APC_VERSION}.tgz
#tar -zxf APC-${APC_VERSION}.tgz
#cd APC-${APC_VERSION}
#$OPENSHIFT_RUNTIME_DIR/srv/php/bin/phpize
#./configure \
#--with-php-config=$OPENSHIFT_RUNTIME_DIR/srv/php/bin/php-config \
#--enable-apc \
#--enable-apc-debug=no
#make && make install
#cd ..

echo "Install xdebug"
#if [ ! -d "$OPENSHIFT_RUNTIME_DIR/srv/php/bin/php-config" ]; then
cd $OPENSHIFT_RUNTIME_DIR/tmp/
wget http://xdebug.org/files/xdebug-${XDEBUG_VERSION}.tgz
tar -zxf xdebug-${XDEBUG_VERSION}.tgz
cd xdebug-${XDEBUG_VERSION}
$OPENSHIFT_RUNTIME_DIR/srv/php/bin/phpize
./configure \
--with-php-config=$OPENSHIFT_RUNTIME_DIR/srv/php/bin/php-config
make && cp modules/xdebug.so $OPENSHIFT_RUNTIME_DIR/srv/php/lib/php/extensions
cd ..
#fi

# cleanup
echo "Cleanup"
rm -r $OPENSHIFT_RUNTIME_DIR/tmp/*.tar.gz
rm -r $OPENSHIFT_RUNTIME_DIR/tmp/*.tgz
rm -r $OPENSHIFT_RUNTIME_DIR/tmp/*
rm -rf $OPENSHIFT_TMP_DIR/*

echo "COPY TEMPLATES"
cd $Current_DIR
cd ..
DIR="$PWD"


echo "COPY TEMPLATES"
cp $OPENSHIFT_REPO_DIR/misc/templates/bash_profile.tpl $OPENSHIFT_HOMEDIR/app-root/data/.bash_profile
python $OPENSHIFT_REPO_DIR/misc/parse_templates.py

#nohup python ${DIR}/misc/parse_templates.py    > $OPENSHIFT_DIY_LOG_DIR/parse_templates.log 2>&1 &

#python ${DIR}/misc/parse_templates.py

#cp ${DIR}/misc/templates/bash_profile.tpl $OPENSHIFT_HOMEDIR/app-root/data/.bash_profile
#python $OPENSHIFT_REPO_DIR/misc/parse_templates.py
cp ${DIR}/misc/templates/php.ini.tpl $OPENSHIFT_RUNTIME_DIR/srv/php/etc/apache2/php.ini


#cat << EOF >>$OPENSHIFT_RUNTIME_DIR/srv/php/etc/apache2/php.ini

#EOF

echo "START APACHE"
kill -9 `lsof -t -i :8080`
nohup sh -c "$HOME/app-root/runtime/srv/httpd/bin/apachectl start" > $OPENSHIFT_DIY_LOG_DIR/apach_server.log 2>&1 &

#nohup sh -c "./install.sh"  > $OPENSHIFT_DIY_LOG_DIR/Apach_install.log 2>&1 &
#tail -f  $OPENSHIFT_DIY_LOG_DIR/Apach_install.log
echo "*****************************"
echo "***  F I N I S H E D !!   ***"
echo "*****************************"
