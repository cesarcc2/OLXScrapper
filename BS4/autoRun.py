from models.models import Product, Search
import utils
import time
import dataBase.database as db
import json

def getAllProducts(searches:list):
    if __name__ != "__main__":
        for search in searches:
            search:Search = search
            print("Searching:   " + search.transcript)
            products = utils.search_page(search)
            db.insertSearchResult(products,search)
            print(str(len(products)) +' results.')
            print("")

def buildData():
    if __name__ != "__main__":
        searches = db.getSearches()
        for search in searches:
            search: Search = search
            products = db.getResultsBySearchId(search.id)
            filteredProducts: list = []
            optimalProducts: list = []
            print('')
            print("Building Data for search: " + search.transcript)
            print('')
            for product in products:
                invalid = False
                product: Product = product
                if  (search.onlyNegotiables and not(product.negotiable)):
                    invalid = True
                if  (not(search.allowTradable) and product.tradable):
                    invalid = True
                if  (product.price <= float(search.minPrice) or float(search.maxPrice) <= product.price):
                    invalid = True
                if(product.tradable == False):
                    if  (float(search.optimalPrice) - 30 <= float(product.price) <= float(search.optimalPrice) + 30):
                        optimalProducts.append(product.id)
                    
                if(invalid == False):
                    filteredProducts.append(product.id)
            
            filteredSearch = {"search": search.id, "products": filteredProducts}
            db.updateFiltered(filteredSearch)
            optimalSearch = {"search": search.id, "products": optimalProducts}
            db.updateOptimal(optimalSearch)
                    
                


def loop():
    if __name__ != "__main__":
        print("")
        print("Restarting Scraping!")
        print("")

        getAllProducts(db.getSearches())

        buildData()


        

def start():
    if __name__ != "__main__":
        print("")
        print("Auto run? You lazy fuck")
        print("")

        loopsFinished = 1
        while True:
            loop()

            print("Loops done so far:   " + str(loopsFinished))
            time.sleep(60*10)
            loopsFinished = loopsFinished + 1
