#!/bin/bash 
#it is not completed

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
	
	export OPENSHIFT_LOG_DIR='/home/openshifts/logs/'
	echo 'OPENSHIFT_LOG_DIR is:'
	echo $OPENSHIFT_LOG_DIR
else
   echo "Exists"
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

mkdir ~/app-root/runtime/srv	
mkdir ~/app-root/runtime/srv/mysql
	nohup sh -c  "wget http://dev.mysql.com/get/Downloads/MySQL-5.5/mysql-5.5.28-linux2.6-i686.tar.gz/from/http://cdn.mysql.com/"  > $OPENSHIFT_LOG_DIR/mysql_install_conf.log /dev/null 2>&1 &  
	tail -f $OPENSHIFT_LOG_DIR/mysql_install_conf.log
	
#tar xzf mysql-5.5.28-linux2.6-i686.tar.gz
tar xzf *
ln -s mysql-5.5.28-linux2.6-i686 ~/app-root/runtime/srv/mysql

groupadd mysql 
useradd -r -g mysql mysql

cd ~/app-root/runtime/srv/mysql
chown -R mysql.mysql . 
scripts/mysql_install_db --user=mysql 
chown -R root . 
chown -R mysql data

cd ~/app-root/runtime/srv/mysql
cat > rc.mysqld <<EOF
#!/bin/sh
# Start/stop/restart mysqld.
#
# Copyright 2003  Patrick J. Volkerding, Concord, CA
# Copyright 2003  Slackware Linux, Inc., Concord, CA
# Copyright 2008  Patrick J. Volkerding, Sebeka, MN
#
# This program comes with NO WARRANTY, to the extent permitted by law.
# You may redistribute copies of this program under the terms of the
# GNU General Public License.

# To start MySQL automatically at boot, be sure this script is executable:
# chmod 755 /etc/rc.d/rc.mysqld

# Before you can run MySQL, you must have a database.  To install an initial
# database, do this as root:
#
#   mysql_install_db --user=mysql
#
# Note that the mysql user must exist in /etc/passwd, and the created files
# will be owned by this dedicated user.  This is important, or else mysql
# (which runs as user "mysql") will not be able to write to the database
# later (this can be fixed with 'chown -R mysql.mysql /var/lib/mysql').
#
# To increase system security, consider using "mysql_secure_installation"
# as well.  For more information on this tool, please read:
#   man mysql_secure_installation

# To allow outside connections to the database comment out the next line.
# If you don't need incoming network connections, then leave the line
# uncommented to improve system security.
# SKIP="--skip-networking"

DATA="~/app-root/runtime/srv/mysql/data"
MYSQLD="~/app-root/runtime/srv/mysql/bin/mysqld_safe"
PID="$DATA/mysql.pid"

# Start mysqld:
mysqld_start() {
  if [ -x $MYSQLD ]; then
    # If there is an old PID file (no mysqld running), clean it up:
    if [ -r $PID ]; then
      if ! ps axc | grep mysqld 1> /dev/null 2> /dev/null ; then
        echo "Cleaning up old $PID."
        rm -f $PID
      fi
    fi
    $MYSQLD --datadir=$DATA --pid-file=$PID $SKIP &
  fi
}

# Stop mysqld:
mysqld_stop() {
  # If there is no PID file, ignore this request...
  if [ -r $PID ]; then
    killall mysqld
    # Wait at least one minute for it to exit, as we dont know how big the DB is...
    for second in 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 \
      0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 60 ; do
      if [ ! -r $PID ]; then
        break;
      fi
      sleep 1
    done
    if [ "$second" = "60" ]; then
      echo "WARNING:  Gave up waiting for mysqld to exit!"
      sleep 15
    fi
  fi
}

# Restart mysqld:
mysqld_restart() {
  mysqld_stop
  mysqld_start
}

case "$1" in
'start')
  mysqld_start
  ;;
'stop')
  mysqld_stop
  ;;
'restart')
  mysqld_restart
  ;;
*)
  echo "usage $0 start|stop|restart"
esac
EOF

chmod a+x rc.mysqld

cd ~/app-root/runtime/srv/mysql/bin 
./mysql -u root -p
SET PASSWORD FOR 'root'@'localhost' = PASSWORD('your-mysql-passowrd');
SET PASSWORD FOR 'root'@'127.0.0.1' = PASSWORD('your-mysql-passowrd');
SET PASSWORD FOR 'root'@'localhost.localdomain' = PASSWORD('your-mysql-passowrd');
DROP DATABASE test;
DROP USER ''@'localhost';
DROP USER ''@'localhost.localdomain';

fi

############### Method 2 for install mysql ################
cd /tmp
wget http://wiki.diahosting.com/down/lnmp/mysql-5.1.46.tar.gz
nohup sh -c "./configure --prefix=${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/mysql --enable-assembler --with-charset=utf8 --enable-thread-safe-client --with-extra-charsets=all --with-big-tables &&
make && make install"> $OPENSHIFT_LOG_DIR/mysql_install.log /dev/null 2>&1 & tail -f  $OPENSHIFT_LOG_DIR/mysql_install.log

chown -R mysql:mysql ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/mysql

cp support-files/my-medium.cnf /etc/my.cnf

sed -i 's#\[mysqld\]#\[mysqld\]\nbasedir=/usr/local/mysql\ndatadir=/var/lib/mysql\n#' /etc/my.cnf
sed -i 's#log-bin=mysql-bin#\#log-bin=mysql-bin#' /etc/my.cnf
sed -i 's#binlog_format=mixed#\#binlog_format=mixed#' /etc/my.cnf

${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/mysql/bin/mysql_install_db --basedir=${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/mysql  --datadir=/var/lib/mysql --user=mysql

cp ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/mysql/share/mysql/mysql.server /etc/init.d/mysqld
chmod 755 /etc/init.d/mysqld

/etc/init.d/mysqld start

${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/mysql/bin/mysqladmin -u root password $myrootpwd

chkconfig mysqld on

#ln -s ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/mysql/bin/myisamchk /usr/bin/
#ln -s ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/mysql/bin/mysql /usr/bin/
#ln -s ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/mysql/bin/mysqldump /usr/bin/



############## end of methos 2 from install mysql #################
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