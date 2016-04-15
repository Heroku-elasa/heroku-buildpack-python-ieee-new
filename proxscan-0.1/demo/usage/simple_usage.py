""" Name:simple_usage.py
    Description: It connects to a proxy ip and sends a request to the proxy
    to connect to a separate server. If the server sends back a cookie
    in this case '123' then it is likely to be a proxy.
"""
# It imports the basic functions.
from proxscan import *

# In this case we are checking for HTTP proxy.
REQUEST_HTTP = 'CONNECT 67.164.8.83:8000 HTTP/1.0\r\n\r\n'

# These handles are called when the checkup is finished.
def is_good(con):
    print 'it is a proxy'

def is_bad(con):
    print 'it isnt a proxy'

# is_active returns a Spin instance that we must bind callbacks
# to DONE, TIMEOUT, CONNECT_ERR, CLOSE in order to check proxy activity.
# You have proxy_ip, proxy_port, REQUEST TYPE, cookie, and timeout
# if the server doesn't reply the cookie in timeout seconds
# then it runs TIMEOUT event. You can increase timeout as much as
# needed. When checking for tons of proxies it is interesting to
# increase timeout.
con = is_active('210.79.216.252', 8080, REQUEST_HTTP, '123', 10)
xmap(con, DONE, is_good)
xmap(con, TIMEOUT, is_bad)
xmap(con, CONNECT_ERR, is_bad)

# If the supposed proxy closes the connection before sending a cookie
# then it isn't a proxy server.
xmap(con, CLOSE, is_bad)
gear.mainloop()

