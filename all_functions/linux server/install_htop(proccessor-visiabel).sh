mkdir  $OPENSHIFT_HOMEDIR/app-root/runtime/srv/dtrx
cd /tmp

wget http://pkgs.fedoraproject.org/lookaside/pkgs/dtrx/dtrx-7.1.tar.gz/4be207724b75aea3e9f93374298b2174/dtrx-7.1.tar.gz
tar xvf dtrx-7.1.tar.gz
cd dtrx-7.1
python setup.py install --prefix=$OPENSHIFT_HOMEDIR/app-root/runtime/srv/dtrx
 
# Then just make sure that you have /usr/local/bin in your cygwin path, with a line like 
# the following in your .bashrc
PATH="$PATH:$OPENSHIFT_HOMEDIR/app-root/runtime/srv/dtrx"

 $OPENSHIFT_HOMEDIR/app-root/runtime/srv/dtrx/bin/dtrx
 
 