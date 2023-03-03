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
from math import ceil
from typing import Optional

from bill import Bill
from call import Call


# Constants for the month-to-month contract monthly fee and term deposit
MTM_MONTHLY_FEE = 50.00
TERM_MONTHLY_FEE = 20.00
TERM_DEPOSIT = 300.00

# Constants for the included minutes and SMSs in the term contracts (per month)
TERM_MINS = 100

# Cost per minute and per SMS in the month-to-month contract
MTM_MINS_COST = 0.05

# Cost per minute and per SMS in the term contract
TERM_MINS_COST = 0.1

# Cost per minute and per SMS in the prepaid contract
PREPAID_MINS_COST = 0.025


class Contract:
    """ A contract for a phone line

    This class is not to be changed or instantiated. It is an Abstract Class.

    === Public Attributes ===
    start:
         starting date for the contract
    bill:
         bill for this contract for the last month of call records loaded from
         the input dataset
    """
    start: datetime.date
    bill: Optional[Bill]

    def __init__(self, start: datetime.date) -> None:
        """ Create a new Contract with the <start> date, starts as inactive
        """
        self.start = start
        self.bill = None

    def new_month(self, month: int, year: int, bill: Bill) -> None:
        """ Advance to a new month in the contract, corresponding to <month> and
        <year>. This may be the first month of the contract.
        Store the <bill> argument in this contract and set the appropriate rate
        per minute and fixed cost.

        DO NOT CHANGE THIS METHOD
        """
        raise NotImplementedError

    def bill_call(self, call: Call) -> None:
        """ Add the <call> to the bill.

        Precondition:
        - a bill has already been created for the month+year when the <call>
        was made. In other words, you can safely assume that self.bill has been
        already advanced to the right month+year.
        """
        self.bill.add_billed_minutes(ceil(call.duration / 60.0))

    def cancel_contract(self) -> float:
        """ Return the amount owed in order to close the phone line associated
        with this contract.

        Precondition:
        - a bill has already been created for the month+year when this contract
        is being cancelled. In other words, you can safely assume that self.bill
        exists for the right month+year when the cancelation is requested.
        """
        self.start = None
        return self.bill.get_cost()


# TODO: Implement the MTMContract, TermContract, and PrepaidContract
class TermContract(Contract):
    def __init__(self, start: datetime.date(2017, 12, 25), end: datetime.date(2019, 6, 25)) -> None:
        """ Create a new Contract with the <start> date, starts as inactive
        """
        self.start = start
        self.end = end
        self.bill = None
        print("constructor invoked, created a TermContract object")

    def new_month(self, month: int, year: int, bill: Bill) -> None:
        """ Advance to a new month in the contract, corresponding to <month> and
                <year>. This may be the first month of the contract.
                Store the <bill> argument in this contract and set the appropriate rate
                per minute and fixed cost.
        """
        # self.start.month = month
        # self.start.year = year
        bill.set_rates('TERM',TERM_MINS_COST)
        bill.add_fixed_cost(TERM_DEPOSIT+TERM_MONTHLY_FEE)
        bill.add_free_minutes(TERM_MINS)

    def cancel_contract(self) -> float:
        self.start = None
        # if

    #def cancel_contract(self) -> float:

class MTMContract(Contract):
    def __init__(self, start: datetime.date(2017, 12, 25)) -> None:
        self.start = start
        self.bill = None

    def new_month(self, month: int, year: int, bill: Bill) -> None:
        """ Advance to a new month in the contract, corresponding to <month> and
                <year>. This may be the first month of the contract.
                Store the <bill> argument in this contract and set the appropriate rate
                per minute and fixed cost.
        """
        pass

class PrepaidContract(Contract):
    def __init__(self, start: datetime.date(2017, 12, 25),balance) -> None:
        self.start = start
        self.balance = balance
        self.bill = None

    def new_month(self, month: int, year: int, bill: Bill) -> None:
        pass



if __name__ == '__main__':
    testContract = TermContract(datetime.date(2017, 12, 25),datetime.date(2019, 6, 25))
    testBill = Bill()
    testContract.new_month(1,2018,testBill)

    '''import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': [
            'python_ta', 'typing', 'datetime', 'bill', 'call', 'math'
        ],
        'disable': ['R0902', 'R0913'],
        'generated-members': 'pygame.*'
    })
    '''
