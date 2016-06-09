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
mkdir $OPENSHIFT_HOMEDIR/app-root/runtime/tmp/
mkdir  $OPENSHIFT_HOMEDIR/app-root/runtime/srv/java

if [ ! -d ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/java/bin ]; then
	cd $OPENSHIFT_HOMEDIR/app-root/runtime/srv/java
	wget --no-check-certificate --no-cookies --header "Cookie: oraclelicense=accept-securebackup-cookie" http://download.oracle.com/otn-pub/java/jdk/7u55-b13/jdk-7u55-linux-x64.tar.gz
	tar -zxf jdk-7u55-linux-x64.tar.gz
	rm jdk-7u55-linux-x64.tar.gz
	mv jdk1.7.0_55/* .
	rm -rf jdk1.7.0_55
	#update-alternatives --install /usr/bin/java java $OPENSHIFT_HOMEDIR/app-root/runtime/srv/java/bin/java 100  
	#update-alternatives --config java
	#wget http://www.java.net/download/jdk7u40/archive/b40/binaries/jdk-7u40-fcs-bin-b40-linux-x64-16_aug_2013.tar.gz
	export PATH=${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/java/bin:$PATH
	export JAVA_HOME="${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/java"
	export JRE_HOME="${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/java/jre"
fi

if [ ! -d "$OPENSHIFT_HOMEDIR/app-root/runtime/srv/phantomjs/bin" ]; then
	cd $OPENSHIFT_HOMEDIR/app-root/runtime/srv/phantomjs
	rm -rf *
	
	
	#wget http://phantomjs.googlecode.com/files/phantomjs-1.8.0-linux-x86_64.tar.bz2
	#wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-1.9.8-linux-x86_64.tar.bz2
	wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2
	tar xf phantomjs-2.1.1-linux-x86_64.tar.bz2
	rm phantomjs-2.1.1-linux-x86_64.tar.bz2
	mv phantomjs-2.1.1-linux-x86_64/* .
	rm phantomjs-2.1.1-linux-x86_64
	./bin/phantomjs -v
	export PATH=${PATH}:$OPENSHIFT_HOMEDIR/app-root/runtime/srv/phantomjs/bin/  
	
	$OPENSHIFT_HOMEDIR/app-root/runtime/srv/phantomjs/bin/phantomjs --webdriver='${OPENSHIFT_DIY_IP}:15052'
	$OPENSHIFT_HOMEDIR/app-root/runtime/srv/phantomjs/bin/phantomjs --webdriver=8080 --webdriver-selenium-grid-hub='http://${OPENSHIFT_DIY_IP}:15052'
	
	
	#phantom for openshift gooooooooooooooooood  working
	cd $OPENSHIFT_HOMEDIR/app-root/runtime/srv/phantomjs
	rm -rf *
	git clone https://github.com/hienchu/openshift-cartridge-phantomjs.git
	mv openshift-cartridge-phantomjs/* .
	port='8080'
	kill -9 `lsof -t -i :$port`
	phantomjs_app=$OPENSHIFT_HOMEDIR/app-root/runtime/srv/phantomjs/usr/template/server.js
	mkdir $OPENSHIFT_HOMEDIR/app-root/runtime/srv/phantomjs/bin/
	cp  $OPENSHIFT_HOMEDIR/app-root/runtime/srv/phantomjs/versions/1.9/bin/phantomjs $OPENSHIFT_HOMEDIR/app-root/runtime/srv/phantomjs/bin/.
	export PATH=${PATH}:$OPENSHIFT_HOMEDIR/app-root/runtime/srv/phantomjs/bin/  
	nohup sh -c "$OPENSHIFT_HOMEDIR/app-root/runtime/srv/phantomjs/versions/1.9/bin/phantomjs  $phantomjs_app $OPENSHIFT_DIY_IP $port "> ${OPENSHIFT_LOG_DIR}/tornado1.log /dev/null 2>&1 &
	#tail -f ${OPENSHIFT_LOG_DIR}/tornado1.log
	phantomjs --webdriver=$OPENSHIFT_DIY_IP:15052
	
	
	#ghost driver fixed
	cd $OPENSHIFT_HOMEDIR/app-root/runtime/srv/phantomjs
	rm -rf *
	git clone https://github.com/darwin10/phantomjs.git
	mv phantomjs/* .
	nohup sh -c "./build.sh  --confirm">${OPENSHIFT_LOG_DIR}/phantomjs2.log /dev/null 2>&1 &
	#tail -f ${OPENSHIFT_LOG_DIR}/phantomjs2.log
	
	./bin/phantomjs -v
	export PATH=${PATH}:$OPENSHIFT_HOMEDIR/app-root/runtime/srv/phantomjs/bin/  
	
	#ghost driver fixed new 
	mkdir $OPENSHIFT_HOMEDIR/app-root/runtime/srv/phantomjs
	cd $OPENSHIFT_HOMEDIR/app-root/runtime/srv/phantomjs
	rm -rf *
	git clone https://github.com/power-electro/phantomjs-ghostdriver.git
	mv phantomjs-ghostdriver/* .
	rm -rf phantomjs-ghostdriver
	nohup sh -c "./build.sh  --confirm">${OPENSHIFT_LOG_DIR}/phantomjs2.log /dev/null 2>&1 &
	#tail -f ${OPENSHIFT_LOG_DIR}/phantomjs2.log
	
	
	#ghost driver fixed new  ariya
	mkdir $OPENSHIFT_HOMEDIR/app-root/runtime/srv/phantomjs/qt
	cd $OPENSHIFT_HOMEDIR/app-root/runtime/srv/phantomjs
	rm -rf *
	git clone https://github.com/ariya/phantomjs.git
	mv phantomjs/* .
	rm -rf phantomjs
	mv  $OPENSHIFT_TMP_DIR/phantomjs-ghostdriver/src/qt/* $OPENSHIFT_HOMEDIR/app-root/runtime/srv/phantomjs/src/qt/
	cd $OPENSHIFT_HOMEDIR/app-root/runtime/srv/phantomjs/src/qt/
	git clone https://github.com/Vitallium/qtbase.git
	#git clone https://github.com/Vitallium/qtwebkit.git
	#git clone https://github.com/Vitallium/phantomjs-3rdparty-win.git
	
	cd qtbase && rm -rf .git && rm -rf .gitignore 
	cd ..
	cd qtwebkit && rm -rf .git  && rm -rf .gitignore
	cd ..
	mv phantomjs-3rdparty-win/*  3rdparty/. && rm -rf phantomjs-3rdparty-win
	cd 3rdparty && rm -rf .git  && rm -rf .gitignore
	cd ..
	cd $OPENSHIFT_HOMEDIR/app-root/runtime/srv/phantomjs
	rm -rf *
	
	cd $OPENSHIFT_HOMEDIR/app-root/runtime/srv/phantomjs
	#cp -rf  $OPENSHIFT_TMP_DIR/phantomjs-ghostdriver/src/qt/* $OPENSHIFT_HOMEDIR/app-root/runtime/srv/phantomjs/src/qt/qtbase/.
	export PATH=${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin:${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/lib/python2.7:$PATH
	${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/python build.py --qmake-args " -prefix $OPENSHIFT_HOMEDIR/app-root/runtime/srv/phantomjs/qt " --confirm
	#python build.py --confirm
	nohup sh -c "python build.py  --confirm ">${OPENSHIFT_LOG_DIR}/phantomjs2.log /dev/null 2>&1 &
	#tail -f ${OPENSHIFT_LOG_DIR}/phantomjs2.log
	du --max-depth=0 ${OPENSHIFT_HOMEDIR}app-root/runtime/srv/phantomjs
	
	./bin/phantomjs -v
	export PATH=${PATH}:$OPENSHIFT_HOMEDIR/app-root/runtime/srv/phantomjs/bin/  
	
	
	$OPENSHIFT_HOMEDIR/app-root/runtime/srv/phantomjs/bin/phantomjs --webdriver='${OPENSHIFT_DIY_IP}:15052'
	$OPENSHIFT_HOMEDIR/app-root/runtime/srv/phantomjs/bin/phantomjs --webdriver=8080 --webdriver-selenium-grid-hub='http://${OPENSHIFT_DIY_IP}:15052'
	
	
	
	cd $OPENSHIFT_TMP_DIR
	rm -rf *
	mkdir  $OPENSHIFT_HOMEDIR/app-root/runtime/srv/ghostdriver
	cd $OPENSHIFT_HOMEDIR/app-root/runtime/srv/ghostdriver
	rm -rf *
	git clone https://github.com/detro/ghostdriver.git
	mv ghostdriver/* .
	rm -rf ghostdriver
	export PATH=${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/ghostdriver/src:$PATH
	
	#wget http://selenium.googlecode.com/files/selenium-server-standalone-2.40.0.jar
	wget https://selenium-release.storage.googleapis.com/2.52/selenium-server-standalone-2.52.0.jar
	
	$OPENSHIFT_HOMEDIR/app-root/runtime/srv/java/bin/java -jar selenium-server-standalone-2.52.0.jar -role hub
	$OPENSHIFT_HOMEDIR/app-root/runtime/srv/phantomjs/bin/phantomjs --webdriver=8080 --webdriver-selenium-grid-hub='http://${OPENSHIFT_DIY_IP}:15052'
	
	$OPENSHIFT_HOMEDIR/app-root/runtime/srv/java/bin/java -jar selenium-server-standalone-2.52.0.jar -role node -hub http://${OPENSHIFT_DIY_IP}:15006 # -port 15011 -host ${OPENSHIFT_DIY_IP}
	$OPENSHIFT_HOMEDIR/app-root/runtime/srv/java/bin/java -jar selenium-server-standalone-2.52.0.jar -role node  -port 15011 -host ${OPENSHIFT_DIY_IP} #-hub http://${OPENSHIFT_DIY_IP}:15010  #
	$OPENSHIFT_HOMEDIR/app-root/runtime/srv/java/bin/java -jar selenium-server-standalone-2.52.0.jar;htmlunit-driver-standalone-2.21.jar org.openqa.grid.selenium.GridL
	rm selenium-server-standalone-2.0b3.jar
	
	cd $OPENSHIFT_TMP_DIR
	rm -rf *
	#git clone https://github.com/SeleniumHQ/selenium.git 
	#cd selenium
	#${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/python/bin/python setup.py install
	
	$OPENSHIFT_HOMEDIR/app-root/runtime/srv/phantomjs/bin/phantomjs --webdriver='${OPENSHIFT_DIY_IP}:15052'
	$OPENSHIFT_HOMEDIR/app-root/runtime/srv/phantomjs/bin/phantomjs --webdriver=8080 --webdriver-selenium-grid-hub='http://${OPENSHIFT_DIY_IP}:15052'
	
	
	mkdir $OPENSHIFT_HOMEDIR/app-root/runtime/srv/casperjs
	cd $OPENSHIFT_HOMEDIR/app-root/runtime/srv/casperjs
	
	git clone git://github.com/n1k0/casperjs.git
	mv casperjs/* .
	rm -rf casperjs
	export PATH=${PATH}:$OPENSHIFT_HOMEDIR/app-root/runtime/srv/casperjs/bin/
	export PATH=${PATH}:$OPENSHIFT_HOMEDIR/app-root/runtime/srv/phantomjs/bin/  
	casperjs
	
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

cd $OPENSHIFT_TMP_DIR
cat <<'EOF'  >> googlelinks.js
var links = [];
var casper = require('casper').create();

function getLinks() {
    var links = document.querySelectorAll('h3.r a');
    return Array.prototype.map.call(links, function(e) {
        return e.getAttribute('href');
    });
}

casper.start('http://google.fr/', function() {
    // search for 'casperjs' from google form
    this.fill('form[action="/search"]', { q: 'casperjs' }, true);
});

casper.then(function() {
    // aggregate results for the 'casperjs' search
    links = this.evaluate(getLinks);
    // now search for 'phantomjs' by filling the form again
    this.fill('form[action="/search"]', { q: 'phantomjs' }, true);
});

casper.then(function() {
    // aggregate results for the 'phantomjs' search
    links = links.concat(this.evaluate(getLinks));
});

casper.run(function() {
    // echo results in some pretty fashion
    this.echo(links.length + ' links found:');
    this.echo(' - ' + links.join('\n - ')).exit();
});
EOF
$OPENSHIFT_HOMEDIR/app-root/runtime/srv/casperjs/bin/casperjs googlelinks.js

$OPENSHIFT_HOMEDIR/app-root/runtime/srv/python/bin/python
from selenium import webdriver
import os
home = os.environ['OPENSHIFT_HOMEDIR'];
ip = os.environ['OPENSHIFT_DIY_IP']
#chromedriver = home + 'app-root/runtime/srv/phantomjs/bin/phantomjs'# +' --webdriver='+ip+':15010'
chromedriver = home + '/app-root/runtime/srv/chrome/chromedriver'
os.environ["webdriver.chrome.driver"] = chromedriver

#dr = '--webdriver=8080 --webdriver-selenium-grid-hub=http://' + ip + ':15010'
dr = ' --cookies-file=/tmp/xx.txt'
#driver = webdriver.PhantomJS(executable_path=chromedriver, port=15010, service_args=dr)
driver = webdriver.Chrome(executable_path=chromedriver, port=15010, service_args=dr)
driver = webdriver.Chrome(chromedriver, port=15010)

driver = webdriver.Remote("http://"+ip+":15010",desired_capabilities=webdriver.DesiredCapabilities.HTMLUNIT)
driver = webdriver.Remote("http://"+ip+":15010/wd/hub", webdriver.DesiredCapabilities.HTMLUNITWITHJS)

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
path = home + 'app-root/runtime/srv/phantomjs/bin/phantomjs'
desired_capabilities = DesiredCapabilities.PHANTOMJS
desired_capabilities['phantomjs.ghostdriver.path'] = home+'app-root/runtime/srv/ghostdriver/src/main.js'
driver = webdriver.PhantomJS(executable_path=path, port=15010,desired_capabilities=desired_capabilities)
		
echo "*****************************"
echo "***  F I N I S H E D !!   ***"
echo "*****************************"
