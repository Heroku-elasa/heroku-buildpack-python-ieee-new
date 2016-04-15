#check mysql verssion
mysql  -u $OPENSHIFT_MYSQL_DB_USERNAME -p$OPENSHIFT_MYSQL_DB_PASSWORD  -e 'SHOW VARIABLES LIKE "%version%";'
mysql  -u $OPENSHIFT_MYSQL_DB_USERNAME -p$OPENSHIFT_MYSQL_DB_PASSWORD  -e 'STATUS'

mysql -u $OPENSHIFT_MYSQL_DB_USERNAME -p$OPENSHIFT_MYSQL_DB_PASSWORD -e 'show databases'
mysql -u $OPENSHIFT_MYSQL_DB_USERNAME -p$OPENSHIFT_MYSQL_DB_PASSWORD -e 'show databases'  | grep -v 'Database'
mysql -u $OPENSHIFT_MYSQL_DB_USERNAME -p$OPENSHIFT_MYSQL_DB_PASSWORD -e "create database p1resta4shop3";

mysql  -u $OPENSHIFT_MYSQL_DB_USERNAME -p$OPENSHIFT_MYSQL_DB_PASSWORD  p1resta4shop3 > p1resta4shop3.sql
mysql  -u $OPENSHIFT_MYSQL_DB_USERNAME -p$OPENSHIFT_MYSQL_DB_PASSWORD  $OPENSHIFT_APP_NAME <   moodle.sql 
gzip -d Forum-2016-01-03-Full-Backup.sql.gz
mysql  -f -u $OPENSHIFT_MYSQL_DB_USERNAME -p$OPENSHIFT_MYSQL_DB_PASSWORD   p1resta4shop34new2 < Forum-2016-01-03-Full-Backup.sql 

sed -e "s/^INSERT INTO/INSERT IGNORE INTO/" < Forum-2016-01-03-Full-Backup.sql | mysql -p$OPENSHIFT_MYSQL_DB_PASSWORD  p1resta4shop34new2

mysqldump -u $OPENSHIFT_MYSQL_DB_USERNAME:$OPENSHIFT_MYSQL_DB_PORT  $OPENSHIFT_APP_NAME < Forum-2016-01-02-Full-Backup.sql.gz 

#backup database;
mkdir /tmp/db-bup;
mysql -u $OPENSHIFT_MYSQL_DB_USERNAME -p$OPENSHIFT_MYSQL_DB_PASSWORD -e "show databases" \
| grep -Ev 'Database|information_schema' \
| while read dbname; \
do \
echo 'Dumping $dbname' \
#mysqldump -u $OPENSHIFT_MYSQL_DB_USERNAME -p$OPENSHIFT_MYSQL_DB_PASSWORD $dbname > /tmp/db-bup/$dbname.sql;\
echo "This is the message body" | mutt -a "/tmp/db-bup"$dbname.sql -s "subject of message" -- soheil_paper@yahoo.com\
done


#backup database;
rm -rf  /tmp/db-bup
mkdir /tmp/db-bup;
nohup sh -c " mysql -s -r -u $OPENSHIFT_MYSQL_DB_USERNAME -p$OPENSHIFT_MYSQL_DB_PASSWORD -e 'show databases' | while read db; do mysqldump -u $OPENSHIFT_MYSQL_DB_USERNAME -p$OPENSHIFT_MYSQL_DB_PASSWORD  $db -r /tmp/db-bup/${db}.sql; [[ $? -eq 0 ]] && gzip /tmp/db-bup/${db}.sql; done" > $OPENSHIFT_LOG_DIR/mysql.log /dev/null 2>&1 &  
tail -f $OPENSHIFT_LOG_DIR/mysql.log


#emailing

gzip -c /tmp/db-bup/p1resta4shop.sql  | mail -s "MySQL DB" soheil_paper@yahoo.com

mail -s "Backup" -a "/tmp/p1resta4shop3.sql" soheil_paper@yahoo.com

echo "This is the message body" | mutt -a "/tmp/"$dbname.sql -s "subject of message" -- soheil_paper@yahoo.com

echo "This is the message body" | mutt -a "/tmp/p1resta4shop.sql" -s "subject of message" -- soheil_paper@yahoo.com

echo "This is the message body" | mutt -a /tmp/p1resta4shop3.sql  -s "subject of message"  -- soheil_paper@yahoo.com


./sendEmail -f my.account@gmail.com -t soheil_paper@yahoo.com \
-u this is the test tile -m "this is a test message" \
-s smtp.gmail.com \
-o tls=yes \
-xu timachichihamed -xp amirkabir \
-a "/tmp/email/vbuletin-4-1-2.zip"


./sendEmail -f usernameonly@gmail.com -t 989156605321@txt.att.net \
-m This is an SMS message from Linux.\
-s smtp.gmail.com \
-o tls=yes \
-xu timachichihamed -xp amirkabir