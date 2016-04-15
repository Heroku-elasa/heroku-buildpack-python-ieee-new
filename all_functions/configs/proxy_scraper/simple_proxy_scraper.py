#!/usr/bin/env python
from BeautifulSoup import BeautifulSoup as Soup
import requests
import re, urllib
def Scrape_simple(url = 'http://proxy-hunter.blogspot.com/2010/03/18-03-10-speed-l1-hunter-proxies-310.html'):
    document = urllib.urlopen(url)
    tree = Soup(document.read())
    regex  = re.compile(r'^(\d{3}).(\d{1,3}).(\d{1,3}).(\d{1,3}):(\d{2,4})')
    proxylist = tree.findAll(attrs = {"class":"Apple-style-span", "style": "color: black;"}, text = regex)
    data = proxylist[0]
    for x in data.split('\n'):
            print x
    return x

def get_proxy_list(pr_site_list='..//..//configs//sites_proxy//all_proxies_list//Sites_to_get_proxylist.txt'):
    hosts = [host.strip() for host in open(pr_site_list).readlines()]
    siteList = [];proxies_list=[]
    i=-1
    for j in range(i + 1, len(hosts)):
        if ( not re.findall("#", hosts[j]) and hosts[j] != '' ):
            siteList.append(hosts[j])
    for j in range(0, len(siteList)):
        proxies=Scrape_simple(str(siteList[j]))
        if ( not re.findall("#", proxies[j]) and proxies[j] != '' ):
            proxies_list.append(proxies[j])

    return proxies_list


pages = ['https://www.hidemyass.com/proxy-list']

for page in pages:
    hidemyass = Soup(requests.get(page).text)
    rows = hidemyass.find_all(lambda tag:tag.name=='tr' and tag.has_attr('class'))
    for row in rows:
        fields = row.find_all('td')
        # get ip, port, and protocol for proxy
        ip = fields[1].get_text()            # <-- Here's the above td element
        port = fields[2].get_text()
        protocol = fields[6].get_text().lower()
        # store proxy in database
        db.add_proxy({'ip':ip,'port':port,'protocol':protocol})
        num_found += 1

pr=get_proxy_list()
