import utils
import services.firebaseService as firebaseService

def start():
    if __name__ == "runOnce":
        print("")
        userSearch = input("Gimme the damn search : ")
        products = utils.search_page(userSearch)

        if(products != None):
            firebaseService.saveProducts(products,userSearch)
        else:
            print('No Results! Sorry')
            print("")

        input('Press ENTER to exit to the menu')

