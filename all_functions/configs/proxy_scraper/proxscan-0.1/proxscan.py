from untwisted.network import *
from untwisted.event import *
from untwisted.utils.stdio import *
from untwisted.utils.shrug import *
from untwisted.task import *
from socket import *
from struct import pack
from socket import inet_aton
from re import finditer, compile, DOTALL
from UserDict import UserDict

DONE = get_event()
TIMEOUT = get_event()
COMPLETE = get_event()

"""
These are examples of request that are to be sent.
We are assuming that 67.164.8.83:8001 is the server target
address.

REQUEST_HTTP = 'CONNECT 67.164.8.83:8001 HTTP/1.0\r\n\r\n'
REQUEST_SQUID = 'GET http://67.164.8.83:8001 HTTP/1.0\r\n\r\n'  
REQUEST_SOCKS4 = pack('!BBH4sB',
            4, # SOCK VERSION it is 4.
            1, # SOCK command, in this case 1 = CONNECT
            8000, # It is the targer port.
            inet_aton('67.164.8.83'), # The target ip.
            0) # terminator for our user-id (empty string).

REQUEST_SOCKS5 = '%s%s' % (struct.pack(
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
                inet_aton(self.target_ip),
                self.target_port))
"""


def set_up_server(port, backlog):
    """ This is the counter part of is_active. 
    It is the server that will wait for the cookies
    and send them back through the proxy.
    """

    sock = socket(AF_INET, SOCK_STREAM)
    serv = Spin(sock)
    serv.bind(('', port))
    serv.listen(backlog)
    # Since it will be a listening socket.
    Server(serv)

    def handle_accept(serv, con):
        """ It just installs basic protocols
        and set up basic handles. 
        """
        Stdin(con)
        Stdout(con)
        Shrug(con)
        # We just send the cookie back.
        xmap(con, FOUND, lambda con, data: con.dump('%s\r\n' % data))
        xmap(con, CLOSE, lose)

    xmap(serv, ACCEPT, handle_accept)
    return serv

def is_active(proxy_ip, proxy_port, request, cookie, timeout):
    """ This function is used to test whether a given proxy
        completes a cycle.
        It sends a cookie and waits for it. 
        If the cookie isn't sent back by the server it just runs timeout event.

        The proxy ip that wants to test.
        proxy_ip 
        
        The port in which the proxy listens on.
        proxy_port 
        It contains a specific chunk of text
        containing ip and port for the dummy server.
        request 

        The key that must be returned. If the server
        returns such a key then it is an active proxy.
        cookie  
        If the server doesnt send the cookie in timeout
        then it throws TIMEOUT event.
        timeout
    """
    sock = socket(AF_INET, SOCK_STREAM)
    con = Spin(sock)
    Client(con)

    def run_timeout():
        """ It is used to spawn a TIMEOUT event, it is
        if we don't get our cookie back in a given period
        of time after having connected then it might not
        be a proxy.
        """
        spawn(con, TIMEOUT)
        # We just kill the connection.
        lose(con)

    def missing_cookie(con):
        sched.unmark(timeout, run_timeout)
        lose(con)
    
    def set_up_con(con):
        """ When it stablishes a connection with the proxy
        this callback is called in order to set a timeout
        and send the request and the cookie and it waits
        for the cookie.
        """
        # It installs basic protocols.
        Stdout(con)
        Stdin(con)
        # We will be using Shrug since we will need it
        # to match the cookies that are sent back
        # through the proxy.
        Shrug(con)
        # Whenever a complete line is found we just
        # spawn such a line as an event.
        # So, if we send '123\r\n' the server would
        # send back '123\r\n' and we would know it is
        # a proxy.
        xmap(con, FOUND, lambda con, data: spawn(con, data, data))

        # It has to be called just once so we
        # pass True.

        sched.after(timeout, run_timeout, True)

        xmap(con, CLOSE, missing_cookie)
        # We dump the request.
        con.dump(request)

        # We must wait for the request being dumped
        # in order to send the cookie.
        yield hold(con, DUMPED)
        con.dump('%s\r\n' % cookie)

        # We then finally wait for the cookie back.
        yield hold(con, cookie)
        
        # If we got our cookie back then we do not need
        # to spawn TIMEOUT it means the proxy is active.
        sched.unmark(timeout, run_timeout)

        # We finally spawn DONE and lose the connection with the proxy.
        spawn(con, DONE)
        lose(con)
    
    # It starts the process.
    xmap(con, CONNECT, set_up_con)
    xmap(con, CONNECT_ERR, lose)
    con.connect_ex((proxy_ip, proxy_port)) 
    
    return con

