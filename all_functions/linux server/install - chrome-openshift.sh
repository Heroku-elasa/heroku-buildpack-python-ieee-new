#!/bin/sh
# Change this to the last working Libs (may be you have to try and error)

if [ ! -z $OPENSHIFT_DIY_LOG_DIR ]; then
    echo "$OPENSHIFT_LOG_DIR" > "$OPENSHIFT_HOMEDIR/.env/OPENSHIFT_DIY_LOG_DIR"

    nohup   OPENSHIFT_DIY_LOG_DIR2=${OPENSHIFT_LOG_DIR}   > /dev/null 2>&1
    echo $OPENSHIFT_DIY_LOG_DIR2
fi
# ========================================================
# Step 1. Download the archives.
# 1. chrome 15.0.1
# 2. java jre-7u7
# 3. flash 11.2
# ========================================================

mkdir $OPENSHIFT_HOMEDIR/app-root/runtime/srv
mkdir $OPENSHIFT_HOMEDIR/app-root/runtime/srv/chrome
chrome_dir=$OPENSHIFT_HOMEDIR/app-root/runtime/srv/chrome
mkdir $OPENSHIFT_HOMEDIR/app-root/runtime/tmp/
if [ ! -d "$OPENSHIFT_HOMEDIR/app-root/runtime/srv/chrome/bin" ]; then
    
	cd $OPENSHIFT_TMP_DIR
	rm -rf $OPENSHIFT_TMP_DIR/*
	
	
# Just stick this script somewhere and do ./get-chromium

# QUICK HACK to automate local user bleeding-edge chromium build installs

# how do you like to call this program? (chrome-linux, chrome, chromium, google-chrome?)
APPNAME="chromium"
# get the latest build number (JSON)
VERSION="wget -qO- http://build.chromium.org/f/chromium/snapshots/Linux/LATEST"
# get some extra metadata to display on the command line
LOGURL="http://build.chromium.org/f/chromium/snapshots/Linux/"$VERSION"/REVISIONS"
LOG=$(wget -qO- $LOGURL)
# build the URL of the file we'll be downloading
DOWNLOADURL="http://build.chromium.org/f/chromium/snapshots/Linux/"$VERSION"/chrome-linux.zip"


# Here's some command line output ...
echo -e "\r\n-------------------------"
echo "BUILD: "$VERSION
echo $LOGURL
echo $LOG
echo -e "-------------------------\r\n"

# if this was already downloaded, then it would either need to be deleted or aborted

# where should we put this 37MB download?
tempfile="/tmp/chrome-linux-"$VERSION".zip"
tempdir="/tmp/chrome-linux/"$VERSION
# just putting this in my home directory now because i'm lazy
permdir="~/"$APPNAME"/"$VERSION

# get the large download ...
wget $DOWNLOADURL -O $tempfile
mkdir -p $permdir
unzip $tempfile -d $permdir

	cd $OPENSHIFT_TMP_DIR
	rm -rf $OPENSHIFT_TMP_DIR/*
	cd $OPENSHIFT_HOMEDIR/app-root/runtime/srv/chrome
	wget http://chromedriver.storage.googleapis.com/2.22/chromedriver_linux64.zip
	unzip chromedriver_linux64.zip
	rm chromedriver_linux64.zip
	export PATH=${PATH}:$OPENSHIFT_HOMEDIR/app-root/runtime/srv/chrome/
	ln  -s $OPENSHIFT_HOMEDIR/app-root/runtime/srv/chrome/chromedriver /usr/bin/chromedriver
	
    # ========================================================
    # Now you can run it as shown below.
    # I added flash and java test URLs to make sure that it
    # was working.
    # ========================================================


fi

echo "*****************************"
echo "***         USAGE         ***"
echo "{chrome_dir}/rtf/run.sh http://www.adobe.com/software/flash/about/ http://javatester.org/"
${chrome_dir}/rtf/run.sh http://www.adobe.com/software/flash/about/ http://javatester.org/
echo "*****************************"

from selenium import webdriver
import os
home = os.environ['OPENSHIFT_HOMEDIR'];
ip = os.environ['OPENSHIFT_DIY_IP']
#chromedriver = home + 'app-root/runtime/srv/phantomjs/bin/phantomjs --webdriver='+ip+':15022'
chromedriver = home + '/app-root/runtime/srv/chrome/chromedriver'
os.environ["webdriver.chrome.driver"] = chromedriver

#dr = '--webdriver=8080 --webdriver-selenium-grid-hub=http://' + ip + ':15022'
dr = ' --cookies-file=/tmp/xx.txt'
#driver = webdriver.PhantomJS(executable_path=chromedriver, port=15022, service_args=dr)
driver = webdriver.Chrome(executable_path=chromedriver, port=15022, service_args=dr)
driver = webdriver.Chrome(chromedriver, port=15032)

driver = webdriver.Remote("http://"+ip+":15001",desired_capabilities=webdriver.DesiredCapabilities.HTMLUNIT)
driver = webdriver.Remote("http://"+ip+":15001/wd/hub", webdriver.DesiredCapabilities.HTMLUNITWITHJS)


echo "*****************************"
echo "***  F I N I S H E D !!   ***"
echo "*****************************"