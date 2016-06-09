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


#cd /usr/local

mkdir ~/firefox
cd /tmp
wget http://ftp.mozilla.org/pub/mozilla.org/firefox/releases/35.0/linux-x86_64/en-US/firefox-35.0.tar.bz2
tar xvjf firefox-35.0.tar.bz2 -C ~/firefox
mkdir ~/backups
cp -avr ~/.mozilla/ ~/backups
cd firefox
ln -s /home/firefox/firefox/firefox /usr/bin/firefox
export PATH=${PATH}:/home/firefox/firefox/firefox

#./firefox
mkdir $OPENSHIFT_HOMEDIR/app-root/runtime/srv
mkdir $OPENSHIFT_HOMEDIR/app-root/runtime/srv/firefox
firefox_dir=$OPENSHIFT_HOMEDIR/app-root/runtime/srv/firefox
mkdir $OPENSHIFT_HOMEDIR/app-root/runtime/tmp/
if [ ! -d "$OPENSHIFT_HOMEDIR/app-root/runtime/srv/firefox/bin" ]; then
	cd $OPENSHIFT_HOMEDIR/app-root/runtime/srv/firefox
	rm -rf *
	
	
	#wget http://firefox.googlecode.com/files/firefox-1.8.0-linux-x86_64.tar.bz2
	wget https://download-installer.cdn.mozilla.net/pub/firefox/releases/46.0/linux-x86_64/en-US/firefox-46.0.tar.bz2
	tar xf firefox-46.0.tar.bz2
	rm firefox-46.0.tar.bz2
	mv firefox-46.0/ firefox
	cd firefox
	export DISPLAY=:0.0
	./firefox -v
	
	
	git clone git://github.com/n1k0/casperjs.git
	export PATH=${PATH}:$OPENSHIFT_HOMEDIR/app-root/runtime/srv/casperjs/bin/  
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

# define path to the firefox binary
firefox = os.path.expanduser('$OPENSHIFT_HOMEDIR/app-root/runtime/srv/firefox/bin/firefox')

home=os.environ['OPENSHIFT_HOMEDIR'];path=home+'app-root/runtime/srv/firefox/bin/firefox'
url = 'http://www.scoreboard.com/game/6LeqhPJd/#game-summary'
with contextlib.closing(webdriver.PhantomJS(firefox)) as driver:
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
