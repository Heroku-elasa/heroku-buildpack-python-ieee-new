
__author__ = 's'


import twill
t_com = twill.commands
t_com.reset_browser
t_com.reset_output
t_com = twill.commands
## get the default browser
t_brw = t_com.get_browser()
# t_brw.set_agent_string("Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14")
t_brw.add_extra_headers = [
    ('User-agent','Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1'),
    ('Accept','text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5;application/json;text/javascript;*/*'),
    ('Accept-Language','en,hu;q=0.8,en-us;q=0.5,hu-hu;q=0.3'),
    ('Accept-Encoding', 'gzip, deflate'),
    ('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.7'),
    ('Keep-Alive', '300'),
    ('Connection', 'keep-alive'),
    ('Cache-Control', 'max-age=0'),
    # ('Referer', self.url),
    ('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8'),
    ('X-Requested-With', 'XMLHttpRequest')
]
## open the url
# url = 'http://google.com'

# t_brw.save_cookies(self.cookies)
# t_brw.load_cookies(self.cookies)
print t_com.show_extra_headers()
print t_com.show_cookies()
t_brw.go('wwww.google.com')
