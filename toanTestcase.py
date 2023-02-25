
import datetime
import json

import application
import call
from contract import Contract
from customer import Customer
from phoneline import PhoneLine
from visualizer import Visualizer
def create_customers(log: dict[str, list[dict]]) -> list[Customer]:
    """ Returns a list of Customer instances for each customer from the input
    dataset from the dictionary <log>.

    Precondition:
    - The <log> dictionary contains the input data in the correct format,
    matching the expected input format described in the handout.
    """
    customer_list = []
    for cust in log['customers']:
        customer = Customer(cust['id'])
        for line in cust['lines']:
            # TODO:
            # comment out the following three lines of code only when you get
            # to implement task 3. These lines are provided as a placeholder so
            # that your visualization works when you have only completed up to
            # and including task 2. Never instantiate the abstract class
            # "Contract" as below.
            # Remove this TODO list when you're done.
            contract = Contract(datetime.datetime.now())
            contract.new_month = lambda *args: None
            contract.bill_call = lambda *args: None
            # TODO:
            # 1) Uncomment the piece of code below once you've implemented
            #    all types of contracts.
            # 2) Make sure to import the necessary contract classes in this file
            #    and remove any unused imports to pass PyTA.
            # 3) Do not change anything in the code below besides uncommenting it
            # 4) Remove this TODO list when you're done.
            """
            contract = None
            if line['contract'] == 'prepaid':
                # start with $100 credit on the account
                contract = PrepaidContract(datetime.date(2017, 12, 25), 100)
            elif line['contract'] == 'mtm':
                contract = MTMContract(datetime.date(2017, 12, 25))
            elif line['contract'] == 'term':
                contract = TermContract(datetime.date(2017, 12, 25),
                                        datetime.date(2019, 6, 25))
            else:
                print("ERROR: unknown contract type")
            """

            line = PhoneLine(line['number'], contract)
            customer.add_phone_line(line)
        customer_list.append(customer)
    return customer_list

def import_data() -> dict[str, list[dict]]:
    """ Open the file <dataset.json> which stores the json data, and return
    a dictionary that stores this data in a format as described in the A1
    handout.

    Precondition: the dataset file must be in the json format.
    """
    with open("dataset.json") as o:
        log = json.load(o)
        return log

def process_event_history(log: dict[str, list[dict]],
                          customer_list: list[Customer]) -> None:
    """ Process the calls from the <log> dictionary. The <customer_list>
    list contains all the customers that exist in the <log> dictionary.

    Construct Call objects from <log> and register the Call into the
    corresponding customer's call history.

    Hint: You must advance all customers to a new month using the new_month()
    function, everytime a new month is detected for the current event you are
    extracting.

    Preconditions:
    - All calls are ordered chronologically (based on the call's date and time),
    when retrieved from the dictionary <log>, as specified in the handout.
    - The <log> argument guarantees that there is no "gap" month with zero
    activity for ALL customers, as specified in the handout.
    - The <log> dictionary is in the correct format, as defined in the
    handout.
    - The <customer_list> already contains all the customers from the <log>.
    """
    # TODO: Implement this method. We are giving you the first few lines of code
    billing_date = datetime.datetime.strptime(log['events'][0]['time'],
                                              "%Y-%m-%d %H:%M:%S")
    billing_month = billing_date.month
    #print(billing_month)
    # start recording the bills from this date
    # for i in log['events']:
    #     if i['type'] == 'call':
    #         print(i)
    #for i in customer_list:
        #print(i)
    for i in log['events']:
        if i['type'] == 'call':
            date = datetime.datetime.strptime(i['time'],"%Y-%m-%d %H:%M:%S")

            tempcall = call.Call(i['src_number'],i['dst_number'],date,
                                 i['duration'],i['src_loc'],i['dst_loc'])
            if i['src_number'] == application.find_customer_by_number(i['src_number'],customer_list):
                Customer.make_call(tempcall)
            elif i['dst_number'] == application.find_customer_by_number(i['src_number'],customer_list):
                Customer.receive_call(tempcall)
            if date.month > billing_month:
                new_month(customer_list,date.month,date.year)
                billing_month = date.month
                #print('hits',date.month)
            #print("time", i['time'], type(i['time'])
            #print("Month: ", tempcall.time.month, "Year: ", tempcall.time.year)

def new_month(customer_list: list[Customer], month: int, year: int) -> None:
    """ Advance all customers in <customer_list> to a new month of their
    contract, as specified by the <month> and <year> arguments.
    """
    for cust in customer_list:
        cust.new_month(month, year)
    # Note: uncomment the following lines when you're ready to implement this
    #
    # new_month(customer_list, billing_date.month, billing_date.year)
    #
    # for event_data in log['events']:
    #
    # ...
import callhistory
def main():
    input_dictionary = import_data()
    customers = create_customers(input_dictionary)
    process_event_history(input_dictionary, customers)

    #print(input_dictionary['events'])
main()