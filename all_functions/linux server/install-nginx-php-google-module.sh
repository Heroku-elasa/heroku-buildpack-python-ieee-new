#!/bin/bash 

Current_DIR="$PWD"
echo ${Current_DIR}
source ${Current_DIR}/.openshift/action_hooks/common

PYTHON_VERSION="2.7.4"
PCRE_VERSION="8.35"
NGINX_VERSION="1.6.0"
MEMCACHED_VERSION="1.4.15"
ZLIB_VERSION="1.2.8"
#PHP_VERSION="5.5.9"
PHP_VERSION="5.4.27"

APC_VERSION="3.1.13"
libyaml_package="yaml-0.1.4"

if [[ "$OPENSHIFT_LOG_DIR" = "" ]];then
	#echo "$OPENSHIFT_LOG_DIR" > "$OPENSHIFT_HOMEDIR/.env/OPENSHIFT_DIY_LOG_DIR"
	if [ ! -d ~/home/openshifts ]; then	
        mkdir  ~/home/openshifts
	fi
	
	if [ ! -d /home/openshifts/logs ]; then	
        mkdir /home/openshifts/logs
	fi
	
	if [[ "OPENSHIFT_DIY_LOG_DIR" = "" ]];then
	
	    export OPENSHIFT_LOG_DIR='/home/openshifts/logs/'
	    echo 'OPENSHIFT_LOG_DIR is:'
	    echo $OPENSHIFT_LOG_DIR
	else
	    export OPENSHIFT_LOG_DIR=$OPENSHIFT_DIY_LOG_DIR
	    echo 'OPENSHIFT_LOG_DIR is:'
	    echo $OPENSHIFT_LOG_DIR
	fi
else
   echo "Exists"
   echo 'OPENSHIFT_LOG_DIR is:'
	echo $OPENSHIFT_LOG_DIR
fi

if [[ "$OPENSHIFT_TMP_DIR" = "" ]]; then	
	#mkdir  ~/home/openshifts
	if [ ! -d /home/openshifts/tmp ]; then	
        mkdir /home/openshifts/tmp
	fi
	export OPENSHIFT_TMP_DIR='~/home/openshifts/tmp/'
	echo 'OPENSHIFT_TMP_DIR2 is:'
	echo $OPENSHIFT_TMP_DIR
fi
export OPENSHIFT_TMP_DIR2=${OPENSHIFT_TMP_DIR}
if [  "$OPENSHIFT_HOMEDIR" = "" ]; then	
	if [ ! -d /home/openshifts/app-root ]; then	
        mkdir /home/openshifts/app-root
	fi
	
	if [ ! -d /home/openshifts/app-root/runtime ]; then	
        mkdir /home/openshifts/app-root/runtime
	fi
	
	export OPENSHIFT_HOMEDIR='/home/openshifts/'
	echo 'OPENSHIFT_HOMEDIR is:'
	echo $OPENSHIFT_HOMEDIR
fi


if [ ! -d ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv ]; then	
    mkdir ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv
	
fi
if [ ! -d ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/tmp ]; then	
    mkdir ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/tmp
