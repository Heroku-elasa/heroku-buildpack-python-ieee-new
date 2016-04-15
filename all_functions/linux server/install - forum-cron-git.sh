sendmail -f "elsa.group@gmail.com" -t "soheil_paper@yahoo.com" -m "backup" -u "communiuty"   -a "/tmp/Forum-*.sql.gz" 

mkdir /tmp/email
cd /tmp/email
#mkdir /tmp/email/db
#cd /tmp/email/db
#mysql  -u $OPENSHIFT_MYSQL_DB_USERNAME -p$OPENSHIFT_MYSQL_DB_PASSWORD  p1resta4shop3 > p1resta4shop3new.sql
nohup sh -c " mysql -f -u $OPENSHIFT_MYSQL_DB_USERNAME -p$OPENSHIFT_MYSQL_DB_PASSWORD  p1resta4shop3 > p1resta4shop3.sql"  > $OPENSHIFT_LOG_DIR/mysql.log /dev/null 2>&1 & 
nohup sh -c " mysql -f -u $OPENSHIFT_MYSQL_DB_USERNAME -p$OPENSHIFT_MYSQL_DB_PASSWORD  dr2omnia > dr2omnia.sql"  > $OPENSHIFT_LOG_DIR/mysql.log /dev/null 2>&1 & 

cd /tmp
zip -r    p1resta4shop34new3.zip  p1resta4shop34new3.sql

cd /tmp/email
zip -r    p1resta4shop3.zip  p1resta4shop3.sql
zip -r sites.zip  $HOME/app-root/data/sites/
nohup sh -c " zip -r shopping.zip $HOME/app-root/runtime/repo/php/"  > $OPENSHIFT_LOG_DIR/zipping_conf.log /dev/null 2>&1 &  
 #zip -r -s 10m vbuletin-4-1-2.zip $HOME/app-root/runtime/repo/php/
 
 #cat vbuletin-4-1-2* vbuletin-4-1-2* vbuletin-4-1-2* >vbuletin-4-1-2-final.zip
#gzip -c vbuletin-4-1-2.zip | split -b 10MiB - vbuletin-4-1-2.gz_


mkdir /tmp/db
cd /tmp/db
mysql  -u $OPENSHIFT_MYSQL_DB_USERNAME -p$OPENSHIFT_MYSQL_DB_PASSWORD  p1resta4shop3 > p1resta4shop3.sql
mysql  -u $OPENSHIFT_MYSQL_DB_USERNAME -p$OPENSHIFT_MYSQL_DB_PASSWORD  dr2omnia > dr2omnia.sql

cd





cd /tmp

cd ~/app-root/runtime/repo/php
rm  shopping.zip
#git rm -r --cached
#find . | grep .git | xargs rm -rf #remove git files working
#find  .git | xargs rm -rf
 cd ~/app-root/runtime/repo/.openshift/cron/daily/
# ~/app-root/data/sites
#ln -s sites_new ~/app-root/data/sites

cat << 'EOF' > my-github.sh
cd ~/app-root/runtime/repo/php
#find . | grep .git | xargs rm -rf #remove git files  working
echo "# openshift-test" >> README.md
git init

git add README.md
git add .
git init
cd ~/app-root/data/sites
git add .
git add shopping.zip
#git config --global user.name "soheilpaper"
#git config --global user.email soheil_paper@yahoo.com
 #git commit --amend --reset-author
git commit -a  -m "first commit"

#git remote add origin https://soheilpaper:ss123456@github.com/soheilpaper/openshift-test.git
#git remote add origin https://github.com/soheilpaper/openshift-test.git
git config remote.origin.url https://soheilpaper:ss123456@github.com/soheilpaper/elasa.ir.git

#git remote add origin https://soheilpaper@bitbucket.org/soheilpaper/shopping.elasa.ir.git
#git config remote.origin.url  https://soheilpaper:ss123456@bitbucket.org/soheilpaper/shopping.elasa.ir.git

#git config remote.origin.url  https://soheilpaper:ss123456@bitbucket.org/soheilpaper/shop2.elasa.ir.git


#git config remote.origin.url https://elasa:ss123456@gitlab.com/elasa/ieee2.git

#git pull 
git push -u origin master

EOF
#chmod 755 . -R
chmod 755 my-github.sh
nohup sh -c " ./my-github.sh"> $OPENSHIFT_LOG_DIR/git-hub.log /dev/null 2>&1 &  
#tail -f  $OPENSHIFT_LOG_DIR/git-hub.log
nohup sh -c " ~/app-root/runtime/repo/.openshift/cron/daily/my-github.sh"> $OPENSHIFT_LOG_DIR/git-hub.log /dev/null 2>&1 & 
#tail -f  $OPENSHIFT_LOG_DIR/git-hub.log 
 ./my-github.sh
 
 
 #cd  $HOME/app-root/runtime/repo/php/
#${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/python my_dropbox.py

