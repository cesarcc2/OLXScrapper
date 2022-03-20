import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

def setupFB():
    cred = credentials.Certificate('BS4/services/firebaseData.json')
    firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://olx-pt-scrapper-default-rtdb.europe-west1.firebasedatabase.app/'
    })
    DB = db.reference('/')

def saveProducts(products,userSearch):
    db.reference('/products').child(userSearch).set({
        "search" : userSearch,
        "products" : {
            "buy" : products['buy'],
            "trade" : products['trade']
        }
        })

def saveSearch(search):
    db.reference('/searches').child(search).set({
        "search" : search
        })

def deleteSearch(search):
    db.reference('/searches').child(search).delete()

def getSearches():
    searchesArray = []
    searches = db.reference('/searches').get()
    print("")
    print("Currently Searching: ")
    print("")
    if(searches != None):
        for search in searches:
            print(search)
            searchesArray.append(search)
    return searchesArray