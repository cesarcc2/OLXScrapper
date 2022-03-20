import utils
import services.firebaseService as firebaseService
import time
from time import sleep
import repeatedTimer


def loop():
    if __name__ != "__main__":
        print("")
        print("Restarting Scraping!")
        print("")
        searches = firebaseService.getSearches()

        for search in searches:
            print("Searching:   " + search)
            products = utils.search_page(search)
            firebaseService.saveProducts(products,search)
            print(str(len(products['buy']) + len(products['trade'])) +' results.')
            print("")

def start():
    if __name__ != "__main__":
        print("")
        print("Auto run? You lazy fuck")
        print("")

        loopsFinished = 1;
        while True:
            loop()

            print("Loops done so far:   " + str(loopsFinished))
            time.sleep(60*10)
            loopsFinished = loopsFinished + 1
