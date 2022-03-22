from models.models import Search
import utils
import dataBase.database as db

def start():
    if __name__ == "runOnce":
        print("")
        transcript = input("Gimme the damn search : ")
        searchOBJ = Search(transcript,0,0,0,True,False)
        products = utils.search_page(searchOBJ)

        if(products != None):
            db.insertSearchResult(products,searchOBJ.transcript)
        else:
            print('No Results! Sorry')
            print("")

        input('Press ENTER to exit to the menu')

