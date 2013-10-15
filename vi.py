import sys
import re
import os
import requests
import jinja2
from requests_oauthlib import OAuth1
from flask import render_template
from flask import Flask
from r_s import rank, check, sort
import json
#from scrap import get_category_links

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')



app = Flask('myapp', template_folder=tmpl_dir)
app = Flask(__name__)

BASE_URL = u'https://api.twitter.com/1.1/'

client_key = u'h1T9MORP5zGidpXlibAtA'
client_secret = u'3duWKMwMmnHfPbZPjfSqyEMNnFi1mWEUXUP24QgpE'
resource_owner_key = u'1746056306-LW4UXRxp0qjtij57gXrYkDX5Uy4ANFQyMxoHD2B'
resource_owner_secret = u'rFxMKOaonqWnVpdw3K0p2CoLiWwLfdVFOpA5RlzDcw'

oauth = OAuth1(client_key, client_secret,
                     resource_owner_key, resource_owner_secret)

headeroauth = OAuth1(client_key, client_secret,
                     resource_owner_key, resource_owner_secret,
                     signature_type='auth_header')


queryoauth = OAuth1(client_key, client_secret,
                    resource_owner_key, resource_owner_secret,
                    signature_type='query')


bodyoauth = OAuth1(client_key, client_secret,
                   resource_owner_key, resource_owner_secret,
                   signature_type='body')
                   
payload = {'q': 'undervalued stocks','count':100}
url = 'https://api.twitter.com/1.1/search/tweets.json'
r = requests.get(url, auth=oauth,params=payload)
a=r.json()                   
b=[]

#ef reg_loop(reg

@app.route('/')			   
def vi():
	for i in range(payload['count']):
		time=a['statuses'][i]['created_at']
		st=a['statuses'][i]['text']
		t=time.encode('utf8')
		s=st.encode('utf8')
		tup=(st,time)
		b.append(tup)
	return render_template('vi.html',updates=b)
	#return b

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/stocks')	
def stocks():
	stock_ls=[]
	reg=r'\$[a-zA-Z]+(?:\.(?:[a-zA-Z])+)?'
	for tweets,time in b:
		stock=re.findall(reg,tweets)
		if stock :
			#print stock
			#stock=map(stock[0][1:]
			#print stock
			stock_ls.extend([json.dumps(s[1:]) for s in stock ])
	stock_ls=list(set(stock_ls))
	#stock_ls=map(,stock_ls)
	#tags=str(get_category_links('AAPL'))
	#tags='<p> asd </p>'
	return render_template('ticker.html',tick=stock_ls)
	#return json.dumps(tags)
	
#@app.route('/stocks',methods=['POST'])
#def webs():
#	w=request.form. 

	

	
@app.route('/links')
def link():
	link_ls=[]
	reg2=r'http(?:\S)*'
	for tweets,followers,friends,favorite,total,time in [(a['statuses'][i]['text'],a['statuses'][i]['user']['followers_count'],
								          		          a['statuses'][i]['user']['friends_count'],a['statuses'][i]['favorite_count'],
								                          a['statuses'][i]['user']['statuses_count'],a['statuses'][i]['created_at']) 
								                          for i in range(payload['count']) if u'App' not in a['statuses'][i]['text']]:
		links=re.findall(reg2,tweets)
		if links and 'App' not in links:
			link_ls.append(rank(links,followers,friends,favorite,total,time))
	link_ls=check(link_ls)
	link_st=sort(link_ls)
	return render_template('link.html',lkt=link_st[:20],lko=link_ls[:20])
	#return link_ls
	

if __name__ == "__main__":
    app.run()
#print a['statuses'][0]['user']['statuses_count']
#vi()
#print stocks()
    