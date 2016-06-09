#!/bin/sh
# Change this to the last working Libs (may be you have to try and error)

if [ ! -z $OPENSHIFT_DIY_LOG_DIR ]; then
    echo "$OPENSHIFT_LOG_DIR" > "$OPENSHIFT_HOMEDIR/.env/OPENSHIFT_DIY_LOG_DIR"

    nohup   OPENSHIFT_DIY_LOG_DIR2=${OPENSHIFT_LOG_DIR}   > /dev/null 2>&1
    echo $OPENSHIFT_DIY_LOG_DIR2
fi
# ========================================================
# Step 1. Download the archives.
# 1. firefox 15.0.1
# 2. java jre-7u7
# 3. flash 11.2
# ========================================================

mkdir $OPENSHIFT_HOMEDIR/app-root/runtime/srv
mkdir $OPENSHIFT_HOMEDIR/app-root/runtime/srv/firefox
firefox_dir=$OPENSHIFT_HOMEDIR/app-root/runtime/srv/firefox
mkdir $OPENSHIFT_HOMEDIR/app-root/runtime/tmp/
if [ ! -d "$OPENSHIFT_HOMEDIR/app-root/runtime/srv/siege/bin" ]; then
    
	cd $OPENSHIFT_HOMEDIR/app-root/runtime/tmp/
	wget ftp://ftp.x.org/pub/X10R3/X.V10R3.tar.gz
	tar zxf X.V10R3.tar.gz
	cd X.V10R3
	make
	wget http://selenium.googlecode.com/files/selenium-server-standalone-2.0b3.jar
	#DISPLAY=:1 xvfb-run java -jar selenium-server-standalone-2.0b3.jar
	export DISPLAY=:0.0
	$OPENSHIFT_HOMEDIR/app-root/runtime/srv/java/bin/java -jar selenium-server-standalone-2.0b3.jar 
	rm selenium-server-standalone-2.0b3.jar
    cd $OPENSHIFT_HOMEDIR/app-root/runtime/srv/firefox
	mkdir repo
    pushd repo
    wget http://releases.mozilla.org/pub/mozilla.org/firefox/releases/15.0.1/linux-x86_64/en-US/firefox-15.0.1.tar.bz2
    wget javadl.sun.com/webapps/download/AutoDL?BundleId=68236 -O jre-7u7-linux-x64.tar.gz
    #wget http://fpdownload.macromedia.com/get/flashplayer/pdc/11.2.202.238/install_flash_player_11_linux.x86_64.tar.gz
    wget ftp://priede.bf.lu.lv/pub/MultiVide/MacroMedia/x64/install_flash_player_11_linux.x86_64.tar.gz
    popd
    # ========================================================
    # Step 2. Install in the rtf (release-to-field) directory.
    # ========================================================
    mkdir rtf
    pushd rtf
    tar jxf ../repo/firefox-15.0.1.tar.bz2
    tar zxf ../repo/jre-7u7-linux-x64.tar.gz
    mkdir -p firefox/plugins
    pushd firefox/plugins
	firefox_dir=$OPENSHIFT_HOMEDIR/app-root/runtime/srv/firefox
    tar zxf ${firefox_dir}/repo/install_flash_player_11_linux.x86_64.tar.gz

    # This installs the java plugin.
    ln -s ${firefox_dir}/rtf/jre1.7.0_07/lib/amd64/libnpjp2.so .
    popd
    popd
    # ========================================================
    # Step 3. Create a run script.
    # ========================================================
cat >rtf/run.sh <<EOF
#!/bin/bash
#export DISPLAY=:0.0
export DISPLAY=:0
MYARGS="\$*"
export PATH="${firefox_dir}/rtf/firefox:$rtfdir/jre1.7.0_07/bin:\${PATH}"
export CLASSPATH="${firefox_dir}/rtf/jre1.7.0_07/lib:\${CLASSPATH}"
firefox \$MYARGS
EOF
    chmod a+x rtf/run.sh

    # ========================================================
    # Now you can run it as shown below.
    # I added flash and java test URLs to make sure that it
    # was working.
    # ========================================================


fi

echo "*****************************"
echo "***         USAGE         ***"
echo "{firefox_dir}/rtf/run.sh http://www.adobe.com/software/flash/about/ http://javatester.org/"
${firefox_dir}/rtf/run.sh http://www.adobe.com/software/flash/about/ http://javatester.org/
echo "*****************************"


echo "*****************************"
echo "***  F I N I S H E D !!   ***"
echo "*****************************"