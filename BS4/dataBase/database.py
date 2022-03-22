from xml.dom.minidom import Document
from tinydb import TinyDB, Query, where
from tinydb.operations import delete
from prettytable import PrettyTable
from models.models import Product, Search
import json 

query = Query()


DB = TinyDB('DB.json')
SEARCH = DB.table("search")
RESULTS = DB.table("results")
FILTERED = DB.table("filtered")
OPTIMAL = DB.table("optimal")

def insertSearch(search: Search):
    if __name__ != "__main__":
        SEARCH.upsert(search.toJSON(), query['transcript'] == search.transcript)

def insertSearchResult(products: list,search:Search):
    if __name__ != "__main__":
        for product in products:
            product:Product = product
            searchResults = { 
                'search': search.id,
                'product': product.toJSON()
            }
            if not(RESULTS.contains(query['product']['id'] == product.id)):
                RESULTS.insert(searchResults)
            print(product.name + "  |   " + str(product.price) + "  |   " + product.date + "  |   " + str(product.negotiable))

def updateFiltered(filtered):
    if __name__ != "__main__":
        FILTERED.upsert(filtered, query['search'] == filtered['search'])

def updateOptimal(optimal):
    if __name__ != "__main__":
        OPTIMAL.upsert(optimal, query['search'] == optimal['search'])



def getSearches()->list:
    if __name__ != "__main__":
        searchesRAW = SEARCH.all()
        searches: list = []
        searchesTable = PrettyTable()
        searchesTable.field_names = ["id", "transcript", "minPrice", "maxPrice", "optimalPrice", "allowTradable", "onlyNegotiables"]
        for s in searchesRAW:
            search = Search(s['transcript'],s['minPrice'],s['maxPrice'],s['optimalPrice'],s['allowTradable'],s['onlyNegotiables'],s['id'])
            searchesTable.add_row([search.id,search.transcript,search.minPrice,search.maxPrice,search.optimalPrice,search.allowTradable,search.onlyNegotiables])
            searches.append(search)
        print(searchesTable)
        return searches

def deleteSearch(searchId):
    if __name__ != "__main__":
        SEARCH.remove(where('id') == searchId)



def getResultsBySearchId(searchId)-> list:
    if __name__ != "__main__":
        results = RESULTS.search(query['search'] == searchId)
        products: list = []
        for result in results:
            product = result['product']
            product = Product(product['name'],product['price'],product['tradable'],product['negotiable'],product['date'],product['url'],product['img'],product['location'])
            products.append(product)
        sort = sorted(products, key=lambda x: x.price, reverse=True)
        return sort
            

def getAllSearchResult():
    if __name__ != "__main__":
        searches = RESULTS.all()
        products: list = []
        for result in searches:
            product = result['product']
            product = Product(product['name'],product['price'],product['tradable'],product['negotiable'],product['date'],product['url'],product['img'],product['location'])
            products.append(product)
        sort = sorted(products, key=lambda x: x.price, reverse=True)
        return sort

def getProductById(id:str)->Product:
    result = RESULTS.search(query['product']['id'] == id)[0]
    product = Product(result['product']['name'], result['product']['price'], result['product']['tradable'], result['product']['negotiable'], result['product']['date'], result['product']['url'], result['product']['img'], result['product']['location'])
    return product

def getAllFiltered():
    if __name__ != "__main__":
        searches = FILTERED.all()
        products = []
        for search in searches:
            if(len(search['products']) != 0):
                for productId in search['products']:
                    product:Product = getProductById(productId)
                    if(product != []):
                        products.append(product)
        sort = sorted(products, key=lambda x: x.price, reverse=True)
        return sort

def getFilteredBySearchId(searchID):
    if __name__ != "__main__":
        searches = FILTERED.all()
        products = []
        for search in searches:
            if(len(search['products']) != 0 and search['search'] == searchID):
                for productId in search['products']:
                    product:Product = getProductById(productId)
                    if(product != []):
                        products.append(product)
        sort = sorted(products, key=lambda x: x.price, reverse=True)
        return sort


def getAllOptimal():
    if __name__ != "__main__":
        searches = OPTIMAL.all()
        products = []
        for search in searches:
            if(len(search['products']) != 0):
                for productId in search['products']:
                    product:Product = getProductById(productId)
                    if(product != []):
                        products.append(product)
        sort = sorted(products, key=lambda x: x.price, reverse=True)
        return sort

def getOptimalBySearchId(searchID):
    if __name__ != "__main__":
        searches = OPTIMAL.all()
        products = []
        for search in searches:
            if(len(search['products']) != 0 and search['search'] == searchID):
                for productId in search['products']:
                    product:Product = getProductById(productId)
                    if(product != []):
                        products.append(product)
        sort = sorted(products, key=lambda x: x.price, reverse=True)
        return sort