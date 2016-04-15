cd /tmp
wget http://nmap.org/dist/nmap-6.40.tar.bz2
mkdir $OPENSHIFT_HOMEDIR/app-root/runtime/srv
mkdir $OPENSHIFT_HOMEDIR/app-root/runtime/srv/nmap
tar xvjf nmap-6.40.tar.bz2
cd nmap-6.40
./configure --prefix=$OPENSHIFT_HOMEDIR/app-root/runtime/srv/nmap
nohup  sh -c "make && make install && make clean "   > $OPENSHIFT_LOG_DIR/nmap.log 2>&1 &
tail -f $OPENSHIFT_LOG_DIR/nmap.log	

 

PATH="$PATH:$OPENSHIFT_HOMEDIR/app-root/runtime/srv/nmap/bin/"

nmap google.com -p 1443   -sV --version-all -oG - | grep -iq 'open'
