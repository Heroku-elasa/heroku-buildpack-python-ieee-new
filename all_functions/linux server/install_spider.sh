#!/bin/sh
# Change this to the last working Libs (may be you have to try and error)
nohup sh -c "/
	~/app-root/runtime/srv/python/bin/easy_install scopus_spider  && \
	~/app-root/runtime/srv/python/bin/easy_install python-spy  && \
	~/app-root/runtime/srv/python/bin/easy_install scrapy-jsonrpc  && \
	~/app-root/runtime/srv/python/bin/easy_install scrapyd  && \
	~/app-root/runtime/srv/python/bin/easy_install crappyspider  && \
	~/app-root/runtime/srv/python/bin/easy_install PyderWeb  && \
	~/app-root/runtime/srv/python/bin/easy_install SpiderBOY  && \
	~/app-root/runtime/srv/python/bin/easy_install incywincy  && \
	~/app-root/runtime/srv/python/bin/easy_install spyda  && \
	~/app-root/runtime/srv/python/bin/easy_install spider.py  && \
	~/app-root/runtime/srv/python/bin/easy_install spidertrap  && \
	~/app-root/runtime/srv/python/bin/easy_install spinneret  && \
	~/app-root/runtime/srv/python/bin/easy_install arsespyder  && \
	~/app-root/runtime/srv/python/bin/easy_install AWSpider  && \
	~/app-root/runtime/srv/python/bin/easy_install python-spidermonkey  && \
	~/app-root/runtime/srv/python/bin/easy_install spiderfetch  && \
	~/app-root/runtime/srv/python/bin/easy_install pydermonkey  && \
	~/app-root/runtime/srv/python/bin/easy_install pyspider  && \
	~/app-root/runtime/srv/python/bin/easy_install spyda  && \
	~/app-root/runtime/srv/python/bin/easy_install spyda  && \
	~/app-root/runtime/srv/python/bin/easy_install spyda  && \
	
	~/app-root/runtime/srv/python/bin/easy_install suminb-spider"> $OPENSHIFT_LOG_DIR/python_modules_install_5.log /dev/null 2>&1 &  
	#tail -f  $OPENSHIFT_LOG_DIR/python_modules_install_5.log
	
	
	~/app-root/runtime/srv/python/bin/easy_install loginform
	~/app-root/runtime/srv/python/bin/easy_install scrapyd
	~/app-root/runtime/srv/python/bin/easy_install scrapy
	~/app-root/runtime/srv/python/bin/easy_install facil-proxy-manager


	~/app-root/runtime/srv/python/bin/easy_install   scraperwiki
	~/app-root/runtime/srv/python/bin/easy_install  spynner