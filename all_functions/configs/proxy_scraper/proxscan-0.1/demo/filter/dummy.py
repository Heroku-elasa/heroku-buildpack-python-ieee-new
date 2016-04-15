""" Name: dummy.py
    Description: This is the counter part of check_proxy.py
    If you are going to check for proxy active you need to run this server
    either on your machine or in other machine.
    Usage: 
    python dummy.py port backlog
"""

from proxscan import *
import sys
script, port, backlog = sys.argv
port = int(port)
backlog = int(backlog)

serv = set_up_server(port, backlog)
xmap(serv, ACCEPT, lambda serv, con: sys.stdout.write('Connected %s:%s.\r\n' % con.getpeername()))
gear.mainloop()
