mkdir  $OPENSHIFT_HOMEDIR/app-root/runtime/srv/p7zip
cd /tmp
wget http://downloads.sourceforge.net/project/p7zip/p7zip/9.38.1/p7zip_9.38.1_src_all.tar.bz2

tar xf p7zip_9.38.1_src_all.tar.bz2
cd p*

make && make install DEST_HOME=$OPENSHIFT_HOMEDIR/app-root/runtime/srv/p7zip
PATH="$PATH:$OPENSHIFT_HOMEDIR/app-root/runtime/srv/p7zip/bin/"
