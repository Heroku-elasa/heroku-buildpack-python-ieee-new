mkdir  $OPENSHIFT_HOMEDIR/app-root/runtime/srv/p7zip
cd /tmp
wget http://downloads.sourceforge.net/project/p7zip/p7zip/9.38.1/p7zip_9.38.1_src_all.tar.bz2

tar xf p7zip_9.38.1_src_all.tar.bz2
cd p*

make && make install DEST_HOME=$OPENSHIFT_HOMEDIR/app-root/runtime/srv/p7zip
PATH="$PATH:$OPENSHIFT_HOMEDIR/app-root/runtime/srv/p7zip/bin/"
cd /tmp
rm -rf *

wget http://prestatools.ir/download/prestashop_1.6.0.14_Farsi_PrestaTools.Ir.zip
wget http://ipresta.ir/downloads/prestashop_1.6.0.6_rtl_2.0.zip ###GOOOD
unzip prest*
mkdir $OPENSHIFT_HOMEDIR/app-root/repo/php/p3
cp -fauv   prest*/* $HOME/app-root/runtime/repo/php/themes

#zip -r presta1-6_persioan.zip $HOME/app-root/runtime/repo/php/p6
#zip -r Vb-comunity.zip $HOME/app-root/runtime/repo/php/*
#cp -fauv   * $HOME/app-root/runtime/repo/php/the*
#mkdir $HOME/app-root/runtime/repo/php/themes/bt
mysql -u $OPENSHIFT_MYSQL_DB_USERNAME -p$OPENSHIFT_MYSQL_DB_PASSWORD -e "create database 1presta4shop";

mysql  -u $OPENSHIFT_MYSQL_DB_USERNAME -p$OPENSHIFT_MYSQL_DB_PASSWORD  presta4shop < 1441318603-13ba395a.sql.bz2

mysql  -u $OPENSHIFT_MYSQL_DB_USERNAME -p$OPENSHIFT_MYSQL_DB_PASSWORD  p1resta4shop > 2_update-database.sql 

#wget http://wp-gl22.rhcloud.com/rp/0x14/leo-dress-store-prestashop-theme.7z

 $OPENSHIFT_HOMEDIR/app-root/runtime/srv/p7zip/bin/7za  x leo-dress-store-prestashop-theme.7z
 
cd leo* && cd t* && cd q*
unzip leo_dressstore_quickstart_v15x.zip

mv leo_dressstore/* $OPENSHIFT_HOMEDIR/app-root/repo

cd $OPENSHIFT_HOMEDIR/app-root/repo
#cp -fauv themes/* $OPENSHIFT_HOMEDIR/app-root/repo/p2/themes

#cp -fauv modules/* $OPENSHIFT_HOMEDIR/app-root/repo/p2/modules

#free themes
http://prestatools.ir/download/ae22582662b2d30a80a6903d60f24199.zip
https://wp-gl22.rhcloud.com/rp/0x14/termeh_freee.zip

https://wp-gl22.rhcloud.com/rp/0x14/home_ac_theme.zip

https://wp-gl22.rhcloud.com/rp/0x14/4273b87883d543ceadd4472087436119.zip

https://wp-gl22.rhcloud.com/rp/0x14/c11df0de035208351c359107d56c10f1.zip

http://apollotheme.com//upfiledownload/ap-funiture-prestashop256/free1610ap_funiture.zip

http://apollotheme.com/upfiledownload/ap_underwaer/free-version/1610freeap_underwear.zip