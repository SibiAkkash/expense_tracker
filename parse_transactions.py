import pandas as pd
import xlrd

from dataclasses import dataclass
from pprint import pprint
import datetime


@dataclass
class Transaction:
    date: datetime.date
    narration: str
    reference_id: str
    value_date: datetime.date
    withdraw_amount: float
    deposit_amount: float
    closing_balance: float    
    
    def __repr__(self):
        output = f'date = {self.date.strftime("%d/%m/%y")}\ntransaction_ref = {self.reference_id}\ndescription: {self.narration}\n'
        # show whether amount was withdrawn or deposited
        if self.deposit_amount == 0:
            output += f'withdrew: Rs {self.withdraw_amount}\n'
        if self.withdraw_amount == 0:
            output += f'deposited: Rs {self.deposit_amount}\n'            
        # show closing balance too
        output += f'Closing balance: Rs {self.closing_balance}\n'
        return output
        


def parse_transactions(transactions_xls_file_path: str):
    """ Given xls file of transactions, parse out the transactions"""
    print('-'*150)
    print(f'PARSING "{transactions_xls_file_path}" file')
    print('-'*150)
    
    
    book = xlrd.open_workbook(transactions_xls_file_path)
    sheet = book.sheet_by_index(0)

    transaction_entries_start_idx: int = -1
    transaction_entries_end_idx: int = -1
    label_row_idx: int = -1

    inside_transaction_section: bool = False

    for idx, row in enumerate(sheet.get_rows()):
        # row is a list with xlrd.sheet.Cell objects
        first_cell: xlrd.sheet.Cell = row[0]
        
        # ignore lines that dont start with asterisk, 
        # asterisk lines are markers for the transaction rows starting and ending
        if not first_cell.value.startswith('*'):
            continue
        
        # check if this is start of list of transactions
        row_values          = sheet.row_values(idx)
        filtered_row_values = list(filter(lambda cell: cell != '', row_values))

        # start and end of the transaction list has *** in each cell
        # after filtering out empty cells, if the length of the list is same as original, 
        # it means all cells have text (and these will be asterisks according to the format)
        # store these row numbers
        if len(row_values) == len(filtered_row_values):
            if transaction_entries_start_idx == - 1:
                transaction_entries_start_idx = idx + 1
                label_row_idx = idx - 1
                
            else:
                # there's a blank line before the asterisk line
                transaction_entries_end_idx = idx - 2
                break

    
    # labels = sheet.row_values(label_row_idx)
    # print(labels, transaction_entries_start_idx + 1, transaction_entries_end_idx + 1)

    DATE_FORMAT_USED_IN_DUMP = "%d/%m/%y"    

    for idx, row in enumerate(sheet.get_rows()):
        if transaction_entries_start_idx <= idx <= transaction_entries_end_idx:
            values = sheet.row_values(idx)
            # convert dates to datetime objects
            values[0] = datetime.datetime.strptime(row[0].value, DATE_FORMAT_USED_IN_DUMP)
            values[3] = datetime.datetime.strptime(row[3].value, DATE_FORMAT_USED_IN_DUMP)
            # if withdraw or deposit amount is an empty str, store its value as 0
            if row[4].value == '': values[4] = 0.0
            if row[5].value == '': values[5] = 0.0
            # construct Transaction object
            transaction = Transaction(*values)
            pprint(transaction)
        