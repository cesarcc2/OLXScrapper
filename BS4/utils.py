from bs4 import BeautifulSoup
import requests
import services.firebaseService as firebaseService


def search_page(search,index = None):
    if __name__ != "__main__":
        firebaseService.saveSearch(search)
        URL = 'https://www.olx.pt/ads/q-' + search + "/"
        if index != None:
            URL = URL + '?page=' + str(index)
        r = requests.get(URL)
        soup = BeautifulSoup(r.content, 'html5lib')

        page = soup.find('div', attrs = {'class':'hasPromoted section clr'})
        result = None
        if(page != None):
            result = getProducts(page,search,soup)
        return result

def search_pageWithNumber(search,index):
    if __name__ != "__main__":
        URL = 'https://www.olx.pt/ads/q-' + search + "/"
        if index != None:
            URL = URL + '?page=' + str(index)
        r = requests.get(URL)
        soup = BeautifulSoup(r.content, 'html5lib')

        return soup

def buildProduct(productRAW):
    if __name__ != "__main__":
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

        product['name'] = name
        product['price'] = price.split(" ")[0]
        product['negotiable'] = isNegotiable
        product['date'] = date
        product['url'] = productRAW.find('a')['href']
        product['img'] = productRAW.find('img')['src'] if productRAW.find('img') != None else 'NO IMAGE'
        product['location'] = location
        return product    

def getProducts(page,userSearch,soup):
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

        products = { 'trade': [],'buy': [] }

        productList = soup.find('table', attrs = {'id':'offers_table'})

        # Cycle all the adds and builds the product objects
        offer = productList.find('div', attrs = {'class':'offer-wrapper'})
        product = buildProduct(offer)
        if (product['price'] == "Troca"):
            products['trade'].append(product)
        else:
            products['buy'].append(product)
        
        isLastProduct = False
        while isLastProduct == False:
            offer = offer.findNext('div', attrs = {'class':'offer-wrapper'})
            if offer == None:
                isLastProduct = True
            else:
                product = buildProduct(offer)
                if (product['price'] == "Troca"):
                    products['trade'].append(product)
                else:
                    products['buy'].append(product)
        # Cycle all the adds and builds the product objects

        print("page: " + str(1))

        if(numberOfPages > 1):
            for pageIndex in range(2, numberOfPages + 1):
                    soup = search_pageWithNumber(userSearch, pageIndex)
                    productList = soup.find('table', attrs = {'id':'offers_table'})

                    # Cycle all the adds and builds the product objects
                    offer = productList.find('div', attrs = {'class':'offer-wrapper'})
                    product = buildProduct(offer)
                    if (product['price'] == "Troca"):
                        products['trade'].append(product)
                    else:
                        products['buy'].append(product)
                    

                    isLastProduct = False
                    while isLastProduct == False:
                        offer = offer.findNext('div', attrs = {'class':'offer-wrapper'})
                        if offer == None:
                            isLastProduct = True
                        else:
                            product = buildProduct(offer)
                            if (product['price'] == "Troca"):
                                products['trade'].append(product)
                            else:
                                products['buy'].append(product)
                    # Cycle all the adds and builds the product objects

                    print("page: " + str(pageIndex))
                    if(pageIndex == numberOfPages):
                        break
                    else:
                        pageIndex = pageIndex + 1
        
        return products
