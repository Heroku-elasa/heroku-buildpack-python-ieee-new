import urllib
import simplejson

query = urllib.urlencode({'q' : 'damon cortesi'})
url ='/ajax/services/search/web?v=1.0&%s' \
  % (query)
search_results = urllib.urlopen(url)
json = simplejson.loads(search_results.read())
results = json['responseData']['results']
for i in results:
  print i['title'] + ": " + i['url']</span></code></pre></td></tr></table></div></figure></notextile></div>

