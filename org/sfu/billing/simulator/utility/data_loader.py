import csv, random, string
import configparser
import os

def load_properties():
    config_dir = os.environ.get('APP_HOME')
    config_fileName = ('config.ini')
    config_file = config_dir + os.sep + config_fileName
    return config_file,config_dir
#Creates a customer instance with a constructor;
#Parameters: customer's phone number, receiver's phone number, location of the caller, location of the receiver
class Customer:
    'Common base class for all customer'
    customer_count = 0

    def __init__(self, caller, receiver, origin, destination):
        self.caller = caller
        self.receiver = receiver
        self.origin = origin
        self.destination = destination
        Customer.customer_count += 1

    def displayCount(self):
        print("Total Customer" + str(Customer.customer_count))

    def displayCustomer(self):
        print(" Phone: " + str(self.caller))

#loads cell tower locations from csv file; returns a list of latitude and longitude
def load_locations():
    config = configparser.ConfigParser()
    config_file,config_dir = load_properties()
    config.read(config_file)
    cell_tower_locations_dir = config_dir +'/docs/'+ config['SIMULATOR']['CELL_TOWER_LOCATIONS']
    locations_list = dict()
    with open(cell_tower_locations_dir, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            locations_list[line_count] = row['nodeId']
            line_count += 1
    return locations_list,line_count

#1. Creates empty customer list
#2. Loads cell tower location and location count
#3. Loads customer list csv file
#4. Generates random index using the location count as range
#5. Selects source and destination location (latitude and longitude)
#6. Creates an alpha numeric value of length 8 and adds the linecount as the last two character ie. customer_id
#7. Creates a customer instance using the values created in above steps and stores it in a dictionary and returns it

def load_customer():
    config = configparser.ConfigParser()
    config_file, config_dir = load_properties()
    config.read(config_file)
    customer_list_dir = config_dir + '/docs/' + config['SIMULATOR']['CUSTOMER_LIST']
    customer_list = dict()
    locations,location_count = load_locations()
    with open(customer_list_dir, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            sindex = random.randint(0,location_count-1)
            source = locations[sindex]
            dindex = random.randint(0,location_count-1)
            destination = locations[dindex]
            # alpa_id = ''.join(random.choice(string.ascii_uppercase) for _ in range(8))
            # customer_list[line_count] = Customer(alpa_id + str("%02d" % (line_count,)), row["caller"], row["reciever"],
            #                                      source,destination)
            customer_list[line_count] = Customer(row["caller"], row["reciever"],
                                                 source, destination)
            line_count += 1
    return customer_list

#
# if __name__ == "__main__":
#     print(load_customer())