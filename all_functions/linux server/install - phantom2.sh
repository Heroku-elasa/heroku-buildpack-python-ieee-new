#!/bin/sh
# Change this to the last working Libs (may be you have to try and error)
#https://blog.openshift.com/screen-scraper-as-a-service/

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
	cd $OPENSHIFT_HOMEDIR/app-root/runtime/srv/phantomjs
	rm -rf *
	
	
	#wget http://phantomjs.googlecode.com/files/phantomjs-1.8.0-linux-x86_64.tar.bz2
	wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-1.9.8-linux-x86_64.tar.bz2
	tar xf phantomjs-1.9.8-linux-x86_64.tar.bz2
	rm phantomjs-1.9.8-linux-x86_64.tar.bz2
	mv phantomjs-1.9.8-linux-x86_64/ phantomjs
	cd phantomjs
	mv * ..
	rm -rf phantomjs
	./bin/phantomjs -v
	
	export PATH=${PATH}:$OPENSHIFT_HOMEDIR/app-root/runtime/srv/phantomjs/bin/  

	git clone git://github.com/n1k0/casperjs.git
	export PATH=${PATH}:$OPENSHIFT_HOMEDIR/app-root/runtime/srv/casperjs/bin/  
	#cd $OPENSHIFT_REPO_DIR   
	#  and then run your sample code in a node "session". 
	# ========================================================
	# Step 3. Create a run script.
	# ========================================================
	

fi
if [[ `lsof -n -P | grep 8080` ]];then
	  kill -9 `lsof -t -i :8080`
	  lsof -n -P | grep 8080
    fi

	#$OPENSHIFT_HOMEDIR/app-root/runtime/srv/phantomjs/bin/phantomjs --webdriver=8080 --webdriver-selenium-grid-hub=http://127.0.0.1:4444
	#$OPENSHIFT_HOMEDIR/app-root/runtime/srv/phantomjs/bin/phantomjs --webdriver=$OPENSHIFT_DIY_IP:8080 --webdriver-selenium-grid-hub=http://$OPENSHIFT_DIY_IP:15044
	
	
echo "*****************************"
echo "***  		  USAGE         ***"
echo "{firefox_dir}/rtf/run.sh http://www.adobe.com/software/flash/about/ http://javatester.org/"
#${firefox_dir}/rtf/run.sh http://www.adobe.com/software/flash/about/ http://javatester.org/
echo "*****************************"
cat <<'EOF'  >> phantom_example.py
import selenium.webdriver as webdriver
import contextlib
import os
import lxml.html as LH

# define path to the phantomjs binary
phantomjs = os.path.expanduser('$OPENSHIFT_HOMEDIR/app-root/runtime/srv/phantomjs/bin/phantomjs')

home=os.environ['OPENSHIFT_HOMEDIR'];path=home+'app-root/runtime/srv/phantomjs/bin/phantomjs'
url = 'http://www.scoreboard.com/game/6LeqhPJd/#game-summary'
with contextlib.closing(webdriver.PhantomJS(phantomjs)) as driver:
    driver.get(url)
    content = driver.page_source
    doc = LH.fromstring(content)   
    result = []
    for tr in doc.xpath('//tr[td[@class="left summary-horizontal"]]'):
        row = []
        for elt in tr.xpath('td'):
            row.append(elt.text_content())
        result.append(u', '.join(row[1:]))
    print(u'\n'.join(result))
EOF

echo "*****************************"
echo "***  F I N I S H E D !!   ***"
echo "*****************************"
