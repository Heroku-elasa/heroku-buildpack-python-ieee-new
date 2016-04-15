import getopt
from os import getpid
from random import choice, randrange
import re
from string import letters
from sys import argv, exit
import threading
from time import sleep
import urllib

numthrds = 5

##############################################################################
#   FUNCTION DEFINITIONS                                                     #
##############################################################################

def errmsg(msg):
    from sys import stderr
    print >> stderr, str(getpid()) + ': ' + msg

def getformkey(str):
    r = re.search('<INPUT.*NAME="formkey" VALUE="[0-9a-zA-Z]+"', str)
    if r:
        return re.search('[0-9a-zA-Z]{10}', r.group(0)).group(0)
    else:
        return ''

def rndchars(x):
    str = ""
    for i in range(randrange(x, x + 2)):
        str += choice(letters).lower()
    return str

def rndsubject():
    s = ''
    for i in range(4):
        s += rndchars(6)
    return s

###################
# Do getopt stuff #
###################
msgfile = 'msg.txt'
opt_d = 0
opt_l = 0
proxfile = 'proxies.txt'
purl = 'http://slashdot.org/comments.pl'
sid = '20721'

try:
    opts, args = getopt.getopt(argv[1:], 'df:hlp:s:u:')
except getopt.GetoptError, msg:
    from sys import stderr
    print >> stderr, argv[0] + ': ' + str(msg)
    exit(3)

for c, optarg in opts:
    if c == '-d':
        opt_d = 1
    if c == '-f':
        msgfile = optarg
    if c == '-h':
        print 'pystorm: ' + argv[0] + ' [OPTION]...'
        print 'Perform automated comment posting on a Slashcode blog.\n'
        print '  -d         remove nonworking proxies from internal list'
        print '  -f [FILE]  read HTML messages from [FILE]'
        print '  -h         display this usage help'
        print '  -l         just display list of HTTP proxies collected and exit'
        print '  -p [FILE]  read list of HTTP proxies from [FILE], one per line'
        print '  -s [NUM]   post to the story with ID [NUM]'
        print '  -u [URL]   use [URL] as the comment posting script'
    if c == '-l':
        opt_l = 1
    if c == '-p':
        proxfile = optarg
    if c == '-s':
        sid = optarg
    if c == '-u':
        purl = optarg

if proxfile == '':
    errmsg('no proxy file given')
    exit(10)

##############################
# Read proxies into an array #
##############################

proxies = []
num_proxies = 0

try:
    f = open(proxfile, 'r')
except:
    errmsg("an error occurred when trying to open " + proxfile)
    exit(5)

for x in f.readlines():
    proxies.append('http://' + x.strip())
    num_proxies += 1

f.close()
if num_proxies == 1:
    errmsg('read in 1 proxy')
elif num_proxies > 0:
    errmsg('read in ' + str(num_proxies) + ' proxies')
else:
    errmsg('couldn\'t read in proxies from ' + proxfile)
    exit(7)

if opt_l > 0:
    for n in proxies:
        print n
    exit(0)

if purl == '':
    errmsg('no post URL given')
    exit(11)

if sid == '0':
    errmsg('no SID given')
    exit(9)

if msgfile == '':
    errmsg('no message file given')
    exit(4)

########################################
# Read messages/subjects into an array #
########################################

msgs = []
subjects = []
num_msgs = 0

try:
    f = open(msgfile, 'r')
except:
    errmsg('an error occurred when trying to open ' + msgfile)
    exit(2)

i = 0

msgs.append('')
for x in f.readlines():
    if x == "%\n":
        i = 0
        msgs.append('')
        num_msgs += 1
    else:
        if i == 0:
            msgs[num_msgs] = ''
            subjects.append(x)
            i = 1
        else:
            msgs[num_msgs] += x
num_msgs += 1

f.close()
if num_msgs == 1:
    errmsg('read in 1 message')
elif num_msgs > 0:
    errmsg('read in ' + str(num_msgs) + ' messages')
else:
    errmsg('couldn\'t read in messages from ' + msgfile)
    exit(6)

