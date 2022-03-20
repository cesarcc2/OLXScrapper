
import services.firebaseService as firebaseService
firebaseService.setupFB()
import autoRun
import runOnce



# 
#----------------------- MAIN -------------------
# 
close = False

while close != True:
    print("")
    print("1- Auto Run")
    print("2- Run Once")
    print("3- List Search Terms")
    print("4- Add Search Term")
    print("5- Remove Search Term")
    print("0- Exit")
    print("")

    userOption = input('Do something dude : ')

    if (userOption == str(1)):
            autoRun.start()
    elif (userOption == str(2)):
            runOnce.start()
    elif (userOption == str(3)):
            firebaseService.getSearches()
            print("")
            input('Press ENTER to exit to the menu')
    elif (userOption == str(4)):
            print("")
            userSearch = input("Gimme the damn search : ")
            firebaseService.saveSearch(userSearch)
    elif (userOption == str(5)):
            firebaseService.getSearches()
            print("")
            searchToDelete = input("I love to delete stuff!! Give me the name: ")
            print("")
            confirmation = input("But are you sure?? (y/n)")
            if (confirmation == "y"):
                firebaseService.deleteSearch(searchToDelete)
            else:
                print("")
                print("I guess I aint having fun today... ")
    elif (userOption == str(0)):
        print("")
        print("Bye sucka!")
        close = True;
    else:
        print("")
        print("wrong choice,loser! Start over, I dont have time to fix your mistakes")