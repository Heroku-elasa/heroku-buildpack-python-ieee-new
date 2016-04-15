mkdir  $OPENSHIFT_HOMEDIR/app-root/runtime/srv
mkdir  $OPENSHIFT_HOMEDIR/app-root/runtime/srv/unrar

cd /tmp
wget http://www.rarlab.com/rar/rarlinux-3.9.2.tar.gz
wget http://www.rarlab.com/rar/rarlinux-x64-3.9.2.tar.gz
tar -xvzf rarlinux*
tar -xzvf  rarlinux-x64-3.9.2.tar.gz
cd rar

mv * $OPENSHIFT_HOMEDIR/app-root/runtime/srv/unrar
cd ..
rm -rf /tmp/rar
#make && make install DEST_HOME=$OPENSHIFT_HOMEDIR/app-root/runtime/srv/unrar
PATH="$PATH:$OPENSHIFT_HOMEDIR/app-root/runtime/srv/unrar/"
