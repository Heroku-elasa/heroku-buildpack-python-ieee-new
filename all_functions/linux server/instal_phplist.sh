cd /tmp
mkdir tt
cd tt
wget http://prdownloads.sourceforge.net/phplist/phplist-3.0.12.zip?download

mv phplist-3.0.12.zip?download phplist.zipunzip 
unzip *
cd p*

mkdir $OPENSHIFT_HOMEDIR/app-root/repo/phplist1
cp -fauv   pub*/lis* $HOME/app-root/runtime/repo/phplist1


curl -s http://presta2-beyhagh.rhcloud.com/phplist1/lists/admin