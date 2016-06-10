#!/bin/sh
# Change this to the last working Libs (may be you have to try and error)

if [ ! -z $OPENSHIFT_DIY_LOG_DIR ]; then
	echo "$OPENSHIFT_LOG_DIR" > "$OPENSHIFT_HOMEDIR/.env/OPENSHIFT_DIY_LOG_DIR"
	
	nohup	OPENSHIFT_DIY_LOG_DIR2=${OPENSHIFT_LOG_DIR}   > /dev/null 2>&1
	echo $OPENSHIFT_DIY_LOG_DIR2
fi
# ========================================================
# Step 1. Download the archives.
# 1. firefox 15.0.1
# 2. java jre-7u7
# 3. flash 11.2
# ========================================================

mkdir $OPENSHIFT_HOMEDIR/app-root/runtime/srv
mkdir $OPENSHIFT_HOMEDIR/app-root/runtime/srv/phantomjs
firefox_dir=$OPENSHIFT_HOMEDIR/app-root/runtime/srv/phantomjs
mkdir $OPENSHIFT_HOMEDIR/app-root/runtime/tmp/
if [ ! -d "$OPENSHIFT_HOMEDIR/app-root/runtime/srv/phantomjs/bin" ]; then
	cd $OPENSHIFT_HOMEDIR/app-root/runtime/srv/
	git clone git://github.com/ariya/phantomjs.git
	cd phantomjs
	#./build.sh
	if [ -d "${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin" ]; then
	    ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/python build.py
	else
		python build.py
	fi
	nohup sh -c "./build.sh   --confirm "> $OPENSHIFT_LOG_DIR/phantomjs_install.log /dev/null 2>&1 &  
	bash -i -c 'tail -f  $OPENSHIFT_LOG_DIR/phantomjs_install.log'
	
	
	if [[ `lsof -n -P | grep 8080` ]];then
	  kill -9 `lsof -t -i :8080`
	  lsof -n -P | grep 8080
    fi
	#phantomjs --webdriver=8080 --webdriver-selenium-grid-hub=http://127.0.0.1:4444
	#phantomjs --webdriver=8080 --webdriver-selenium-grid-hub=http://127.2.25.131:15044
	
	export PATH=${PATH}:$OPENSHIFT_HOMEDIR/app-root/runtime/srv/phantomjs/bin/  
	cd $OPENSHIFT_HOMEDIR/app-root/runtime/srv/
	rm -rf casperjs
	git clone git://github.com/n1k0/casperjs.git
	export PATH=${PATH}:$OPENSHIFT_HOMEDIR/app-root/runtime/srv/casperjs/bin/  
	export PATH=${PATH}:$OPENSHIFT_HOMEDIR/app-root/runtime/srv/python/bin/
	#cd $OPENSHIFT_REPO_DIR   
	#  and then run your sample code in a node "session". 
	# ========================================================
	# Step 3. Create a run script.
	# ========================================================
	

fi

echo "*****************************"
echo "***  		  USAGE         ***"
echo "{firefox_dir}/rtf/run.sh http://www.adobe.com/software/flash/about/ http://javatester.org/"
#${firefox_dir}/rtf/run.sh http://www.adobe.com/software/flash/about/ http://javatester.org/
echo "*****************************"


echo "*****************************"
echo "***  F I N I S H E D !!   ***"
echo "*****************************"

cat << 'EOF' > .buildpacks
https://github.com/heroku/heroku-buildpack-ruby
https://github.com/stomita/heroku-buildpack-phantomjs
EOF
