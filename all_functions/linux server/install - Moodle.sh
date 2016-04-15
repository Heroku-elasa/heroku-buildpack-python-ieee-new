cd 
cd app-root/runtime/repo/php
wget https://download.moodle.org/download.php/direct/stable30/moodle-3.0.2.zip
unzip *
mv mo*/* .
mysql -u $OPENSHIFT_MYSQL_DB_USERNAME -p$OPENSHIFT_MYSQL_DB_PASSWORD -e "create database moodle";

env |grep sql
find -name theme

##Themes
cd app-root/runtime/repo/php/theme
mkdir tt
cd tt
wget https://moodle.org/plugins/download.php/10136/theme_roshnilite_moodle30_2015092107.zip
unzip *
mv ro* ..