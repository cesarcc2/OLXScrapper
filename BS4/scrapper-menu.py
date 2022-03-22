
from models.models import Search, Product
import autoRun
import runOnce
from prettytable import PrettyTable
import dataBase.database as db
import utils



# 
#----------------------- MAIN -------------------
# 
close = False

while close != True:
        print("")
        print("1- Run Once")
        print("2- Auto Run")
        print("3- List Search Terms")
        print("4- Add Search Term")
        print("5- Remove Search Term")
        print("6- Print Menu")
        print("0- Exit")
        print("")

        userOption = input('Do something dude : ')

        if (userOption == str(1)):
                runOnce.start()
        elif (userOption == str(2)):
                autoRun.start()
        elif (userOption == str(3)):
                db.getSearches()
                print("")
                input('Press ENTER to exit to the menu')
        elif (userOption == str(4)):
                print("")
                transcript = input("Gimme the damn search: ")
                minPrice = input("Min Price: ")
                maxPrice = input("Max Price: ")
                optimalPrice = input("Optimal Price: ")
                reply = None
                while reply not in ("", "y", "n"):
                        reply = input("Do you want tradables? (y/n)").lower()
                        allowTradable = (reply in ("", "y"))
                reply = None
                while reply not in ("", "y", "n"):
                        reply = input("Only negotiables? (y/n)").lower()
                        onlyNegotiables = (reply in ("", "y"))
                search = Search(transcript, utils.formatNumber(float(minPrice)), utils.formatNumber(float(maxPrice)), utils.formatNumber(float(optimalPrice)), allowTradable, onlyNegotiables)



                db.insertSearch(search)
        elif (userOption == str(5)):
                db.getSearches()
                print("")
                searchToDelete = input("I love to delete stuff!! Give me the id: ")
                print("")
                confirmation = input("But are you sure?? (y/n)")
                if (confirmation == "y"):
                        db.deleteSearch(searchToDelete)
                else:
                        print("")
                        print("I guess I aint having fun today... ")
        elif (userOption == str(6)):                
                printMenuClose = False
                while printMenuClose != True:
                        print("")
                        print("1- Results")
                        print("2- Result by Search ID")
                        print("3- Filtered")
                        print("4- Filtered by Search ID")
                        print("5- Optimal")
                        print("6- Optimal by Search ID")
                        print("0- Back")
                        print('')
                        printUserInput = input("Choose :")
                        print('')
                        if(printUserInput == str(1)):
                                searches = db.getAllSearchResult()
                                allResultsTable = PrettyTable()
                                allResultsTable.field_names = ["id", "name", "price", "date", "location", "tradable", "url"]
                                for search in searches:
                                        product:Product = search
                                        allResultsTable.add_row([product.id,product.name,product.price,product.date,product.location,product.tradable,product.url])
                                print(allResultsTable)
                                print('')
                                input('ENTER to continue')
                        elif(printUserInput == str(2)):
                                db.getSearches()
                                id = input("Give me the id: ")
                                searches = db.getResultsBySearchId(id)
                                print('')
                                allResultsTable = PrettyTable()
                                allResultsTable.field_names = ["id", "name", "price", "date", "location", "tradable", "url"]
                                for search in searches:
                                        product:Product = search
                                        allResultsTable.add_row([product.id,product.name,product.price,product.date,product.location,product.tradable,product.url])
                                print(allResultsTable)
                                print('')
                                input('ENTER to continue')
                        elif(printUserInput == str(3)):
                                searches = db.getAllFiltered()
                                print('')
                                allFilteredTable = PrettyTable()
                                allFilteredTable.field_names = ["id", "name", "price", "date", "location", "tradable", "url"]
                                for search in searches:
                                        product:Product = search
                                        allFilteredTable.add_row([product.id,product.name,product.price,product.date,product.location,product.tradable,product.url])
                                print(allFilteredTable)
                                print('')
                                input('ENTER to continue')
                        elif(printUserInput == str(4)):
                                db.getSearches()
                                id = input("Give me the id: ")
                                searches = db.getFilteredBySearchId(id)
                                print('')
                                allResultsTable = PrettyTable()
                                allResultsTable.field_names = ["id", "name", "price", "date", "location", "tradable", "url"]
                                for search in searches:
                                        product:Product = search
                                        allResultsTable.add_row([product.id,product.name,product.price,product.date,product.location,product.tradable,product.url])
                                print(allResultsTable)
                                print('')
                                input('ENTER to continue')
                        elif(printUserInput == str(5)):
                                searches = db.getAllOptimal()
                                print('')
                                allOptimalTable = PrettyTable()
                                allOptimalTable.field_names = ["id", "name", "price", "date", "location", "tradable", "url"]
                                for search in searches:
                                        product:Product = search
                                        allOptimalTable.add_row([product.id,product.name,product.price,product.date,product.location,product.tradable,product.url])
                                print(allOptimalTable)
                                print('')
                                input('ENTER to continue')
                        elif(printUserInput == str(6)):
                                db.getSearches()
                                id = input("Give me the id: ")
                                searches = db.getOptimalBySearchId(id)
                                print('')
                                allResultsTable = PrettyTable()
                                allResultsTable.field_names = ["id", "name", "price", "date", "location", "tradable", "url"]
                                for search in searches:
                                        product:Product = search
                                        allResultsTable.add_row([product.id,product.name,product.price,product.date,product.location,product.tradable,product.url])
                                print(allResultsTable)
                                print('')
                                input('ENTER to continue')
                        elif(printUserInput == str(0)):
                                printMenuClose = True
                        else:
                                print('')
                                print('Wrong input')
                                print('')

        elif (userOption == str(0)):
                print("")
                print("Bye sucka!")
                close = True
        else:
                print("")
                print("wrong choice,loser! Start over, I dont have time to fix your mistakes")