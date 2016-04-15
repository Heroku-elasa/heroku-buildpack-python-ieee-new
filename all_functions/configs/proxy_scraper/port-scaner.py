
import socket
import subprocess
import sys
import urllib2
from datetime import datetime
from ipwhois import IPWhois
#import ipaddress
University_port_checker="..//..//configs//sites_proxy//all_proxies_list//University_port_checker.txt"
Proxy_on='..//..//configs//sites_proxy//all_proxies_list//university_Proxy_on.txt'
# Clear the screen
subprocess.call('clear', shell=True)

ports=['80','8080','1080','3128','8888','8123','8118','8081','6588','4444','9999','443','8121','7004','8118','6903'];
from grab import Grab, GrabError
def get_valid_proxy(proxy_list): #format of items e.g. '128.2.198.188:3124'
    g = Grab()
    for proxy in proxy_list:
        for port in ports:
            pr=proxy.split(':')[0]+':'+port;
            g.setup(proxy=pr, proxy_type='http', connect_timeout=5, timeout=5)
            try:
                g.go('google.com')
            except GrabError:
                #logging.info("Test error")
                pass
            else:
                yield proxy

def whois(pr):
    from pprint import pprint
    obj = IPWhois(pr.split(':')[0])
    #results = obj.lookup(get_referral=True)
    results = obj.lookup()
    return results


def is_bad_proxy(pip):
    try:
        proxy_handler = urllib2.ProxyHandler({'http': pip})
        opener = urllib2.build_opener(proxy_handler)
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib2.install_opener(opener)
        req=urllib2.Request('http://www.google.com')  # change the URL to test here
        sock=urllib2.urlopen(req)
    except urllib2.HTTPError, e:
        print 'Error code: ', e.code
        return e.code
    except Exception, detail:
        print "ERROR:", detail
        return True
    return False
def prox_list_base_range(range1='',range2=''):
    if range1.split('.')[0]==range2.split('.')[0]:
        r1=range1.split('.')[1];r2=range2.split('.')[1]
        if r1.split('.')[0]==r2.split('.')[0]:
            r1=r1.split('.')[1];r2=r2.split('.')[1]
            if r1.split('.')[0]==r2.split('.')[0]:
                r1=r1.split('.')[1];r2=r2.split('.')[1]
                if r1.split('.')[0]==r2.split('.')[0]:
                    pass

def ipRange(start_ip, end_ip):
   start = list(map(int, start_ip.split(".")))
   end = list(map(int, end_ip.split(".")))
   temp = start
   ip_range = []

   ip_range.append(start_ip)
   while temp != end:
      start[3] += 1
      for i in (3, 2, 1):
         if temp[i] == 256:
            temp[i] = 0
            temp[i-1] += 1
      ip_range.append(".".join(map(str, temp)))

   return ip_range


# sample usage


def find_on_proxy_range(Proxy_university='',Proxy_on=''):
    socket.setdefaulttimeout(120)

    # two sample proxy IPs
    proxyList = [line.rstrip('\n') for line in open(Proxy_university ,'a+')]
    d=open(Proxy_on ,'a+');
    ports=['80','8080','1080','3128','8888','8123','8118','8081','6588','4444','9999','443','8121','7004','8118','6903'];
    for p_range in range(1,1025):
        ports.append(str(p_range));

    for currentProxy in proxyList:
        k=currentProxy.replace('\n','').split(':')[0];
        try:
            whosi=whois(k);
            dd=whosi['nets']

            range_=dd[0];
            #range1=range.items()
            #print range1

            range2=dd[0].keys()
            range_value=dd[0].values()
            if 'range' in range2:
                i = range2.index('range')
                #print players.name('range')
            print '\n'+str(i)+'\n'
            print range2[i]
            print range_value[i]
            range_12=range_value[i];
            range_1=range_12.split('-')[0].replace(' ','');
            range_2=range_12.split('-')[1].replace(' ','')
            ip_range = ipRange(range_1, range_2)
            for ip in ip_range:
                print(ip)
            for ip in ip_range:
                #ip_existance_cheker=ipaddress.ip_address(ip)
                #if  ip_existance_cheker:
                    for port in ports:
                        currentProxy=ip;
                        currentProxy=currentProxy.split(':')[0]+':'+port;
                        if is_bad_proxy(currentProxy):
                            print "Bad Proxy %s" % (currentProxy)
                        else:
                            print "%s is working" % (currentProxy)
                            #proxies_on = [line.rstrip('\n') for line in open(Proxy_on ,'a+')]
                            #proxies_on.append(currentProxy)

                            d.writelines(currentProxy);
        except:
            pass
    d.close()

def find_on_proxy(Proxy_university='',Proxy_on=''):
    socket.setdefaulttimeout(120)

    # two sample proxy IPs
    proxyList = [line.rstrip('\n') for line in open(Proxy_university ,'a+')]
    d=open(Proxy_on ,'a+');
    ports=['80','8080','1080','3128','8888','8123','8118','8081','6588','4444','9999','443','8121','7004','8118','6903'];

    for currentProxy in proxyList:

        for port in ports:
            currentProxy=currentProxy.split(':')[0]+':'+port;
            if is_bad_proxy(currentProxy):
                print "Bad Proxy %s" % (currentProxy)
            else:
                print "%s is working" % (currentProxy)
                #proxies_on = [line.rstrip('\n') for line in open(Proxy_on ,'a+')]
                #proxies_on.append(currentProxy)

                d.writelines(currentProxy);
    d.close()
#s=get_valid_proxy(University_port_checker)
#find_on_proxy(University_port_checker,Proxy_on)
#find_on_proxy_range(University_port_checker,Proxy_on)

#find_on_proxy_range(Proxy_university='',Proxy_on='')

# Ask for input
def main():
    remoteServer    = raw_input("Enter a remote host to scan: ")
    remoteServerIP  = socket.gethostbyname(remoteServer)

    # Print a nice banner with information on which host we are about to scan
    print "-" * 60
    print "Please wait, scanning remote host", remoteServerIP
    print "-" * 60

# Check what time the scan started
    t1 = datetime.now()

# Using the range function to specify ports (here it will scans all ports between 1 and 1024)

# We also put in some error handling for catching errors
    ports=['80','8080','1080','3128','8888','8123','8118','8081','6588','4444','9999','443','8121','7004','8118','6903'];
    try:
        for port in range(1,1025):
        #for port in ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((remoteServerIP, int(port)))
            if result == 0:
                print "Port {}: \t Open".format(port)
            else:
                print "Port {}: \t Closed".format(port)
            sock.close()

    except KeyboardInterrupt:
        print "You pressed Ctrl+C"
        sys.exit()

    except socket.gaierror:
        print 'Hostname could not be resolved. Exiting'
        sys.exit()

    except socket.error:
        print "Couldn't connect to server"
        sys.exit()

    # Checking the time again
    t2 = datetime.now()

    # Calculates the difference of time, to see how long it took to run the script
    total =  t2 - t1

    # Printing the information to screen
    print 'Scanning Completed in: ', total
find_on_proxy_range(University_port_checker,Proxy_on)

if __name__ == '__main__':

    find_on_proxy_range(University_port_checker,Proxy_on)
    main()
