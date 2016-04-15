""" Usage:
    python check_proxy.py http xab 67.164.8.83 8000 123 100
    http is the protocol
    xab is the source containing ips.
    67.164.8.83 8000 are the ip and port of the dummy server(. I actually use a shell to run the echo server.
    123 is the cookie that the server must reply.
    100 is the timeout that it must wait for the cookie before losing the connection.

    Obs: If you want to run the server locally you can just run the dummy.py file
    that is going to mount a listening socket on an specific port and pass
    your ip to check_proxy.py as above.
"""

from proxscan import *
import sys

header = {
            'http':lambda ip, port: 'CONNECT %s:%s HTTP/1.0\r\n\r\n' % (ip, port),
            'squid':lambda ip, port:'GET http://%s:%s HTTP/1.0\r\n\r\n' % (ip, port),
            'socks4': lambda ip, port: pack('!BBH4sB',
                4, # SOCK VERSION it is 4.
                1, # SOCK command, in this case 1 = CONNECT
                int(port), # It is the targer port.
                inet_aton(ip), # The target ip.
                0), # terminator for our user-id (empty string).
            'socks5': lambda ip, port: '%s%s' % (struct.pack(
                    '!BBB',
                    5, # version
                    1, # number of supported methods
                    0, # anonymous
                    )
            # HACK: just send the CONNECT request straight away instead of
            # waiting for the server to reply to our negotiation.
                    , 
                    struct.pack(
                    '!BBBB4sH',
                    5, # version
                    1, # command (1 for CONNECT)
                    0, # reserved
                    1, # address type (1 for IPv4 address)
                    inet_aton(ip), int(port)))
         }

if __name__ == '__main__':
    script, protocol, source, ip, port, cookie, timeout = sys.argv

    database = load_data(source)
    request = header[protocol](ip, port)
    task = run_test(database, request, cookie, int(timeout))

    def save_result(task):
        print task
        done_list = task.get(DONE)
        if done_list:
            with open('good_http_proxy', 'a+') as fd:
                for ip, port in done_list:
                    fd.write('%s:%s\n' % (ip, port))

        connect_err_list = task.get(CONNECT_ERR)
        if connect_err_list:
            with open('bad_http_proxy', 'a+') as fd:
                for ip, port in connect_err_list:
                    fd.write('%s:%s\n' % (ip, port))

        timeout_list = task.get(TIMEOUT)
        if timeout_list:
            with open('timeout_http_proxy', 'a+') as fd:
                for ip, port in timeout_list:
                    fd.write('%s:%s\n' % (ip, port))

        close_list = task.get(CLOSE)
        if close_list:
            with open('close_http_proxy', 'a+') as fd:
                for ip, port in close_list:
                    fd.write('%s:%s\n' % (ip, port))
               
        raise Kill

    xmap(task, COMPLETE, save_result)
    gear.mainloop()