def load_data(filename):
    """ This function is used to filter proxy file list.
        Sometimes you just copy&paste proxies from a site
        they commonly are pasted in a wrong format.
        This just extracts all the ip:port chunks
        and returns an iterator contaning Match objects
        then can do:
        for ind in load_file('some_dirty_file_of_proxies'):
            print ind.group('ip'), ind.group('port')

        It would print
        ip:port well formated.

        I use this function to filter proxy lists
        that i get from sites so i can test them.
    """
    ADDR_STR = '(?P<ip>[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)[^0-9]+?(?P<port>[0-9]+)'
    ADDR_REG = compile(ADDR_STR, DOTALL)


    with open(filename, 'r') as fd:
        data = fd.read()

    seq = finditer(ADDR_REG, data)
    return seq

class Task(UserDict, Mode):
    """ In a non asynchronous scenary, functions return values when their
    tasks are done. These tasks are performed sequentially. 

    As we are dealing with an asynchronous scenary we will need to know
    when a given function has performed its tasks. 

    As untwisted is purely based on event, some functions will rely on
    events in order to get their job done.

    we need a way of knowing when such a function really has got off its 
    'asynchronous scope'. 

    When a function gets in its scope most times it will be possible 
    to determine the number of tasks that will be performed.

    In this class I try to abstract a scheme that could work in some situations
    with an asynchronous scenary. I implement a counter and a variable to hold
    the limit of tasks that we are expecting to get done. It has
    a 'do' function which is to be called by the events(the tasks).
    When an event occurs it increments the number of tasks done
    when the number of tasks done is equal to the limit of tasks defined
    then we have our function's job entirely done.

    Of course, it wouldn't work in all scenaries, some functions
    will rely on events that might occur more than once so it might turn into
    a mess since we do not specify how many times a given event might occur.

    This class should work for functions/protocols that operate on spins whose events
    occur just once. 

    Another way of thinking of this class is like an accumulator of events.
    When it accumulates how many events as needed then it is time to spawn
    an event the COMPLETE event.
    """

    def __init__(self, lim=0):
        # I use UserDict since it is meant
        # to be a generic accumulator of events.
        # People will be able to have their callbacks
        # called with 'mode' as instance and 'mode' will be
        # a dictionary holding the events's argument.
        UserDict.__init__(self)
        Mode.__init__(self)
        
        # The amount of time that the events must occur.
        self.lim = lim

        # It counts how many times the events occured.
        self.index = 0
    
    def add(self):
        """ It adds a task to be performed. """
        self.lim = self.lim + 1

    def __call__(self, event, *args):
        """ Called when an event is issued it must be binded to a
        spin as xmap(spin, EVENT, task_instance)
        """

        # If there is not a list of args for
        # a given event we just create it.
        chain = self.setdefault(event, [])
        # It just accumulates the event argument.
        chain.append(args)

        # So, we have one task done.
        self.index = self.index + 1
        
        # It checks whether all the tasks were done.
        if self.index >= self.lim:
        # If all them we done we just spawn COMPLETE.
            spawn(self, COMPLETE) 

def run_test(database, request, cookie, timeout):
    """ This function receives  database of proxies
    and run a test on them. It runs the type of test
    specified by request and uses a cookie, timeout
    for all the proxies. 
    It returns a Task object that is used to match
    COMPLETE event that means all the proxies were
    checked.
    """
    task = Task()

    for ind in database:
        ip, port = ind.group('ip', 'port')
        con = is_active(ip, int(port), request, cookie, timeout)
        xmap(con, DONE, lambda con, ip=ip, port=port: task(DONE, ip, port))
        xmap(con, TIMEOUT, lambda con, ip=ip, port=port: task(TIMEOUT, ip, port))
        xmap(con, CONNECT_ERR, lambda con, ip=ip, port=port: task(CONNECT_ERR, ip, port))
        # If the host closed before sending the cookie back
        # then either it doesn't let to connect or just isn't
        # a proxy.
        xmap(con, CLOSE, lambda con, ip=ip, port=port: task(CLOSE, ip, port))
        task.add()

    return task

""" 
class RunTest(Mode):
    def __init__(self, database, request, cookie, timeout):
        Mode.__init__(self)
        self.pool = { DONE: [], TIMEOUT: [], CONNECT_ERR :[] }
        self.lim = 0
        self.index = 0

        for ind in database:
            ip, port = ind.group('ip', 'port')
            con = is_active(ip, int(port), request, cookie, timeout)
            xmap(con, DONE, self.update, DONE, (ip, port))
            xmap(con, TIMEOUT, self.update, TIMEOUT, (ip, port))
            xmap(con, CONNECT_ERR, self.update, CONNECT_ERR, (ip, port))
            self.add()
            self.lim = self.lim + 1

    def update(self, con, event, addr):
        self.pool[event].append(addr)
        self.index = self.index + 1

        if self.index >= self.lim:
            spawn(self, COMPLETE, self.pool)
"""
