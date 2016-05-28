mkdir ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/composer
curl -ss https://getcomposer.org/installer | php -- --install-dir=${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/composer

export PATH=${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/composer:$PATH
cd /tmp
rm -rf tt
mkdir tt
cd tt
#wget http://ftp.drupal.org/files/projects/drush-7.x-5.9.tar.gz
wget https://github.com/drush-ops/drush/archive/master.zip && unzip master.zip
rm master.zip
mv * drush
chmod u+x drush/drush

#tar xzf drush-7.x-5.9.tar.gz && rm drush-7.x-5.9.tar.gz && cd drush && mv drush drush_my
mkdir ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/
mkdir ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/drush
mv  /tmp/tt/drush/* ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/drush && cd ../..
rm -rf tt
export PATH=${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/drush:$PATH

curl -sS https://getcomposer.org/installer | php
mv composer.phar ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/composer
cd ~/app-root/runtime/repo/.openshift/action_hooks
echo "export PATH=${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/drush:$PATH
#export PATH=${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/composer:$PATH" >> ~/app-root/runtime/repo/.openshift/action_hooks/start
chmod 755 start

echo "export PATH=${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/drush:$PATH
export PATH=${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/composer:$PATH
alias drush='${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/drush/drush'
alias drush='/opt/rh/php54/root/usr/bin/php ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/drush/drush.php'" >> ~/app-root/data/.bash_profile

cd ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/drush
php -r "readfile('https://getcomposer.org/installer');" | php
mv composer.phar composer.phar0
php composer.phar0 install 
php composer.phar0 update
#composer config --global bin-dir /usr/local/bin
#composer config --global bin-dir /opt/rh/php54/root/usr/bin
composer config --global vendor-dir ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/composer
php composer install
php ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/composer/composer.phar --no-interaction --no-ansi --no-scripts  --optimize-autoloader --working-dir=${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/drush install
cd ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/drush
# Drush settings

cp drush.php drush.php0
echo "\$options['uri'] = \$_ENV['OPENSHIFT_APP_DNS'];
  \$options['root'] = \$_ENV['OPENSHIFT_REPO_DIR'].'php';" >> drush.php 
if [[ -f ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/drush/drush.php ]]; then	
	echo "$repo_top = getcwd().'/..';
  $options['config'] = $repo_top . '/drush/drushrc.php'; "
  else
	echo "<?php 
	  $repo_top = getcwd().'/..';
  $options['config'] = $repo_top . '/drush/drushrc.php'; " >> drush.php 
fi

cat << EOF >>drushrc.php
<?php 
ini_set('memory_limit', '256M');
if (array_key_exists('OPENSHIFT_APP_NAME', \$_SERVER)) {
  \$src = \$_SERVER;
} else {
  \$src = \$_ENV;
}
\$options['uri'] =\$src['OPENSHIFT_APP_DNS']; 
	   \$options['root'] =\$src['OPENSHIFT_REPO_DIR'].'php'; 
	   \$options['db-url']=\$src['OPENSHIFT_MYSQL_DB_URL'].\$src['OPENSHIFT_APP_DNS'];
	    \$options['backup-dir'] = '/tmp';
	   ?>
EOF
echo " \$options['backup-dir'] = '/tmp';">> drushrc.php
#nano drush.php 
drush status
#install mysql
: <<'end_long_comment' 
#
cd /tmp
wget http://wiki.diahosting.com/down/lnmp/mysql-5.1.46.tar.gz
nohup sh -c "./configure --prefix=${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/mysql --enable-assembler --with-charset=utf8 --enable-thread-safe-client --with-extra-charsets=all --with-big-tables &&
make && make install"> $OPENSHIFT_LOG_DIR/mysql_install.log /dev/null 2>&1 & tail -f  $OPENSHIFT_LOG_DIR/mysql_install.log

chown -R mysql:mysql ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/mysql

cp support-files/my-medium.cnf /etc/my.cnf

sed -i 's#\[mysqld\]#\[mysqld\]\nbasedir=/usr/local/mysql\ndatadir=/var/lib/mysql\n#' /etc/my.cnf
sed -i 's#log-bin=mysql-bin#\#log-bin=mysql-bin#' /etc/my.cnf
sed -i 's#binlog_format=mixed#\#binlog_format=mixed#' /etc/my.cnf

${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/mysql/bin/mysql_install_db --basedir=${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/mysql  --datadir=/var/lib/mysql --user=mysql

cp ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/mysql/share/mysql/mysql.server /etc/init.d/mysqld
chmod 755 /etc/init.d/mysqld

/etc/init.d/mysqld start

${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/mysql/bin/mysqladmin -u root password $myrootpwd

chkconfig mysqld on

#ln -s ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/mysql/bin/myisamchk /usr/bin/
#ln -s ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/mysql/bin/mysql /usr/bin/
#ln -s ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/mysql/bin/mysqldump /usr/bin/


end_long_comment
cd
export pass=$OPENSHIFT_MYSQL_DB_PASSWORD
export user=$OPENSHIFT_MYSQL_DB_USERNAME
mysql -u $OPENSHIFT_MYSQL_DB_USERNAME 
DROP DATABASE drupal2;
CREATE DATABASE drupal2;
#CREATE USER druser@localhost;
#CREATE USER druser2@$OPENSHIFT_MYSQL_DB_HOST;
CREATE USER 'druser'@'$OPENSHIFT_MYSQL_DB_HOST' IDENTIFIED BY 'druser';
#CREATE USER 'juddi'@'$OPENSHIFT_MYSQL_DB_HOST' IDENTIFIED BY 'juddi';
#SET PASSWORD FOR druser@localhost= PASSWORD("password");
SET PASSWORD FOR 'druser'@$OPENSHIFT_MYSQL_DB_HOST= PASSWORD("password");
#GRANT ALL PRIVILEGES ON drupal2.* TO druser@localhost IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON drupal2.* TO $user@$OPENSHIFT_MYSQL_DB_HOST IDENTIFIED BY $pass;
#GRANT ALL PRIVILEGES ON drupal.* TO $OPENSHIFT_MYSQL_DB_USERNAME@$OPENSHIFT_MYSQL_DB_HOST  IDENTIFIED BY $OPENSHIFT_MYSQL_DB_PASSWORD;
FLUSH PRIVILEGES;
cd ${OPENSHIFT_HOMEDIR}/app-root/runtime/repo/php
	chmod  755 . -R
	rm -rf *
if [[ 1=2 ]];then
	drush dl openpublic #--drupal-project-rename=folder_name
	mv open*/* ./
	cd pro*/openpu*
	drush make --prepare-install build-openpublic.make openpublic
rm -rf ~/app-root/data/sites/default/settings.php
fi
echo " \$options['backup-dir'] = '/tmp';">> ~/.drush/drushrc.php
cd ${OPENSHIFT_HOMEDIR}/app-root/runtime/repo/php
nohup sh -c "export PATH=${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/drush:$PATH && drush dl openpublic"> $OPENSHIFT_LOG_DIR/drush_site_install_1_1.log /dev/null 2>&1 &  
tail -f  $OPENSHIFT_LOG_DIR/drush_site_install_1_1.log
cd ${OPENSHIFT_HOMEDIR}/app-root/runtime/repo/php && mv */* './' && cd pro*/openpu* 
nohup sh -c "export PATH=${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/drush:$PATH  && drush make --prepare-install build-openpublic.make openpublic &&\
 cd ${OPENSHIFT_HOMEDIR}/app-root/runtime/repo/php &&\
 drush site-install openpublic --db-url=mysql://$OPENSHIFT_MYSQL_DB_USERNAME:$OPENSHIFT_MYSQL_DB_PASSWORD@$OPENSHIFT_MYSQL_DB_HOST:$OPENSHIFT_MYSQL_DB_PORT/drupal2 --site-name=${OPENSHIFT_APP_NAME}  --account-name='ss' --account-pass='ss' --yes"> $OPENSHIFT_LOG_DIR/drush_site_install_1_2.log /dev/null 2>&1 &  
tail -f  $OPENSHIFT_LOG_DIR/drush_site_install_1_2.log
#drush site-install weebpal --db-url=mysql://$OPENSHIFT_MYSQL_DB_USERNAME:$OPENSHIFT_MYSQL_DB_PASSWORD@$OPENSHIFT_MYSQL_DB_HOST:$OPENSHIFT_MYSQL_DB_PORT/$OPENSHIFT_APP_NAME  --site-name=${OPENSHIFT_APP_NAME}  --account-name='ss' --account-pass='ss'  --account-mail='ss3@elec-lab.tk' --site-mail='ss3@elec-lab.tk' --yes 
#nohup sh -c "drush site-install themebrain_profile --db-url=mysql://$OPENSHIFT_MYSQL_DB_USERNAME:$OPENSHIFT_MYSQL_DB_PASSWORD@$OPENSHIFT_MYSQL_DB_HOST:$OPENSHIFT_MYSQL_DB_PORT/drupal2 --site-name=${OPENSHIFT_APP_NAME}  --account-name='ss' --account-pass='ss'  --account-mail='ss3@elec-lab.tk' --site-mail='ss3@elec-lab.tk' --yes ">$OPENSHIFT_LOG_DIR/drush_site_install_1_2.log /dev/null 2>&1 &  tail -f  $OPENSHIFT_LOG_DIR/drush_site_install_1_2.log  
#drush site-install opendeals --db-url=mysql://$OPENSHIFT_MYSQL_DB_USERNAME:$OPENSHIFT_MYSQL_DB_PASSWORD@$OPENSHIFT_MYSQL_DB_HOST:$OPENSHIFT_MYSQL_DB_PORT/$OPENSHIFT_APP_NAME --site-name=${OPENSHIFT_APP_NAME}  --account-name='ss' --account-pass='ss'  --account-mail=ss3@elec-lab.tk --yes

#drush site-install openpublic --db-url=mysql://druser:password@$OPENSHIFT_MYSQL_DB_HOST:$OPENSHIFT_MYSQL_DB_PORT/drupal2 --site-name=${OPENSHIFT_APP_NAME}  --account-name='ss' --account-pass='ss' --yes

#drush site-install openpublic --site-name=${OPENSHIFT_APP_NAME} --account-pass=$admin_pwd --db-url=mysql://$OPENSHIFT_MYSQL_DB_USERNAME:$OPENSHIFT_MYSQL_DB_PASSWORD@$OPENSHIFT_MYSQL_DB_HOST:$OPENSHIFT_MYSQL_DB_PORT/$OPENSHIFT_APP_NAME --yes
#mysql -u $OPENSHIFT_MYSQL_DB_USERNAME  -h $OPENSHIFT_MYSQL_DB_HOST drupal <

########DONE ##################

echo " \$options['backup-dir'] = '/tmp';">> ~/.drush/drushrc.php
### drush backup database###
drush sql-dump > /tmp/database-backup.sql
### drush restore database###
mysqldump -u $OPENSHIFT_MYSQL_DB_USERNAME:$OPENSHIFT_MYSQL_DB_PORT  $OPENSHIFT_APP_NAME < database-backup.sql
mysqldump -u USERNAME -p'PASSWORD' DATABASENAME > /path/to/backup_dir/database-backup.sql
drush sql-cli < ~/my-sql-dump-file-name.sql
drush bam-backup


####################################
nohup sh -c " wget  -P ${OPENSHIFT_HOMEDIR}/app-root/runtime/repo/php --mirror --user=u220290147 --password=ss123456 ftp://93.188.160.83:21/"> $OPENSHIFT_LOG_DIR/python_modules_install_1_1.log /dev/null 2>&1 &  
tail -f  $OPENSHIFT_LOG_DIR/python_modules_install_1_1.log
cd ${OPENSHIFT_HOMEDIR}/app-root/runtime/repo/php/*
nohup sh -c "zip -r elec-lab.zip . "> $OPENSHIFT_LOG_DIR/zip.log /dev/null 2>&1 &  
tail -f  $OPENSHIFT_LOG_DIR/zip.log

/tmp/tmp/tb/sites/all/modules

~/app-root/data/sites/all/modules
mkdir ~/app-root/data/sites/all/libraries
mv -n /tmp/tmp/tb/sites/all/libraries/*  ~/app-root/data/sites/all/libraries
mkdir ~/app-root/data/sites/all/themes
mv -n /tmp/tmp/tb/sites/all/themes/*  ~/app-root/data/sites/all/themes
mv -n /tmp/tmp/tb/sites/all/*  ~/app-root/data/sites/all/
mv -n /tmp/tmp/tb/sites/*  ~/app-root/data/sites/
mv -n /tmp/tmp/tb/sites/all/modules/*  ~/app-root/data/sites/all/modules
mkdir ~/app-root/data/downloads/drupal-7.34/profiles/themebrain_profile
mv -n /tmp/tmp/tb/profiles/themebrain_profile/*  ~/app-root/data/downloads/drupal-7.34/profiles/themebrain_profile

mv ~/app-root/runtime/repo/.openshift/install_profiles/standard ~/app-root/runtime/repo/.openshift/install_profiles/standard1
mkdir ~/app-root/runtime/repo/.openshift/install_profiles/standard
mv -n /tmp/op/openpublic-7.x-1.x-dev/profiles/openpublic/* ~/app-root/runtime/repo/.openshift/install_profiles/standard
chmod 755 ~/app-root/data/sites/default/settings.php
rm -rf ~/app-root/data/sites/default/settings.php

chmod 755 ~/app-root/runtime/repo/.openshift/action_hooks/deploy
nohup sh -c "./app-root/runtime/repo/.openshift/action_hooks/deploy "> $OPENSHIFT_LOG_DIR/deploy.log /dev/null 2>&1 &  tail -f  $OPENSHIFT_LOG_DIR/deploy.log  
#tail -f  $OPENSHIFT_LOG_DIR/deploy.log

#nohup sh -c "wget http://dl1.sarzamindownload.com/sdlftpuser/92/07/10/Android.Bootcamp_Part2.rar "> $OPENSHIFT_LOG_DIR/zip2.log /dev/null 2>&1 &  
#tail -f  $OPENSHIFT_LOG_DIR/zip2.log
rm drush_download.py
cat <<'EOF'  >> drush_download.py

import subprocess
import ast
st1='"Nodeblock, Follow, Securepages, Addthis, Twitter_pull, Comment_notify, Context_field, Entity_autocomplete, Views_boxes, Delta, Delta_ui, Context_condition_admin_theme, Context_breadcrumb_current_page, Context_bool_field, Nodeconnect, Openpublic_splash, Phase2_profile, Openpublic_breaking_news, Openpublic_comments, Openpublic_base_fields, Openpublic_defaults, Openpublic_home_page_feature, Openpublic_most_popular, Openpublic_person, Openpublic_person_leadership, Openpublic_site_page, Openpublic_webform, Openpublic_editors_choice, Openpublic_captcha, Openpublic_media_room, Openpublic_menu, Openpublic_menu_utility, Openpublic_menu_footer, Openpublic_pages, Openpublic_accessibility, Openpublic_filters, Openpublic_comments_default, Openpublic_webform_defaults"'
st1='"Addthis, Openpublic_splash, Phase2_profile, Openpublic_breaking_news, Openpublic_comments, Openpublic_base_fields, Openpublic_defaults, Openpublic_home_page_feature, Openpublic_most_popular, Openpublic_person, Openpublic_person_leadership, Openpublic_site_page, Openpublic_webform, Openpublic_editors_choice, Openpublic_captcha, Openpublic_media_room, Openpublic_menu, Openpublic_menu_utility, Openpublic_menu_footer, Openpublic_pages, Openpublic_accessibility, Openpublic_filters, Openpublic_comments_default, Openpublic_webform_defaults"'
st1=st1.lower()
st1=st1.replace(',',"','").replace('"',"'")
st2='"['+st1+']"';st2=st2.replace('"','')

ss=ast.literal_eval(st2)
#print ss

print st
for module in ss:
	try:
		st='drush dl '+module+' -Y ';print st
		awk_sort = subprocess.Popen( [st ], stdin= subprocess.PIPE, stdout= subprocess.PIPE,shell=True)
		awk_sort.wait()
		output = awk_sort.communicate()[0]
		print output.rstrip()
	except:
		print 'module '+module+' could not bin installed !!!'
#print "END"
EOF
#python drush_download.py
 drush site-install standard --site-name=${OPENSHIFT_APP_NAME} --account-pass=$admin_pwd --db-url=mysql://$OPENSHIFT_MYSQL_DB_USERNAME:$OPENSHIFT_MYSQL_DB_PASSWORD@$OPENSHIFT_MYSQL_DB_HOST:$OPENSHIFT_MYSQL_DB_PORT/$OPENSHIFT_APP_NAME --yes
nohup sh -c "python drush_download.py"> $OPENSHIFT_LOG_DIR/drush_download.log /dev/null 2>&1 &  
tail -f  $OPENSHIFT_LOG_DIR/drush_download.log

#nohup sh -c "zip  -rT9 ferdowsi-elec-labs_tk.zip '${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/tmp/.'"> $OPENSHIFT_LOG_DIR/python_ftp_sync_download.log /dev/null 2>&1 &  
#nohup sh -c "cd ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/tmp/ && zip  -rT9 ferdowsi-elec-labs_tk.zip ."> $OPENSHIFT_LOG_DIR/python_ftp_sync_download.log /dev/null 2>&1 &  
#tail -f  $OPENSHIFT_LOG_DIR/python_ftp_sync_download.log
