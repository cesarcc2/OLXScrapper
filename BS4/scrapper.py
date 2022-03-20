import requests
import csv
from bs4 import BeautifulSoup
# from product import get_product

def get_product(productRAW):
      product = {}

      small1 = productRAW.find('td', attrs = {'valign': 'bottom','class': 'bottom-cell'})
      small1 = small1.find('small').find('span')
      location = small1.text
      date = small1.findNext('span').text

      strong1 = productRAW.find("strong")
      name = strong1.text
      price = strong1.findNext("strong").text

      isNegotiable = True
      if productRAW.find('span', attrs = {'class': 'normal inlblk pdingtop5 lheight16 color-2'}) == None:
          isNegotiable = False

      product['name'] = name.encode('utf-8')
      product['price'] = price.encode('utf-8')
      product['negotiable'] = isNegotiable
      product['date'] = date.encode('utf-8')
      product['url'] = productRAW.find('a')['href']
      product['img'] = productRAW.find('img')['src']
      product['location'] = location.encode('utf-8')
      return product


# 
#----------------------- MAIN -------------------
# 

URL = "https://www.olx.pt/ads/q-rtx-2070/"
r = requests.get(URL)

 # If this line causes an error, run 'pip install html5lib' or install html5lib
soup = BeautifulSoup(r.content, 'html5lib')
# print(soup.prettify())

numberOfProducts = 0;
products = []

productList = soup.find('table', attrs = {'id':'offers_table'})
numberOfProducts = soup.find('div', attrs = {'class':'hasPromoted section clr'}).find("p").text.split(" ")[1]

print(numberOfProducts) 

offer = productList.find('div', attrs = {'class':'offer-wrapper'})
products.append(get_product(offer))

lastProduct = False
while lastProduct == False:
    offer = offer.findNext('div', attrs = {'class':'offer-wrapper'})
    if offer == None:
        lastProduct = True
    else:
        products.append(get_product(offer))

filename = 'products.csv'
with open(filename, 'wb') as f:
    w = csv.DictWriter(f,['name','price','negotiable','date','url', 'img', 'location'])
    w.writeheader()
    for product in products:
        w.writerow(product)


# 
#----------------------- MAIN END -------------------
# 