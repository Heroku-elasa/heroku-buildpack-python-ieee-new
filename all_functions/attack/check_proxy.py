#! /usr/bin/env python
__author__ = 's'



import urllib2
import urllib
import time
import socket

# Set some global variables
proxy_list = open('proxy_list.txt', 'r')
ip_check_url = 'http://automation.whatismyip.com/n09230945.asp'
#ip_check_url = 'http://pr4ss.tk'
user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0'
socket_timeout = 30

# Get real public IP address
def get_real_pip():
    req = urllib2.Request(ip_check_url)
    req.add_header('User-agent', user_agent)
    conn = urllib2.urlopen(req)
    page = conn.read()
    return page

# Set global variable containing "real" public IP address
#real_pip = get_real_pip()

# make randoe user agent
class RandomUserAgentMiddleware(object):
    from scraper.settings import USER_AGENT_LIST
    import random
    # from scrapy import log
    def process_request(self,):
        ua = random.choice(USER_AGENT_LIST)
        # if ua:
        #     request.headers.setdefault('User-Agent', ua)
        #     #log.msg('>>>> UA %s'%request.headers)
        return ua

        # Snippet imported from snippets.scrapy.org (which no longer works)
        # author: dushyant
        # date : Sep 16, 2011

# Check proxy
def check_proxy(pip):
    try:
        # Build opener
        proxy_handler = urllib2.ProxyHandler({'http':pip})
        opener = urllib2.build_opener(proxy_handler)
        user_agent=RandomUserAgentMiddleware().process_request()
        opener.addheaders = [('User-agent', user_agent)]
        urllib2.install_opener(opener)

        # Build, time, and execute request
        req = urllib2.Request(ip_check_url)
        time_start = time.time()
        conn = urllib2.urlopen(req)
        time_end = time.time()
        detected_pip = conn.read()

        # Calculate request time
        time_diff = time_end - time_start

        # Check if proxy is detected
        if detected_pip == real_pip:
            proxy_detected = True
        else:
            proxy_detected = False

    # Catch exceptions
    except urllib2.HTTPError, e:
        # print "ERROR: Code ", e.code
        return (True, False, 999)
    except Exception, detail:
        # print "ERROR: ", detail
        return (True, False, 999)

    # Return False if no exceptions, proxy_detected=True if proxy detected
    return (False, proxy_detected, time_diff)

def main():
    socket.setdefaulttimeout(socket_timeout)

    print "Current Public IP: " + real_pip
    print
    pr=open('proxy_list.txt','r')
    proxy_list=pr.readlines()
    pr.close()

    for current_proxy in proxy_list:
        current_proxy = current_proxy.strip()
        (proxy_failed, proxy_detected, time_diff) = check_proxy(current_proxy)
        if proxy_failed:
            print ("  FAILED: " + current_proxy)
        else:
            if proxy_detected:
                print "  DETECTED: %s ( %ss )" % ( current_proxy, str(round(time_diff, 2)) )
            else:
                print "  WORKING: %s ( %ss )" % ( current_proxy, str(round(time_diff, 2)) )
        time.sleep(300)

if __name__ == '__main__':
    main()
