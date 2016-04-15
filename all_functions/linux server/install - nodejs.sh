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
mkdir $OPENSHIFT_HOMEDIR/app-root/runtime/srv/nodejs

mkdir $OPENSHIFT_HOMEDIR/app-root/runtime/tmp/
if [ ! -d "$OPENSHIFT_HOMEDIR/app-root/runtime/srv/nodejs/bin" ]; then
	
	cd $OPENSHIFT_HOMEDIR/app-root/runtime/tmp/	
	wget http://nodejs.org/dist/v0.10.30/node-v0.10.30.tar.gz
	tar zxf node-v0.10.30.tar.gz	
	rm node-v0.10.30.tar.gz	
	cd node-v0.10.30	
	nohup sh -c "./configure --prefix=$OPENSHIFT_HOMEDIR/app-root/runtime/srv/nodejs"  > $OPENSHIFT_LOG_DIR/nodej_install_conf.log /dev/null 2>&1 &  
	tail -f $OPENSHIFT_LOG_DIR/nodej_install_conf.log
	nohup sh -c "make && make install && make clean"  > $OPENSHIFT_LOG_DIR/nodej_install.log 2>&1 &  
	tail -f $OPENSHIFT_LOG_DIR/nodej_install.log
	#nohup sh -c "make"  > $OPENSHIFT_LOG_DIR/nodej_install.log 2>&1 &  
	#tail -f $OPENSHIFT_LOG_DIR/nodej_install.log
	export PATH=${PATH}:$OPENSHIFT_HOMEDIR/app-root/runtime/srv/nodejs/bin
	node --version
	export PATH=${PATH}:$OPENSHIFT_HOMEDIR/app-root/runtime/srv/python/bin/
	export PATH=${PATH}:$OPENSHIFT_HOMEDIR/app-root/runtime/srv/phantomjs/bin/  
	
	git clone git://github.com/n1k0/casperjs.git
	export PATH=${PATH}:$OPENSHIFT_HOMEDIR/app-root/runtime/srv/casperjs/bin/ 
    $OPENSHIFT_HOMEDIR/app-root/runtime/srv/python/bin/easy_install Ghost.py	
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
cat <<'EOF'  >> phantom_example.py
import selenium.webdriver as webdriver
import contextlib
import os
import lxml.html as LH

# define path to the phantomjs binary
phantomjs = os.path.expanduser('$OPENSHIFT_HOMEDIR/app-root/runtime/srv/phantomjs/bin/phantomjs')
ip=os.environ['OPENSHIFT_DIY_IP']
import subprocess
#phantomjs --webdriver=8080 --webdriver-selenium-grid-hub=http://127.0.0.1:4444
#phantomjs --webdriver=8080 --webdriver-selenium-grid-hub=http://127.12.156.129:4444
#st='phantomjs --webdriver=8080 --webdriver-selenium-grid-hub=http://'+ip+':4444'
st='phantomjs --webdriver=8080 --webdriver-selenium-grid-hub=http://'+ip+':15023'
awk_sort = subprocess.Popen( [st ], stdin= subprocess.PIPE, stdout= subprocess.PIPE,shell=True)
awk_sort.wait()
output = awk_sort.communicate()[0]
print output.rstrip()


os.environ['PYTHON_EGG_CACHE'] 
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
