"""
CSC148, Winter 2023
Assignment 1

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2022 Bogdan Simion, Diane Horton, Jacqueline Smith
"""
import datetime
import json

import call
from contract import Contract, MTMContract, PrepaidContract, TermContract
from customer import Customer
from phoneline import PhoneLine
from visualizer import Visualizer


def import_data() -> dict[str, list[dict]]:
    """ Open the file <dataset.json> which stores the json data, and return
    a dictionary that stores this data in a format as described in the A1
    handout.

    Precondition: the dataset file must be in the json format.
    """
    with open("dataset.json") as o:
        log = json.load(o)
        return log


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

            contract = None
            if line['contract'] == 'prepaid':
                # start with $100 credit on the account
                contract = PrepaidContract(datetime.date(2017, 12, 25), 100)
            elif line['contract'] == 'mtm':
                contract = MTMContract(datetime.date(2017, 12, 25))
            elif line['contract'] == 'term':
                contract = TermContract(datetime.date(2018, 2, 25),
                                        datetime.date(2019, 6, 25))
            else:
                print("ERROR: unknown contract type")


            line = PhoneLine(line['number'], contract)
            customer.add_phone_line(line)
        customer_list.append(customer)
    return customer_list


def find_customer_by_number(number: str, customer_list: list[Customer]) \
        -> Customer:
    """ Return the Customer with the phone number <number> in the list of
    customers <customer_list>.
    If the number does not belong to any customer, return None.
    """
    cust = None
    for customer in customer_list:
        if number in customer:
            cust = customer
    return cust


def new_month(customer_list: list[Customer], month: int, year: int) -> None:
    """ Advance all customers in <customer_list> to a new month of their
    contract, as specified by the <month> and <year> arguments.
    """
    #print("calling method new_month for", month, year)
    for cust in customer_list:
        cust.new_month(month, year)


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
    # start recording the bills from this date
    # Note: uncomment the following lines when you're ready to implement this
    #
    # new_month(customer_list, billing_date.month, billing_date.year)
    #
    # for event_data in log['events']:
    #  
    # ...
    for i in log['events']:
        #print('hello')
        if i['type'] == 'call':

            date = datetime.datetime.strptime(i['time'],"%Y-%m-%d %H:%M:%S")

            temp_call = call.Call(i['src_number'],i['dst_number'],date,
                                 i['duration'],i['src_loc'],i['dst_loc'])

            customer_who_made_call = find_customer_by_number(i['src_number'], customer_list)
            customer_who_made_call.make_call(temp_call)

            customer_who_receive_call = find_customer_by_number(i['dst_number'],customer_list)
            customer_who_receive_call.receive_call(temp_call)

            if date.month > billing_month:
                new_month(customer_list, date.month, date.year)
                billing_month = date.month

            '''if i['src_number'] == find_customer_by_number(i['src_number'],customer_list):
                print('here')
                Customer.make_call(tempcall)
            elif i['dst_number'] == find_customer_by_number(i['src_number'],customer_list):
                Customer.receive_call(tempcall)
            if date.month > billing_month:
                new_month(customer_list,date.month,date.year)
                billing_month = date.month'''



if __name__ == '__main__':
    v = Visualizer()
    print("Toronto map coordinates:")
    print("  Lower-left corner: -79.697878, 43.576959")
    print("  Upper-right corner: -79.196382, 43.799568")

    input_dictionary = import_data()
    customers = create_customers(input_dictionary)
    process_event_history(input_dictionary, customers)

    print("\n================= MY TEST =====================")
    mrToan = find_customer_by_number("722-8592", customers)
    made_calls, received_call = mrToan.get_history()
    for an_out_going_call in made_calls:
        print(an_out_going_call)

    for i in range(1,13):
        print(mrToan.print_bill(i,2018))


    # ----------------------------------------------------------------------
    # NOTE: You do not need to understand any of the implementation below,
    # to be able to solve this assignment. However, feel free to
    # read it anyway, just to get a sense of how the application runs.
    # ----------------------------------------------------------------------

    # Gather all calls to be drawn on screen for filtering, but we only want
    # to plot each call only once, so only plot the outgoing calls to screen.
    # (Each call is registered as both an incoming and outgoing)
    all_calls = []
    for c in customers:
        hist = c.get_history()
        all_calls.extend(hist[0])
    print("\n-----------------------------------------")
    print("Total Calls in the dataset:", len(all_calls))

    # Main loop for the application.
    # 1) Wait for user interaction with the system and processes everything
    #    appropriately
    # 2) Take the calls from the results of the filtering and create the
    #    drawables and connection lines for those calls
    # 3) Display the calls in the visualization window
    events = all_calls
    while not v.has_quit():
        events = v.handle_window_events(customers, events)

        connections = []
        drawables = []
        for event in events:
            connections.append(event.get_connection())
            drawables.extend(event.get_drawables())

        # Put the connections on top of the other sprites
        drawables.extend(connections)
        v.render_drawables(drawables)

    import python_ta

    python_ta.check_all(config={
        'allowed-import-modules': [
            'python_ta', 'typing', 'json', 'datetime',
            'visualizer', 'customer', 'call', 'contract', 'phoneline'
        ],
        'allowed-io': [
            'create_customers', 'import_data'
        ],
        'generated-members': 'pygame.*'
    })
