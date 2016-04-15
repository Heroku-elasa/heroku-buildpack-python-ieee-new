#!/bin/sh
# http://www.danstraw.com/installing-selenium-server-2-as-a-service-on-ubuntu/2010/09/23/
rm -rf /tmp/*
yum install xorg-x11-server-Xvfb xorg-x11-xauth  -y
yum install firefox -y
yum update firefox
yum update xorg-x11-server-Xvfb
yum update cairo

#sudo yum install ImageMagick -y
sudo su
mkdir /usr/lib/selenium/
cd /usr/lib/selenium/
wget http://selenium-release.storage.googleapis.com/2.44/selenium-server-standalone-2.44.0.jar
mkdir -p /var/log/selenium/
chmod a+w /var/log/selenium/

nano /etc/init.d/selenium

#!/bin/bash

case "${1:-''}" in
        'start')
                if test -f /tmp/selenium.pid
                then
                        echo "Selenium is already running."
                else
                        java -jar /usr/lib/selenium/selenium-server-standalone-2.0a5.jar -port 4443 > /var/log/selenium/selenium-output.log 2> /var/log/selenium/selenium-error.log & echo $! > /tmp/selenium.pid
                        echo "Starting Selenium..."

                        error=$?
                        if test $error -gt 0
                        then
                                echo "${bon}Error $error! Couldn't start Selenium!${boff}"
                        fi
                fi
        ;;
        'stop')
                if test -f /tmp/selenium.pid
                then
                        echo "Stopping Selenium..."
                        PID=`cat /tmp/selenium.pid`
                        kill -3 $PID
                        if kill -9 $PID ;
                                then
                                        sleep 2
                                        test -f /tmp/selenium.pid && rm -f /tmp/selenium.pid
                                else
                                        echo "Selenium could not be stopped..."
                                fi
                else
                        echo "Selenium is not running."
                fi
                ;;
        'restart')
                if test -f /tmp/selenium.pid
                then
                        kill -HUP `cat /tmp/selenium.pid`
                        test -f /tmp/selenium.pid && rm -f /tmp/selenium.pid
                        sleep 1
                        java -jar /usr/lib/selenium/selenium-server-standalone-2.0a5.jar -port 4443 > /var/log/selenium/selenium-output.log 2> /var/log/selenium/selenium-error.log & echo $! > /tmp/selenium.pid
                        echo "Reload Selenium..."
                else
                        echo "Selenium isn't running..."
                fi
                ;;
        *)      # no parameter specified
                echo "Usage: $SELF start|stop|restart|reload|force-reload|status"
                exit 1
        ;;
esac

#Finally, make the script executable:

chmod 755 /etc/init.d/selenium

#To test:

 /etc/init.d/selenium start
