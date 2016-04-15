SERVICE=$OPENSHIFT_HOMEDIR/app-root/runtime/srv/siege/bin/siege
result=$(ps ax|grep -v grep|grep $SERVICE)
echo ${#result}
if  ${#result}> 0 
then
        echo " Working!"
else
        echo "Not Working.....Restarting"
        /usr/bin/xvfb-run -a /opt/python27/bin/python2.7 SERVICE &
fi

top -b -n1 | mail -s 'Process snapshot' soheil.power@gmail.com

 ps ax | grep siege