#!/bin/sh
# http://www.falkotimme.com/howtos/sendmail_smtp_auth_tls/

mkdir $OPENSHIFT_HOMEDIR/app-root/runtime/tmp/
mkdir  $OPENSHIFT_HOMEDIR/app-root/runtime/srv/siege

if [ ! -d "$OPENSHIFT_HOMEDIR/app-root/runtime/srv/siege/bin" ]; then
	cd $OPENSHIFT_HOMEDIR/app-root/runtime/tmp
	rm -rf *

	
	nohup sh -c "./configure --prefix=$OPENSHIFT_HOMEDIR/app-root/runtime/srv/siege"  > $OPENSHIFT_LOG_DIR/siege_install_conf.log /dev/null 2>&1 &  
	tail -f $OPENSHIFT_LOG_DIR/siege_install_conf.log
	nohup sh -c "make && make install && make clean"  > $OPENSHIFT_LOG_DIR/siege_install.log 2>&1 &  
	tail -f $OPENSHIFT_LOG_DIR/siege_install.log
	

fi

mkdir  $OPENSHIFT_HOMEDIR/app-root/runtime/srv/sproxy

if [ ! -d "$OPENSHIFT_HOMEDIR/app-root/runtime/srv/sproxy/bin" ]; then
	
cd /tmp
wget http://www.openssl.org/source/openssl-0.9.7c.tar.gz
wget --passive-ftp ftp://ftp.andrew.cmu.edu/pub/cyrus-mail/cyrus-sasl-2.1.17.tar.gz
wget --passive-ftp ftp://ftp.sendmail.org/pub/sendmail/sendmail.8.12.11.tar.gz

 

#### Install Openssl

tar xvfz openssl-0.9.7c.tar.gz
cd openssl-0.9.7c
./configure --prefix=$OPENSHIFT_HOMEDIR/app-root/runtime/srv/openssl
make
make install
ln -s /usr/local/ssl/bin/openssl /usr/bin/openssl

 cd /tmp
tar xvfz cyrus-sasl-2.1.17.tar.gz
cd cyrus-sasl-2.1.17
./configure --prefix=$OPENSHIFT_HOMEDIR/app-root/runtime/srv/cyrus --enable-anon --enable-plain --enable-login --disable-krb4 --with-saslauthd=/var/run/saslauthd --with-pam --with-openssl=/usr/local/ssl --with-plugindir=/usr/local/lib/sasl2 --enable-cram --enable-digest --enable-otp
	make
make install

cd /tmp
tar xvfz sendmail.8.12.11.tar.gz
cd sendmail-8.12.11/devtools/Site/

mkdir  $OPENSHIFT_HOMEDIR/app-root/runtime/tmp
mkdir  $OPENSHIFT_HOMEDIR/app-root/runtime/srv
mkdir  $OPENSHIFT_HOMEDIR/app-root/runtime/srv/sendEmail
cd $OPENSHIFT_HOMEDIR/app-root/runtime/tmp

wget http://caspian.dotconf.net/menu/Software/SendEmail/sendEmail-v1.55.tar.gz
tar zxvf sendEmail-v1.55.tar.gz
cp sendEmail-v1.55/sendEmail  $OPENSHIFT_HOMEDIR/app-root/runtime/srv/sendEmail
chmod +x $OPENSHIFT_HOMEDIR/app-root/runtime/srv/sendEmail/sendEmail
 
 cd $OPENSHIFT_HOMEDIR/app-root/runtime/srv/sendEmail/
./sendEmail -f my.account@gmail.com -t soheil_paper@yahoo.com \
-u this is the test tile -m "this is a test message" \
-s smtp.gmail.com \
-o tls=yes \
-xu timachichihamed -xp amirkabir \
-a /tmp/email/vbuletin-4-1-2.zip


./sendEmail -f usernameonly@gmail.com -t +14256108659@txt.att.net \
-m This is an SMS message from Linux.\
-s smtp.gmail.com \
-o tls=yes \
-xu timachichihamed -xp amirkabir

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

#$OPENSHIFT_HOMEDIR/app-root/runtime/srv/siege/bin/siege -u http://arianeng.ir -d1 -r20000 -c20
#$OPENSHIFT_HOMEDIR/app-root/runtime/srv/siege/bin/siege -u http://shop.arianeng.ir -d1 -r200 -c15 --time=300H
#$OPENSHIFT_HOMEDIR/app-root/runtime/srv/siege/bin/siege  --header='Host: shop.arianeng.ir' --reps=1000 --time=300H --concurrent=10 --quiet --delay=1 http://shop.arianeng.ir
#$OPENSHIFT_HOMEDIR/app-root/runtime/srv/siege/bin/siege  --header='Host: arianeng.ir' --reps=500 --time=300H --concurrent=10 --quiet --delay=1 http://arianeng.ir

#$OPENSHIFT_HOMEDIR/app-root/runtime/srv/siege/bin/siege  --header='Host: ponisha.ir' --reps=1000 --time=300H --concurrent=10 --quiet --delay=1 http://ponisha.ir 
#$OPENSHIFT_HOMEDIR/app-root/runtime/srv/siege/bin/siege  --header='Host: ponisha.ir' --reps=1000 --time=300H --concurrent=1 --quiet --delay=0 http://bigfishs.tk/

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
