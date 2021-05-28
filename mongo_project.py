import os
import pymongo
if os.path.exists("env.py"):
    import env


# constants
MONGO_URI = os.environ.get("MONGO_URI")
DATABASE = "myFirstDB"
COLLECTION = "celebs"


def mongo_connect(url):
    try:
        conn = pymongo.MongoClient(url)
        return conn

    except pymongo.errors.ConnectionFailure as e:
        print("Could not connect to MongoDB: %s") % e


def show_menu():
    print("")
    print("1. Add a record")
    print("2. Find a record by name")
    print("3. Edit a record")
    print("4. Delete a record")
    print("5. Exit the menu")

    option = input("Enter option: ")
    return option


def get_record():   
    print("")
    first = input("Enter First Name >> ")
    last = input("Enter Last Name >> ")

    try:
        doc = coll.find_one({ "first": first.lower(), "last": last.lower()})
    except:
        print("Error accessing the database")

    if not doc:
        print("")
        print("Error! no results")
    return doc

def add_record():
    print("")
    first = input("Enter First Name >> ")
    last = input("Enter Last Name >> ")
    dob = input("Enter DOB >> ")
    gender = input("Enter Gender >> ")
    hair_colour = input("Enter Hair Colour >> ")
    occupation = input("Enter Occupation >> ")
    nationality = input("Enter Nationality >> ")

    # dictionary which will insert into DB
    new_doc = {
        "first": first.lower(),
        "last": last.lower(),
        "dob": dob,
        "gender": gender,
        "hair_colour": hair_colour,
        "occupation": occupation,
        "nationality": nationality
    }
    
    try:
        coll.insert(new_doc)
        print("")
        print("Document inserted")
    except:
        print("Error accessing the database")


def main_loop():
    while True:
        option = show_menu()
        if option == "1":
            add_record()
        elif option == "2":
            print("You have selected option 2")
        elif option == "3":
            print("You have selected option 3")
        elif option == "4":
            print("You have selected option 4")
        elif option == "5":
            conn.close()
            break
        else:            
            print("Invalid option")
        print("")

# That will call our Mongo connection, and create our Mongo celebrities collection.
conn = mongo_connect(MONGO_URI)
coll = conn[DATABASE][COLLECTION]
# call main_loop() function, which will continue
# to display menu and process the options.
main_loop()