class SpamThread(threading.Thread):

    def run(self):

        global opt_d

        while 1:

            self.proxy = choice(proxies)
            self.opendev = urllib.FancyURLopener({'http': self.proxy})
            self.url = purl + '?sid=' + sid + '&op=Reply'

            # choose a message
            self.i = randrange(0, num_msgs)
            try:
                self.subject = subjects[self.i].strip()
            except:
                self.subject = rndsubject()
            self.msg = msgs[self.i] + '\n' + rndchars(2)

            # get rid of that "Re:" shit in the subject
            if self.subject[0:3] == 'Re:':
                self.subject = self.subject[3:]

            # get initial post form
            try:
                #f = self.opendev.open(self.url, urllib.urlencode({}))
                f = self.opendev.open(self.url)
            except IOError:
                print self.proxy, "couldn't open post form"
                continue
            try:
                str = f.read(50000)
            except:
                print self.proxy, "got no data"
                if opt_d != 0:
                    try:
                        proxies.remove(self.proxy)
                    except ValueError:
                        pass
                continue

            if '<TITLE>BANNED!</TITLE>' in str:
                print self.proxy, "is banned"
                if opt_d != 0:
                    try:
                        proxies.remove(self.proxy)
                    except ValueError:
                        pass
                continue

            # get formkey
            formkey = getformkey(str)
            if formkey != '':
                print self.proxy, "got 1st formkey " + formkey
            else:
                if '<FONT COLOR="#000000">i have a big cock' in str:
                    errmsg('This story has been archived')
                    exit(8)
                print "Proxy", self.proxy, "couldn't get 1st formkey"
                if opt_d != 0:
                    try:
                        proxies.remove(self.proxy)
                    except ValueError:
                        pass
                continue

            # setup POST request
            self.par = urllib.urlencode(
                {
                'sid': sid,
                'pid': '0',
                'formkey': formkey,
                'postersubj': self.subject,
                'postercomment': self.msg,
                'postanon_present': '1',
                'postanon': 'on',
                'op': 'Preview',
                'posttype': '2'
                })

            # preview comment
            try:
                f = self.opendev.open(self.url, self.par)
            except IOError:
                print self.proxy, "couldn't preview"
                if opt_d != 0:
                    try:
                        proxies.remove(self.proxy)
                    except ValueError:
                        pass
                continue
            try:
                str = f.read(50000)
            except:
                print self.proxy, "got no data"
                if opt_d != 0:
                    try:
                        proxies.remove(self.proxy)
                    except ValueError:
                        pass
                continue


            # is this proxy readonly?
            if '<!-- Error type: readonly -->' in str:
                print self.proxy, "is readonly"
                if opt_d != 0:
                    try:
                        proxies.remove(self.proxy)
                    except ValueError:
                        pass
                continue

            # get new formkey
            formkey = getformkey(str)
            if formkey != '':
                print self.proxy, "got 2nd formkey " + formkey
            else:
                print self.proxy, "couldn't get 2nd formkey"
                if opt_d != 0:
                    try:
                        proxies.remove(self.proxy)
                    except ValueError:
                        pass
                continue

            # fucking 20 second shit
            print 'Waiting 20 seconds'
            sleep(20)

            self.url = purl + '?sid=' + sid + '&op=Submit'

            # setup POST request
            self.par = urllib.urlencode(
                {
                'sid': sid,
                'pid': '0',
                'rlogin': '1',
                'formkey': formkey,
                'unickname': '',
                'upasswd': '',
                'postersubj': self.subject,
                'postercomment': self.msg,
                'op': 'Submit',
                'posttype': '2'
                })

            # submit comment
            f = self.opendev.open(self.url, self.par)
            try:
                str = f.read(50000)
            except:
                print self.proxy, "got no data"
                if opt_d != 0:
                    try:
                        proxies.remove(self.proxy)
                    except ValueError:
                        pass
                continue

            # did it work?
            if '</TABLE>Comment Submitted.' in str:
                print self.proxy, "posted #", self.i, "successfully"
            elif '<!-- Error type: filter message -->' in str:
                print self.proxy, "content too lame to post"
                exit(12)
            else:
                if 'Slashdot requires you to wait' in str:
                    print self.proxy, "hit 2 minute limit"
                    continue
                elif '<!-- Error type: troll message -->' in str:
                    print self.proxy, "has been 'temporarily' banned"
                    if opt_d != 0:
                        try:
                            proxies.remove(self.proxy)
                        except ValueError:
                            pass
                        continue
                print self.proxy, "screwed up submit"

#####################
# Main program loop #
#####################

if __name__ == '__main__':

    threadList = []

    # spawn threads
    for i in range(numthrds):
        thread = SpamThread()
        threadList.append(thread)

    # start the fuckers
    for thread in threadList:
        thread.start()

    # did all the threads start?
    numthreads = threading.activeCount() - 1
    errmsg('made ' + str(numthrds) + ' threads, ' + str(numthreads) + ' started')

    # keep track of how many proxies
    x = len(proxies)
    while threading.activeCount() > 1:
        y = len(proxies)
        if x != y:
            if y == 1:
                errmsg("1 proxy in global list")
            elif y == 0:
                errmsg("all proxies used up")
                exit(0)
            else:
                errmsg(str(y) + " proxies in global list")
        try:
            sleep(0.6)
            x = y
        except:
            exit(1)