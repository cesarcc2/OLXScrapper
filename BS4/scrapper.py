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
      product['img'] = productRAW.find('img')['src'] if productRAW.find('img') != None else 'NO IMAGE'
      product['location'] = location.encode('utf-8')
      return product

def search_page(search,index = None):
    URL = 'https://www.olx.pt/ads/q-' + search + "/"
    if index != None:
        URL = URL + '?page=' + str(index)
    r = requests.get(URL)
    print(URL)
    soup = BeautifulSoup(r.content, 'html5lib')
    return soup

# 
#----------------------- MAIN -------------------
# 

search = raw_input('Enter your search:')

soup = search_page(search)

numberOfProducts = soup.find('div', attrs = {'class':'hasPromoted section clr'}).find("p").text.split(" ")[1];
numberOfPages = int(soup.find('div', attrs = {'class':'pager rel clr'}).findAll('span', attrs = {'class': None})[-2].getText());
currentPage = int(soup.find('span', attrs = {'class': 'block br3 c41 large tdnone lheight24 current'}).find('span').text)
print(numberOfProducts) 
print("Pages: " + str(numberOfPages))

products = []

productList = soup.find('table', attrs = {'id':'offers_table'})

# Cycle all the adds and builds the product objects
offer = productList.find('div', attrs = {'class':'offer-wrapper'})
products.append(get_product(offer))

isLastProduct = False
while isLastProduct == False:
    offer = offer.findNext('div', attrs = {'class':'offer-wrapper'})
    if offer == None:
        isLastProduct = True
    else:
        products.append(get_product(offer))
# Cycle all the adds and builds the product objects

print("number of pages: " + str(numberOfPages) + "      page: " + str(1) + "       last product: " + products[len(products) -1]['name'])

for x in range(2, numberOfPages + 1):
        soup = search_page(search,x)
        productList = soup.find('table', attrs = {'id':'offers_table'})

        # Cycle all the adds and builds the product objects
        offer = productList.find('div', attrs = {'class':'offer-wrapper'})
        products.append(get_product(offer))

        isLastProduct = False
        while isLastProduct == False:
            offer = offer.findNext('div', attrs = {'class':'offer-wrapper'})
            if offer == None:
                isLastProduct = True
            else:
                products.append(get_product(offer))
        # Cycle all the adds and builds the product objects

        print("number of pages: " + str(numberOfPages) + "      page: " + str(x) + "       last product: " + products[len(products) -1]['name'])
        if(x == numberOfPages):
            break
        else:
            x = x + 1
        



filename = 'products.csv'
with open(filename, 'wb') as f:
    w = csv.DictWriter(f,['name','price','negotiable','date','url', 'img', 'location'])
    w.writeheader()
    for product in products:
        w.writerow(product)


# 
#----------------------- MAIN END -------------------
# 