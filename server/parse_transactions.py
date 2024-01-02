import xlrd
from pathlib import Path
from sqlalchemy import insert

from db import SessionLocal
from db.models import Transaction
from schema import TransactionCreateSchema


DATE_FORMAT_USED_IN_DUMP = "%d/%m/%y"


def parse_transactions(transactions_xls_file_path: str):
    """Given xls file of transactions, parse out the transactions"""
    print("-" * 150)
    print(f'PARSING "{transactions_xls_file_path}" file')
    print("-" * 150)

    book = xlrd.open_workbook(transactions_xls_file_path)
    sheet = book.sheet_by_index(0)

    transaction_entries_start_idx: int = -1
    transaction_entries_end_idx: int = -1
    # label_row_idx: int = -1
    # inside_transaction_section: bool = False

    for idx, row in enumerate(sheet.get_rows()):
        # row is a list with xlrd.sheet.Cell objects
        first_cell: xlrd.sheet.Cell = row[0]

        # ignore lines that dont start with asterisk,
        # asterisk lines are markers for the transaction rows starting and ending
        if not first_cell.value.startswith("*"):
            continue

        # check if this is start of list of transactions
        row_values = sheet.row_values(idx)
        filtered_row_values = list(filter(lambda cell: cell != "", row_values))

        # start and end of the transaction list has *** in each cell
        # after filtering out empty cells, if the length of the list is same as original,
        # it means all cells have text (and these will be asterisks according to the format)
        # store these row numbers
        if len(row_values) == len(filtered_row_values):
            if transaction_entries_start_idx == -1:
                transaction_entries_start_idx = idx + 1
                # label_row_idx = idx - 1

            else:
                # there's a blank line before the asterisk line
                transaction_entries_end_idx = idx - 2
                break

    transactions = []

    for idx, row in enumerate(sheet.get_rows()):
        if transaction_entries_start_idx <= idx <= transaction_entries_end_idx:
            values = sheet.row_values(idx)
            (
                date,
                description_from_bank,
                reference_id,
                value_date,
                withdraw_amount,
                deposit_amount,
                closing_balance,
            ) = values

            transaction = TransactionCreateSchema(
                date=date,
                description_from_bank=description_from_bank,
                reference_id=reference_id,
                value_date=value_date,
                withdraw_amount=withdraw_amount if withdraw_amount else 0.0,
                deposit_amount=deposit_amount if deposit_amount else 0.0,
                closing_balance=closing_balance,
            )

            transactions.append(transaction.model_dump())

    with SessionLocal() as session:
        session.execute(insert(Transaction).values(transactions))
        session.commit()


if __name__ == "__main__":
    print("parsing last downloaded transactions sheet")
    transactions_dir = Path.cwd() / "transaction_lists"
    latest_downloaded_file_path = list(
        sorted(transactions_dir.iterdir(), key=lambda file: file.name, reverse=True)
    )[0]
    parse_transactions(transactions_xls_file_path=str(latest_downloaded_file_path))
