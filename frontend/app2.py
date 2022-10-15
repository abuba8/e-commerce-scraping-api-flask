from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup as Bs
import lxml
from flask_cors import CORS, cross_origin
from werkzeug.datastructures import ImmutableMultiDict
import json

app = Flask(__name__)

CORS(app, resources = {r"/api/*": {"origins": "*"}})
app.config['CORS HEADERS'] = 'Content-Type'

def get_search_result_amazon(url):
    #https://www.amazon.com/s?k=hp+laptop&ref=nb_sb_noss_2
    #https://www.amazon.com/s?k=hp&ref=nb_sb_noss_2
    link = "https://www.amazon.com/s?k={}&ref=nb_sb_noss_2"
    query = url.replace(' ','+')
    url = link.format(query)
    print('getting data from amazon.....')
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 Edg/90.0.818.66',
        'Accept-language': 'en-GB, en-US;q=0.9,en;q=0.8',
    }
    r= requests.get(url, headers=headers)

    soup = Bs(r.text, 'lxml')
    namedivs = soup.find_all("span", {"class": "a-size-medium a-color-base a-text-normal"})
    pricedivs = soup.find_all("span", {"class": "a-offscreen"})
    searchdivs = soup.find_all("a", {"class": "a-link-normal a-text-normal"}, href=True)
    imagedivs = soup.find_all("img", {"class":"s-image"})
    search_names = []
    search_prices=[]
    search_urls=[]
    search_images = []
    i=0
    for (n, p, s, img) in zip(namedivs, pricedivs, searchdivs, imagedivs):
        i=i+1
        search_names.append(n.getText())
        search_prices.append(p.getText())
        search_images.append(img['src'])
        find2fdp = s['href'].find("%2Fdp%")
        indexstart = s['href'].find('url=%')
        if find2fdp == -1:
            search_urls.append('https://www.amazon.com/' +s['href'][indexstart+7:])
        else:
            search_urls.append('https://www.amazon.com/' +s['href'][indexstart+7:find2fdp]+'/dp/'+s['href'][find2fdp+8:s['href'].find("%2Fref")]+'/')

        if(i==5):
            break
    
    myDict = {}
    myDict["names"] = search_names
    myDict["prices"] = search_prices
    myDict["urls"] = search_urls
    myDict["images"] = search_images
    #dictionary = dict(zip(keys, values))

    return myDict
 


def get_search_result_ebay(url):
	#https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570.l1313&_nkw=hp+laptop&_sacat=0
	#https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570.l1313&_nkw=hp&_sacat=0
	print('getting data from ebay.....')
	link = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570.l1313&_nkw={}&_sacat=0"
	query = url.replace(' ','+')
	url = link.format(query)
	headers={
	    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 Edg/90.0.818.66',
	    'Accept-language': 'en-GB, en-US;q=0.9,en;q=0.8',
	}
	r= requests.get(url, headers=headers)

	soup = Bs(r.text, 'lxml')
	namedivs = soup.find_all("h3", {"class":"s-item__title"})
	pricedivs = soup.find_all("span", {"class": "s-item__price"})
	urldivs = soup.find_all("a", {"class": "s-item__link"})
	imagedivs = soup.find_all("img", {"class":"s-item__image-img"})
	search_names = []
	search_prices=[]
	search_urls=[]
	search_images = []
	i=0
	for n in namedivs:
	    
	    i=i+1
	    if i==1:
	        pass
	    else:
	        #print(n.getText())
	        search_names.append(n.getText())
	        #print(n.getText())
	        search_prices.append(pricedivs[i-2].getText())
	        search_urls.append(urldivs[i-1]['href'])
	        search_images.append(imagedivs[i-2]['src'])
	        

	    if(i==6):
	        break

	myDict = {}
	myDict["names"] = search_names
	myDict["prices"] = search_prices
	myDict["urls"] = search_urls
	myDict["images"] = search_images
	#dictionary = dict(zip(keys, values))

	return myDict
       


 
def get_search_result_daraz(url):
    #https://www.daraz.pk/catalog/?q=hp+laptop&_keyori=ss&from=input&spm=a2a0e.searchlist.search.go.1444920evuAmgX
    #https://www.daraz.pk/catalog/?q=hp&_keyori=ss&from=input&spm=a2a0e.searchlist.search.go.1444920evuAmgX
    print('getting data from Daraz.....')
    link = "https://www.daraz.pk/catalog/?q={}&_keyori=ss&from=input&spm=a2a0e.searchlist.search.go.1444920evuAmgX"
    query = url.replace(' ','+')
    url = link.format(query)
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 Edg/90.0.818.66',
        'Accept-language': 'en-GB, en-US;q=0.9,en;q=0.8',
    }
    r= requests.get(url, headers=headers)

    soup = Bs(r.text, 'lxml')
    
    search_names = []
    search_prices=[]
    search_urls=[]
    search_images = []
    urldiv = soup.find_all("script", {"type":"application/ld+json"})
    findurl = urldiv[1]
    findurl = str(findurl)
    for i in range(1,6,1):
        try:
            #print(i)
            positionst = findurl.find('"position":'+str(i))
            positionend = findurl.find('},{"@type":"ListItem","position":'+str(i+1))
            new_url=findurl[positionst+20:positionend-1]
            r= requests.get(new_url, headers=headers)
            #print(new_url)
            search_urls.append(new_url)
            r= requests.get(new_url, headers=headers)
            soup = Bs(r.text, 'lxml')
            soup = str(soup)
            nstartindex = soup.find(',"showFacebookFallback":false,"title":"')
            nendindex = soup.find('","type":"product","url"')
            #print(soup[nstartindex+39:nendindex])
            search_names.append(soup[nstartindex+39:nendindex])
            pstartindex = soup.find('"salePrice":{"text":"')
            #print(soup[pstartindex+21:pstartindex+31])
            search_prices.append(soup[pstartindex+21:pstartindex+31])
            
            istartindex = soup.find('https://static-01.daraz.pk/')
            #print(soup[istartindex:istartindex+65])
            search_images.append(soup[istartindex:istartindex+65])
        except:
            search_names.append('error getting file')

    myDict = {}
    myDict["names"] = search_names
    myDict["prices"] = search_prices
    myDict["urls"] = search_urls
    myDict["images"] = search_images
    #dictionary = dict(zip(keys, values))

    return myDict




@app.route('/api', methods=['POST', 'GET'])
@cross_origin()
def index():
    if(request.method=='POST'):
        data = dict(request.get_json())
        print (data['query'])
        query = data['query']
        amazon = get_search_result_amazon(query)
        e_bay = get_search_result_ebay(query)
        daraz = get_search_result_daraz(query)
        finalDict = {}
        finalDict["amazon"] = amazon
        finalDict["ebay"] = e_bay
        finalDict["daraz"] = daraz
        return jsonify(finalDict)
    else:
        return jsonify({'result': 'GET request'})
    

if __name__ == "__main__":
    app.run(debug=True)