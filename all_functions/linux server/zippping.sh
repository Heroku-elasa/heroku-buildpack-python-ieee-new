zip -r presta1-6_persioan.zip $HOME/app-root/runtime/repo/php/p6

zip -r vbuletin-4-1-2.zip $HOME/app-root/runtime/repo/php/

split -b 10m "vbuletin-4-1-2.zip" "vbuletin-4-1-2.zip.part-"

gzip -c vbuletin-4-1-2.zip | split -b 10MiB - vbuletin-4-1-2.gz_

mkdir /tmp/email
cd /tmp/email
nohup sh -c " zip -r vbuletin-4-1-2.zip $HOME/app-root/runtime/repo/php/"  > $OPENSHIFT_LOG_DIR/zipping_conf.log /dev/null 2>&1 &  
	tail -f $OPENSHIFT_LOG_DIR/zipping_conf.log
cd /tmp/ff
	
mv vbuletin-4-1-2.zip $HOME/app-root/runtime/repo/php/

ctl_all stop
zip -r p1resta4shop.zip  $HOME/mysql/data/p1resta4shop/

mail -s "Backup" -a "/tmp/ff/p1resta4shop.zip" soheil_paper@yahoo.com

mail -s "Backup" -a "/tmp/ff/vbuletin-4-1-2.zip" soheil_paper@yahoo.com


echo "This is the message body" | mutt -a "/tmp/Forum-2016-01-01-Full-Backup.sql.gz" -s "subject of message" -- soheil_paper@yahoo.com
sendmail -f "elsa.group@gmail.com" -t "soheil_paper@yahoo.com" -m "backup" -u "communiuty"   -a "/tmp/Forum-2016-01-02-Full-Backup.sql.gz" 
sendmail -f "elsa.group@gmail.com" -t "soheil_paper@yahoo.com" -m "backup" -u "communiuty"   -a "/tmp/Forum-*.sql.gz" 

mail -s "Backup" -a "/tmp/Forum-2016-01-01-Full-Backup.sql.gz" soheil_paper@yahoo.com


