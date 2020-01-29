# Heroku IEEE paper scraper based of Python
![ss](http://s6.picofile.com/file/8386472450/Screenshot_from_2019_12_17_13_11_11.png)

# Instalation

you need to run this comand in your local pc :

```
#heroku login
#heroku bash run
cd
git clone https://github.com/Heroku-elasa/heroku-buildpack-toolbelt.git && cd heroku-buildpack-toolbelt/bin && chmod 755 compile 
./compile && export PATH=~/openshifts/app-root/runtime/srv/heroku/bin:$PATH && cd && rm -rf heroku-buildpack-toolbelt
export PATH=~/openshifts/app-root/runtime/srv/heroku/bin:$PATH
heroku

cd
mkdir rem
OPENSHIFT_HOMEDIR=/app/openshifts2/
OPENSHIFT_HOMEDIR_heroku=/app/openshifts2/openshifts
rm -rf $OPENSHIFT_HOMEDIR_heroku
rm -rf $OPENSHIFT_HOMEDIR
mkdir $OPENSHIFT_HOMEDIR
mkdir $OPENSHIFT_HOMEDIR_heroku
mkdir $OPENSHIFT_HOMEDIR_heroku/tmp
echo "https://github.com/stomita/heroku-buildpack-phantomjs.git" >> $OPENSHIFT_HOMEDIR_heroku/tmp.txt
mkdir $OPENSHIFT_HOMEDIR_heroku/logs
echo "https://github.com/stomita/heroku-buildpack-phantomjs.git" >> $OPENSHIFT_HOMEDIR_heroku/logs/logs.txt
mkdir $OPENSHIFT_HOMEDIR_heroku/app-root
mkdir $OPENSHIFT_HOMEDIR_heroku/app-root/runtime
mkdir $OPENSHIFT_HOMEDIR_heroku/app-root/runtime/srv
mkdir $OPENSHIFT_HOMEDIR_heroku/app-root/runtime/srv/tornado3
#heroku info
cd rem

git clone https://elasa:PASSWORD@gitlab.com/elasa/ieee2.git #yr_guthub_usernames=here my username is elasa and your pass
rm -rf $OPENSHIFT_HOMEDIR_heroku/app-root/runtime/srv/tornado3/*
mv ieee2/al*/* $OPENSHIFT_HOMEDIR_heroku/app-root/runtime/srv/tornado3/.
mv ieee2/*  $OPENSHIFT_HOMEDIR/. 

cd
rm -rf rem

if [ ! -d $OPENSHIFT_HOMEDIR_heroku/app-root/runtime/srv ]; then
	echo  'making $OPENSHIFT_HOMEDIR_heroku/app-root/runtime/srv'
	mkdir $OPENSHIFT_HOMEDIR_heroku/app-root/runtime/srv	
fi
if [ ! -d $OPENSHIFT_HOMEDIR_heroku/app-root/runtime/srv/cpdf ]; then
	echo "installing cpdf"
	mkdir $OPENSHIFT_HOMEDIR_heroku/app-root/runtime/srv/cpdf
	cd  $OPENSHIFT_HOMEDIR_heroku/app-root/runtime/srv/cpdf
	git clone https://github.com/coherentgraphics/cpdf-binaries.git
	mv cpdf-binaries/Linux-Intel-64bit/* .
	rm -rf cpdf-binaries
fi

cd $OPENSHIFT_HOMEDIR
git init
git add .
git config --global user.email "you@example.com"
git config --global user.name "Your Name"
export test_python_ieee='test-python-ieee3ss5'
heroku apps:destroy --app=$test_python_ieee --confirm $test_python_ieee
heroku create --stack cedar-14 --buildpack https://github.com/ddollar/heroku-buildpack-multi.git
heroku apps:rename $test_python_ieee
heroku git:remote -a $test_python_ieee
#heroku buildpacks:set https://github.com/ddollar/heroku-buildpack-multi.git

rm -rf .buildpacks
git commit -am "make it better"

rm -rf Procfile
#echo "web: python /app/openshifts/app-root/runtime/srv/tornado3/tornado-get.py  --port PORT --root '/app/openshifts/app-root/runtime/srv/tornado3/' --wtdir '/static' --ip OPENSHIFT_DIY_IP" >> Procfile
echo "web: python /app/openshifts/app-root/runtime/srv/tornado3/tornado-get.py  --port PORT --root /app/openshifts/app-root/runtime/srv/tornado3/ --wtdir '/static' --ip OPENSHIFT_DIY_IP" >> Procfile
echo "web: python /app/openshifts/app-root/runtime/srv/tornado3/tornado-get.py  --port PORT --root '/app/openshifts/app-root/runtime/srv/tornado3/' --wtdir '/static' --ip OPENSHIFT_DIY_IP"
#echo "web: python /app/all_functions/tornado-get.py  --port PORT --root '/app/all_functions/' --wtdir '/static'" >> Procfile

#echo "https://github.com/procrastinatio/heroku-buildpack-python-phantomjs" >> .buildpacks
#echo "http://github.com/srbartlett/heroku-buildpack-phantomjs-2.0.git" >> .buildpacks
echo "https://github.com/stomita/heroku-buildpack-phantomjs.git" >> .buildpacks

#echo "https://github.com/Heroku-elasa/heroku-buildpack-python.git" >> .buildpacks
#echo "https://github.com/Heroku-elasa/heroku-buildpack-python-ieee-new.git" >> .buildpacks
echo "https://github.com/Heroku-elasa/heroku-buildpack-python-ieee.git" >> .buildpacks


echo "install heroku-buildpack-toolbelt"
echo "https://github.com/futurice/heroku-buildpack-toolbelt.git" >> .buildpacks
#echo "https://github.com/heroku/heroku-buildpack-ruby.git" >> .buildpacks

echo "install nginx"
#echo "https://github.com/ryandotsmith/nginx-buildpack.git" >> .buildpacks


heroku config:add LD_LIBRARY_PATH=/usr/local/lib:/usr/lib:/lib:/app/vendor/phantomjs/lib

heroku config:add HEROKU_TOOLBELT_API_EMAIL=ss4@elec-lab.tk
heroku config:add HEROKU_TOOLBELT_API_PASSWORD=`heroku auth:PASSWORD`

#openshift added
heroku config:add OPENSHIFT_HOMEDIR=/app/openshifts
heroku config:add OPENSHIFT_LOG_DIR=/app/openshifts/logs
heroku config:add OPENSHIFT_TMP_DIR=/app/openshifts/tmp
heroku config:add OPENSHIFT_REPO_DIR=/app/openshifts
export OPENSHIFT_GEAR_DNS=$test_python_ieee.herokuapp.com
heroku config:set OPENSHIFT_GEAR_DNS=$test_python_ieee.herokuapp.com #$(heroku apps:info -s| grep "web-url" | cut -d= -f2)
#heroku config:set OPENSHIFT_GEAR_DNS=$(heroku apps:info -s| grep "web-url" | cut -d= -f2)
heroku config:set OPENSHIFT_DIY_IP='0.0.0.0'
heroku config:set NGINX_WORKERS=8


git add .
git commit -a  -m "first commit"
#git checkout -b  newbranch
git push heroku master


git clone https://github.com/power-electro/free-papers_elasa_ir_site-list.git
#$File="${OPENSHIFT_HOMEDIR}app-root/runtime/repo/free-papers_elasa_ir_site-list/openshift_freepapers_site_list.txt"
cd free-papers_elasa_ir_site-list
File="openshift_freepapers_site_list.txt"
#if grep -q $OPENSHIFT_GEAR_DNS "$File"; then
if grep -q $OPENSHIFT_GEAR_DNS "openshift_freepapers_site_list.txt"; then
	echo $OPENSHIFT_GEAR_DNS "is in file"
	else  
    echo $OPENSHIFT_GEAR_DNS  >> openshift_freepapers_site_list.txt
    echo $OPENSHIFT_GEAR_DNS "added in file"
	git config --global user.email "you@example.com"
	git config --global user.name "Your Name"
    git commit -a  -m "$OPENSHIFT_GEAR_DNS added" 
    git config remote.origin.url https://elasa:PASSWORD@github.com/your_github_repo_for_saving_free-papers_site-list.git
	#git remote add origin https://soheilpaper:PASSWORD@github.com/power-electro/free-papers_elasa_ir_site-list.git
	git push -u origin master
fi
cd ..
heroku logs -t
#heroku run bash
#vendor/phantomjs/bin/phantomjs
heroku ps:scale web=0 --app=$test_python_ieee
heroku ps:scale web=1 --app=$test_python_ieee
#heroku run bash
#export OPENSHIFT_DIY_IP='0.0.0.0'
nohup sh -c " python ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/tornado3/tornado-get.py  --port '15001' --root '${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/tornado3/' --wtdir '/static' --ip OPENSHIFT_DIY_IP" > ${OPENSHIFT_LOG_DIR}/tornado1.log /dev/null 2>&1 &
tail -f ${OPENSHIFT_LOG_DIR}/tornado1.log
nohup sh -c " python ${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/tornado3/tornado-get.py  --port PORT --root '${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/tornado3/' --wtdir '/static' --ip OPENSHIFT_DIY_IP" > tornado1.log /dev/null 2>&1 &
tail -f tornado1.log	
curl http://127.0.0.1:$PORT
curl http://127.0.0.1:15001
curl http://0.0.0.0:15002
#heroku config:set OPENSHIFT_DIY_IP='172.18.113.66'
python $OPENSHIFT_HOMEDIR/app-root/runtime/srv/tornado3/tornado-get.py  --port PORT --root $OPENSHIFT_HOMEDIR/app-root/runtime/srv/tornado3/ --wtdir '/static' --ip OPENSHIFT_DIY_IP 
 
 heroku config:set OPENSHIFT_DIY_IP='0.0.0.0'
 heroku ps:scale web=0 --app=$test_python_ieee
heroku ps:scale web=1 --app=$test_python_ieee
heroku logs -t



#heroku run python $OPENSHIFT_HOMEDIR/app-root/runtime/srv/tornado3/tornado-get.py  --port $PORT --root '${OPENSHIFT_HOMEDIR}/app-root/runtime/srv/tornado3/' --wtdir '/static' --ip OPENSHIFT_DIY_IP shell


```

# Consider in heroku pyhton seetin like this:


This is the official [Heroku buildpack](https://devcenter.heroku.com/articles/buildpacks) for Python apps, powered by [pip](https://pip.pypa.io/) and other excellent software.

Recommended web frameworks include **Django** and **Flask**. The recommended webserver is **Gunicorn**. There are no restrictions around what software can be used (as long as it's pip-installable). Web processes must bind to `$PORT`, and only the HTTP protocol is permitted for incoming connections.

Some Python packages with obscure C dependencies (e.g. scipy) are [not compatible](https://devcenter.heroku.com/articles/python-c-deps). 

See it in Action
----------------

Deploying a Python application couldn't be easier:

    $ ls
    Procfile  requirements.txt  web.py

    $ heroku create --buildpack heroku/python

    $ git push heroku master
    ...
    -----> Python app detected
    -----> Installing python-2.7.11
         $ pip install -r requirements.txt
           Collecting requests (from -r requirements.txt (line 1))
             Downloading requests-2.9.1-py2.py3-none-any.whl (501kB)
           Installing collected packages: requests
           Successfully installed requests-2.9.1
           
    -----> Discovering process types
           Procfile declares types -> (none)

A `requirements.txt` file must be present at the root of your application's repository.

You can also specify the latest production release of this buildpack for upcoming builds of an existing application:

    $ heroku buildpacks:set heroku/python





Specify a Python Runtime
------------------------

Specific versions of the Python runtime can be specified with a `runtime.txt` file:

    $ cat runtime.txt
    python-3.5.1

Runtime options include:

- `python-2.7.11`
- `python-3.5.1`
- `pypy-5.0.1` (unsupported, experimental)

Other [unsupported runtimes](https://github.com/heroku/heroku-buildpack-python/tree/master/builds/runtimes) are available as well. Use at your own risk. 



