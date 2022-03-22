from bs4 import BeautifulSoup
import requests
from models.models import Product,Search
import uuid
import dataBase.database as db

def formatNumber(num):
  if num % 1 == 0:
    return int(num)
  else:
    return num

def search_page(search:Search):
    if __name__ != "__main__":
        db.insertSearch(search)
        URL = 'https://www.olx.pt/ads/q-' + search.transcript + "/"
        r = requests.get(URL)
        soup = BeautifulSoup(r.content, 'html5lib')

        page = soup.find('div', attrs = {'class':'hasPromoted section clr'})
        result = None
        if(page != None):
            result = getProducts(page,search,soup)
        return result

def search_pageWithNumber(search:Search,index):
    if __name__ != "__main__":
        URL = 'https://www.olx.pt/ads/q-' + search.transcript + "/"
        if index != None:
            URL = URL + '?page=' + str(index)
        r = requests.get(URL)
        soup = BeautifulSoup(r.content, 'html5lib')

        return soup

def buildProduct(productRAW) -> Product: 
    if __name__ != "__main__":

        
        small1 = productRAW.find('td', attrs = {'valign': 'bottom','class': 'bottom-cell'})
        small1 = small1.find('small').find('span')
        location = small1.text
        date = small1.findNext('span').text

        strong1 = productRAW.find("strong")
        name = strong1.text
        rawPrice = strong1.findNext("strong").text.split(" ")[0]
        price:float = '0'
        isTradable = False
        if (rawPrice == "Troca"):
            isTradable = True
            price = -1
        else:
           priceTemp:str = rawPrice
           numberOfCommas = priceTemp.find(',')
           priceTemp = priceTemp.replace('.','')
           if(numberOfCommas != -1):
            priceTemp = priceTemp.replace(',','.')
           price = float(priceTemp)
        isNegotiable = True
        if productRAW.find('span', attrs = {'class': 'normal inlblk pdingtop5 lheight16 color-2'}) == None:
            isNegotiable = False
        url = productRAW.find('a')['href']
        img = productRAW.find('img')['src'] if productRAW.find('img') != None else 'NO IMAGE'
        product = Product(name,formatNumber(price),isTradable,isNegotiable,date,url,img,location)
        # product = {'id':id,'name':name,'price':price,'isTradable':isTradable,'isNegotiable':isNegotiable,'date':date,'url':url,'img':img,'location':location}

        return product  

def getProducts(page,search:Search,soup):
    if __name__ != "__main__":
        numberOfProducts = page.find("p").text.split(" ")[1];
        pagerEl = soup.find('div', attrs = {'class':'pager rel clr'})
        if (pagerEl == None):
            numberOfPages = 1
        else:
            allPagers = pagerEl.findAll('span', attrs = {'class': None})
            lastPageEl = allPagers[-2]
            numberOfPages = int(lastPageEl.getText());

        print('Number of Products:      ' + str(numberOfProducts)) 
        print("Number of Pages:         " + str(numberOfPages))
        print("")

        products:list = []

        productList = soup.find('table', attrs = {'id':'offers_table'})

        # Cycle all the adds and builds the product objects
        offer = productList.find('div', attrs = {'class':'offer-wrapper'})
        product = buildProduct(offer)
        products.append(product)
            
        isLastProduct = False
        while isLastProduct == False:
            offer = offer.findNext('div', attrs = {'class':'offer-wrapper'})
            if offer == None:
                isLastProduct = True
            else:
                product = buildProduct(offer)
                products.append(product)
        # Cycle all the adds and builds the product objects

        print("page: " + str(1))

        if(numberOfPages > 1):
            for pageIndex in range(2, numberOfPages + 1):
                    soup = search_pageWithNumber(search, pageIndex)
                    productList = soup.find('table', attrs = {'id':'offers_table'})

                    # Cycle all the adds and builds the product objects
                    offer = productList.find('div', attrs = {'class':'offer-wrapper'})
                    product = buildProduct(offer)
                    products.append(product)
                    

                    isLastProduct = False
                    while isLastProduct == False:
                        offer = offer.findNext('div', attrs = {'class':'offer-wrapper'})
                        if offer == None:
                            isLastProduct = True
                        else:
                            product = buildProduct(offer)
                            products.append(product)
                    # Cycle all the adds and builds the product objects

                    print("page: " + str(pageIndex))
                    if(pageIndex == numberOfPages):
                        break
                    else:
                        pageIndex = pageIndex + 1
        
        return products


def confirm_prompt(question: str) -> bool:
    reply = None
    while reply not in ("", "y", "n"):
        reply = input(f"{question} (Y/n): ").lower()
    return (reply in ("", "y"))