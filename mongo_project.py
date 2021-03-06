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


def find_record():
    doc = get_record()
    if doc:
        print("")
        for k,v in doc.items():
            if k != "_id":
                print(k.capitalize() + ": " + v.capitalize())


def edit_record():
    doc = get_record()
    if doc:
        update_doc = {}
        print("")
        for k,v in doc.items():
            if k != "_id":
                update_doc[k] = input(k.capitalize() + "[" + v + "] > ")

                if update_doc[k] == "":
                    update_doc[k] = v
        try:
            coll.update_one(doc, {"$set": update_doc})
            print("")
            print("Document updated")
        except:
            print("Error accessing the database")    


def delete_record():
    doc = get_record()
    if doc:
        print("")
        for k,v in doc.items():
            if k != "_id":
                print(k.capitalize() + ": " + v.capitalize())

        print("")
        confirmation = input("Is this the document you wish to delete?\nY or N > ")
        print("")
        if confirmation.lower() == "y":
            try:
                coll.remove(doc)
                print("Document removed successfully!")
            except:
                print("Error accessing database")
        # do not wish to delete, N selection
        else:
            print("Document not deleted")


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
            find_record()
        elif option == "3":
            edit_record()
        elif option == "4":
            delete_record()
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