fi
export OPENSHIFT_TMP_DIR2=${OPENSHIFT_TMP_DIR}
export OPENSHIFT_TMP_DIR2=${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/tmp
if [ ! -d ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/nginx/sbin ]; then	
	cd $OPENSHIFT_TMP_DIR2
	wget http://nginx.org/download/nginx-${NGINX_VERSION}.tar.gz
	tar zxf nginx-${NGINX_VERSION}.tar.gz
	rm nginx-${NGINX_VERSION}.tar.gz
	wget ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/pcre-${PCRE_VERSION}.tar.gz
	tar zxf pcre-${PCRE_VERSION}.tar.gz
	rm pcre-${PCRE_VERSION}.tar.gz
	wget http://zlib.net/zlib-${ZLIB_VERSION}.tar.gz
	
	wget "https://www.openssl.org/source/openssl-1.0.1j.tar.gz"
	tar xzvf openssl-1.0.1j.tar.gz
	rm openssl-1.0.1j.tar.gz
	#nginx google scholar
	git clone https://github.com/cuber/ngx_http_google_filter_module
	git clone https://github.com/yaoweibin/ngx_http_substitutions_filter_module
	
	#upstreem optimizaing
	#https://github.com/yzprofile/ngx_http_dyups_module
	git clone git://github.com/yzprofile/ngx_http_dyups_module.git
	
	
	git clone https://github.com/cep21/healthcheck_nginx_upstreams.git
	
	# cpu load balance
	git clone https://github.com/alibaba/nginx-http-sysguard.git
	
	tar -zxf zlib-${ZLIB_VERSION}.tar.gz
	rm zlib-${ZLIB_VERSION}.tar.gz
	if [ ! -d ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/nginx ]; then	
		mkdir ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/nginx
	fi
	
	cd nginx-${NGINX_VERSION}	
	nohup sh -c "./configure\
	   --with-cc-opt='-g -O2 -fstack-protector --param=ssp-buffer-size=4 -Wformat -Werror=format-security -D_FORTIFY_SOURCE=2' \
	   --with-ld-opt='-Wl,-Bsymbolic-functions -Wl,-z,relro' \
	   --prefix=${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/nginx\
	   --with-pcre=${OPENSHIFT_TMP_DIR2}/pcre-${PCRE_VERSION}\
	   --with-zlib=${OPENSHIFT_TMP_DIR2}/zlib-${ZLIB_VERSION}\
	   --with-openssl=${OPENSHIFT_TMP_DIR2}/openssl-1.0.1j\
	   --add-module=${OPENSHIFT_TMP_DIR2}/ngx_http_google_filter_module\
       --add-module=${OPENSHIFT_TMP_DIR2}/ngx_http_substitutions_filter_module\
	   --add-module=${OPENSHIFT_TMP_DIR2}/ngx_http_dyups_module\
	   --add-module=${OPENSHIFT_TMP_DIR2}/healthcheck_nginx_upstreams\
	   --add-module=${OPENSHIFT_TMP_DIR2}/nginx-http-sysguard\
	   --http-proxy-temp-path=${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/nginx/proxy\
	   --http-client-body-temp-path=${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/nginx/client_body_temp\
	   --http-fastcgi-temp-path=${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/nginx/fastcgi_temp\
	   --with-http_ssl_module\
	   --with-http_realip_module \
	   --with-http_addition_module \
	   --with-http_dav_module \
	   --with-http_flv_module \
	   --with-http_mp4_module \
	   --with-http_gunzip_module\
	   --with-http_gzip_static_module \
	   --with-http_random_index_module \
	   --with-http_secure_link_module\
	   --with-http_stub_status_module \
       --with-http_geoip_module \
       --with-http_image_filter_module \
       --with-http_spdy_module \
       --with-http_sub_module \
       --with-http_xslt_module \
	   --with-mail \
	   --with-mail_ssl_module \
	   --with-file-aio\
	   --with-debug\
	   --with-pcre-jit \
	   --with-ipv6 && make && make install && make clean" > $OPENSHIFT_LOG_DIR/Nginx_config.log 2>&1 & 
	bash -i -c 'tail -f $OPENSHIFT_LOG_DIR/Nginx_config.log'
	#trap " " INT
	#tail -f $OPENSHIFT_LOG_DIR/Nginx_config.log
	#trap - INT
	#echo 5
	
	#nohup sh -c "make && make install && make clean"  > $OPENSHIFT_LOG_DIR/nginx_install.log /dev/null 2>&1 &  
	#bash -i -c 'tail -f $OPENSHIFT_LOG_DIR/nginx_install.log'
	#./configure --with-pcre=$OPENSHIFT_TMP_DIR2/pcre-8.35 --prefix=$OPENSHIFT_DATA_DIR/nginx --with-http_realip_module
	#make &&	make install
fi


echo "INSTALL PHP"
if [ ! -d ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/php-${PHP_VERSION}/sbin ]; then
	cd $OPENSHIFT_TMP_DIR2
	wget http://us1.php.net/distributions/php-${PHP_VERSION}.tar.gz
	tar zxf php-${PHP_VERSION}.tar.gz
	cd php-${PHP_VERSION}
	wget -c http://us.php.net/get/php-${PHP_VERSION}.tar.gz/from/this/mirror
	tar -zxf mirror	
	mkdir ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/php-${PHP_VERSION}
	cd php-${PHP_VERSION}
	
	nohup sh -c "./configure --with-mysql=mysqlnd\
        --with-mysqli=mysqlnd --with-pdo-mysql=mysqlnd\
        --prefix=${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/php-${PHP_VERSION}\
        --enable-fpm --with-zlib --enable-xml --enable-bcmath --with-curl --with-gd \
        --enable-zip --enable-mbstring --enable-sockets --enable-ftp && make && make install && make clean"  > $OPENSHIFT_LOG_DIR/php_install_conf.log /dev/null 2>&1 &  
	bash -i -c 'tail -f $OPENSHIFT_LOG_DIR/php_install_conf.log'
	#nohup sh -c "make && make install && make clean"  > $OPENSHIFT_LOG_DIR/php_install.log 2>&1 &  
	#bash -i -c 'tail -f $OPENSHIFT_LOG_DIR/php_install.log'
	#./configure --with-mysql=mysqlnd --with-mysqli=mysqlnd --with-pdo-mysql=mysqlnd --prefix=${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/php-5.4.27 --enable-fpm --with-zlib --enable-xml --enable-bcmath --with-curl --with-gd --enable-zip --enable-mbstring --enable-sockets --enable-ftp
#	make && make install
	cp  $OPENSHIFT_TMP_DIR2/php-${PHP_VERSION}/php.ini-production ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/php-${PHP_VERSION}/lib/php.ini
fi	
echo "Cleanup"

PYTHON_CURRENT=`${OPENSHIFT_RUNTIME_DIR}/srv/python/bin/python -c 'import sys; print(".".join(map(str, sys.version_info[:3])))'`

#checked
if [ "$PYTHON_CURRENT" != "$PYTHON_VERSION" ]; then
	cd $OPENSHIFT_TMP_DIR2
	if [ ! -d ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python ]; then
       mkdir ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python
	fi
	wget http://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tar.bz2
	tar jxf Python-${PYTHON_VERSION}.tar.bz2
	rm -rf Python-${PYTHON_VERSION}.tar.bz2
	cd Python-${PYTHON_VERSION}
	
	#./configure --prefix=$OPENSHIFT_DATA_DIR
	nohup sh -c "./configure --prefix=${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python && make install && make clean "   > $OPENSHIFT_LOG_DIR/pyhton_install.log 2>&1 &
	bash -i -c 'tail -f $OPENSHIFT_LOG_DIR/pyhton_install.log'
	#nohup sh -c "make && make install && make clean"   >  $OPENSHIFT_LOG_DIR/pyhton_install.log 2>&1 &
	
	export "export path"
	export PATH=${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin:$PATH
	nohup sh -c "export PATH=$OPENSHIFT_HOMEDIR/app-root/runtime/srv/python/bin:$PATH " > $OPENSHIFT_LOG_DIR/path_export2.log 2>&1 &
	echo '--Install Setuptools--'

	cd $OPENSHIFT_TMP_DIR2
	
	#installing easy_install
	wget https://pypi.python.org/packages/source/s/setuptools/setuptools-1.1.6.tar.gz #md5=ee82ea53def4480191061997409d2996
	tar xzvf setuptools-1.1.6.tar.gz
	rm setuptools-1.1.6.tar.gz
	cd setuptools-1.1.6	
	
	${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/python setup.py install
	
	OPENSHIFT_RUNTIME_DIR=${OPENSHIFT_HOMEDIR}/app-root/runtime
	OPENSHIFT_REPO_DIR=${OPENSHIFT_HOMEDIR}/app-root/runtime/repo
	echo '---Install pip---'
	cd $OPENSHIFT_TMP_DIR2
	wget https://raw.github.com/pypa/pip/master/contrib/get-pip.py
	${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/python get-pip.py
	mkdir trash
	cd trash
	wget http://entrian.com/goto/goto-1.0.zip
	unzip goto-1.0.zip
	cd goto-1.0
	${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/python setup.py install
	
	#memcached for python
	wget ftp://ftp.tummy.com/pub/python-memcached/python-memcached-latest.tar.gz
	tar -zxvf python-memcached-latest.tar.gz
	cd python-memcached-*	
	$OPENSHIFT_HOMEDIR/app-root/runtime/srv/python/bin/python setup.py install
	cd ../..
	rm -rf trash
	
	cd
	echo '---instlling tornado -----'
	nohup sh -c "\
	${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/easy_install tornado==4.0.1 && \	
	${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/easy_install lamson && \
	${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/easy_install BeautifulSoup==3.2.1 && \	
	${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/easy_install mechanize==0.2.5 && \	
	${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/easy_install pypdf==1.12 && \
	${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/easy_install mongolog && \
	${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/easy_install django && \
	${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/easy_install hurry.filesize && \
	${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/easy_install reportlab==3.0 && \
	${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/easy_install pdfrw && \
	${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/easy_install webapp2 && \
	${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/easy_install google && \	
	${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/easy_install selenium && \
	${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/easy_install twill==0.9.1 && \
	${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/pip  install lxml==3.2.3 && \
	${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/easy_install cssselect==0.9.1 && \
	${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/easy_install django-screamshot && \
	${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/easy_install img2pdf && \
	${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/easy_install pdfminer && \
	${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/easy_install pdfparanoia && \
	${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/easy_install youtube-dl && \	
	${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/easy_install requesocks==0.10.8 && \	
	${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/easy_install requests==2.4.1"> $OPENSHIFT_LOG_DIR/python_modules_install_1.log /dev/null 2>&1 &  
	#tail -f  $OPENSHIFT_LOG_DIR/python_modules_install_1.log
	#install pdf logo removal (pdfparanoia)
	${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/easy_install feedparser 
	${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/easy_install uwsgi 
	${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/easy_install cookielib 
	nohup sh -c "\	
	${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/easy_install uwsgi  && \	
	${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/easy_install cookielib"> $OPENSHIFT_LOG_DIR/python_modules_install_1_1.log /dev/null 2>&1 &  
	#tail -f  $OPENSHIFT_LOG_DIR/python_modules_install_1_1.log
	#scholar pachage
	nohup sh -c "/
	${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/easy_install  google-scholar-scraper && \
	${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/easy_install springerdl"> $OPENSHIFT_LOG_DIR/python_modules_install_2.log /dev/null 2>&1 &  
	#tail -f  $OPENSHIFT_LOG_DIR/python_modules_install.log
	#upload package
	${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/easy_install dbupload 
	nohup sh -c "/	
	${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/pip install click && \
	${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/pip install wget && \
	${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/pip install dropbox && \
	${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/pip install PyDrive && \
	${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/pip install mega.py && \
	${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/pip install pymediafire && \
	${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/easy_install s3web"> $OPENSHIFT_LOG_DIR/python_modules_install_3.log /dev/null 2>&1 &  
	#tail -f  $OPENSHIFT_LOG_DIR/python_modules_install_3.log
	#upload to mega.co.nz 50 gig free
	#git clone https://github.com/TobiasTheViking/megaannex.git
	nohup sh -c "/${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/pip install megacl"> $OPENSHIFT_LOG_DIR/python_modules_install_4.log /dev/null 2>&1 &  
	
	#upload ftp
	nohup sh -c "/
	${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/easy_install ftpsync &&\
	${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/easy_install Crypto && \
	${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/pip install paramiko && \
	${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/easy_install pycrypto && \
	${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/pip install fabric"> $OPENSHIFT_LOG_DIR/python_modules_install_5.log /dev/null 2>&1 &  
	#tail -f  $OPENSHIFT_LOG_DIR/python_modules_install_5.log
	#install ghost webdirver
	#${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/easy_install 
	
	#install PyQt
	
	wget http://sourceforge.net/projects/pyqt/files/PyQt4/PyQt-4.9.6/PyQt-mac-gpl-4.9.6.tar.gz
	tar xzvf PyQt-mac-gpl-4.9.6.tar.gz
	cd PyQt-mac-gpl-4.9.6
	#install google-app
	${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/pip install python-appengine #make working GAE code for any python
	${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/pip install pyyaml
	${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/pip install gae_installer
	${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/pip install webob
	${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/pip install Paste
	#must to install django <=1.1.4 pip install Django==1.1.4 
	#wget storage.googleapis.com/appengine-sdks/featured/google_appengine_1.9.13.zip
	#unzip google_appengine_1.9.13.zip
	#cd google_appengine
	
	nohup sh -c "/
	mkdir ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/google-app-sdk && \
	mv google_appengine ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/google_appengine && \
	export PATH=$PATH:${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/google_appengine && \
	${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/pip install appengine"> $OPENSHIFT_LOG_DIR/python_modules_install_6.log /dev/null 2>&1 &  
	
	
	mkdir ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/gmp
	wget https://ftp.gnu.org/gnu/gmp/gmp-6.0.0a.tar.bz2
	tar -xvjpf gmp-6.0.0a.tar.bz2
	cd gmp-6.0.0a
	nohup sh -c "./configure --prefix=${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/gmp && make && make check  &&make install && make clean "   > $OPENSHIFT_LOG_DIR/gmp_install.log 2>&1 &
	#tail -f $OPENSHIFT_LOG_DIR/gmp_install.log
	
	
	mkdir ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/tornado
	#wget balabal
	#unzip bala
	

fi

# echo 'Make uwsgi '
	cd $OPENSHIFT_TMP_DIR2
	mkdir ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python
	wget http://projects.unbit.it/downloads/uwsgi-latest.tar.gz
	tar zxvf uwsgi-latest.tar.gz
	cd uwsgi-2.0.7

rm -rf $OPENSHIFT_TMP_DIR2/*

	
if [[ `lsof -n -P | grep 8080` ]];then
	kill -9 `lsof -t -i :8080`
	lsof -n -P | grep 8080
fi
if [[ `lsof -n -P | grep 9000` ]];then
	kill -9 `lsof -t -i :9000`
	lsof -n -P | grep 9000
fi	
#---starting nginx ----
nohup sh -c "${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/nginx/sbin/nginx -c  ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/nginx/conf/nginx.conf.default" > $OPENSHIFT_LOG_DIR/nginx_run.log 2>&1 & 
#tail -f $OPENSHIFT_LOG_DIR/nginx_run.log
#nohup sh -c"${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/php-${PHP_VERSION}/sbin/php-fpm -c  ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/php-${PHP_VERSION}/etc/php-fpm.conf"  > $OPENSHIFT_LOG_DIR/php_run.log 2>&1 & tail -f $OPENSHIFT_LOG_DIR/php_run.log
nohup sh -c "${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/php-${PHP_VERSION}/sbin/php-fpm" >  $OPENSHIFT_LOG_DIR/php_run.log 2>&1 &
#tail -f $OPENSHIFT_LOG_DIR/php_run.log
#---stoping nginx ----
nohup sh -c "killall nginx" > $OPENSHIFT_LOG_DIR/nginx_stop.log 2>&1 &
nohup sh -c "killall php-fpm" > $OPENSHIFT_LOG_DIR/php-fpm_stop.log 2>&1 &

#nohup sh -c  "./install-nginx-php.sh" > $OPENSHIFT_LOG_DIR/main_install.log /dev/null 2>&1  & tail -f $OPENSHIFT_LOG_DIR/main_install.log

#emailing 
# echo | mail -s "Subject" -r from@address -q mail.sh  ss3@elec-lab.tk -a "Content-Type: text/plain; charset=UTF-8" 
# echo | mail -s "Subject" -r from@address -q mail.sh  soheil_paper@yahoo.com -a "Content-Type: text/plain; charset=UTF-8" 
 
 #wget -e use_proxy=yes -e http_proxy=219.223.190.90:3128  "http://s28.hexupload.com/files/3/kzx4asbhcczhr4/sayaree.meymonha.720p.farsi(P30Movie.ir).mkv"
 #nohup sh -c  "wget -e use_proxy=yes -e http_proxy=143.89.225.246:3128  "http://s32.uploadbaz.com/files/8/tkmoe9k40pmrmw/Dawn.Of.The.Planet.Of.The.Apes.2014.CAM.x264.avi"" > $OPENSHIFT_LOG_DIR/main_install.log /dev/null 2>&1  & tail -f $OPENSHIFT_LOG_DIR/main_install.log
# nohup sh -c  "rm -rf androd-ebooks* " > $OPENSHIFT_LOG_DIR/main_installw.log /dev/null 2>&1  & tail -f $OPENSHIFT_LOG_DIR/main_installw.log