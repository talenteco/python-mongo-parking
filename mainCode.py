import json
from connectToDB import connectToMongo

def findParkingSpace(values):
    parkingSpace=-1
    for i in range(1, 3):
        if(i not in values):
            parkingSpace = i
            break
    
    return(parkingSpace)


def retrieveParkingValue(carIdentifier, collection):
    if(collection.count_documents({'car_identifier' : carIdentifier})>0):
        currentParkingSpot = {}
        for i in collection.find({'car_identifier' : carIdentifier}):
            currentParkingSpot = i

        print("Your car's Parking spot level and number is : " + json.dumps(currentParkingSpot['parking_details']))
        print("Would you like to unpark your car?(Type 'Yes' to unpark,  any other input will keep the car parked)")
        userInput = input().upper().strip()
        if(userInput == 'YES'):
            return(True)
        else:
            return(-1)
    
    else:
        print("Car is not parked. Would you like to park it?(Type 'Yes' to park, any other input will keep the car unparked)")
        userInput = input().upper().strip()
        if(userInput == 'YES'):
            return(False)
        else:
            return(-1)


def storeParkingValue(carIdentifier, collection, finalDecision):
    if(finalDecision == "PARK"):
        values=[]
        for i in collection.find():
            values.append(i['parking_details']['spot_number'])
        
        parkingSpaceFinalValue = findParkingSpace(values)

        if(parkingSpaceFinalValue != -1):
            parking_level = 'A' if(parkingSpaceFinalValue<21) else 'B'

            final_car_parking_details = {'car_identifier':carIdentifier, 'parking_details':{'parking_level': parking_level, 'spot_number': parkingSpaceFinalValue}}
            collection.insert_one(final_car_parking_details)
            print("Your car has been parked, Thank you!")
        
        else:
            print("Sorry, the parking space is currently full. Remove a car first before proceeding to park!")

    else:
        collection.delete_one({'car_identifier' : carIdentifier})
        print("Your car has been unparked, Thank you!")


def userInteract():

    print("Hello! And welcome to The Parking Space, please enter your car's unique identification number below:")

    carNumber = input().upper().strip()

    if(len(carNumber)==0) or (carNumber.isspace()):
        carNumber=False

    return(carNumber)


def main():
    client = connectToMongo()
    database = client['parking_db']
    collection = database['parking_details']
    carNumber = userInteract() #calls function userInteract which is responsible for retrieving a car's
                   #unique identification.


    if(carNumber):#Only for a valid input for the car identifier, we will proceed with the functions.
                  #Invalid inputs are blank spaces or empty inputs.
    
    
        result = retrieveParkingValue(carNumber, collection) #Finds if a car is parked by searching through documents
                                                          # Returns True if car is parked, False otherwise.
    
        if(result == True):
            decision = "UNPARK"  
        elif(result == False):
            decision = "PARK"
        if(result==-1):
            decision = -1
            print('Your car remains as is!')

        if(decision != -1):
            storeParkingValue(carNumber, collection, decision) #Takes the values and decides to insert/delete the document
                                                       #based on the value of the 'decision' variable. Decision variable is set to "PARK"
                                                       #if we dont find the car in the documents in the database.

    else:
        print("Invalid Input, Please Try Again!")

    client.close()#closing MongoDB connection

if __name__ == "__main__":
    main()