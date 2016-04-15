import twill.commands
import BeautifulSoup

class browser:
  def __init__(self, url="http://www.google.com",log = None):
     self.a=twill.commands
     self.a.config("readonly_controls_writeable", 1)
     self.b = self.a.get_browser()
     self.b.set_agent_string("Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14")
     self.log = log
     self.b.clear_cookies()
     self.url=url
  def googleQuery(self, query="python code"):
     self.b.go(self.url)
     #self.b.showforms()
     f = self.b.get_form("f")
     #print "form is %s" % f
     f["q"] = query
     self.b.clicked(f, "btnG")
     self.b.submit()
     pageContent = self.b.get_html()
     soup=BeautifulSoup.BeautifulSoup(pageContent)
     ths = soup.findAll(attrs={"class" : "l"})
     for a in ths:
        print a

t=browser()
t.googleQuery("twill queries")