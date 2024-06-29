import psycopg2
import os


def save_transactions(event, context):
    transactions = event

    if not transactions:
        return "No transactions to process"

    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    DB_USERNAME = os.getenv("DB_USERNAME")
    DB_PASSWORD = os.getenv("DB_PASSWORD")

    try:
        print("connecting to DB....")
        connection = psycopg2.connect(
            user=DB_USERNAME,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
        )

        print("connected")

    except Exception as e:
        print(f"Error connecting to DB: {e}")
        raise e

    cursor = connection.cursor()

    reference_ids = [transaction.reference_id for transaction in transactions]
    cursor.execute(
        "SELECT * FROM bank_transaction WHERE reference_id = ANY(%s);", (reference_ids)
    )
    existing_transactions = cursor.fetchall()

    transactions_deduped = []
    for transaction in transactions:
        exists = False
        for already_present in existing_transactions:
            if (
                transaction.reference_id == already_present.reference_id
                and transaction.description_from_bank
                == already_present.description_from_bank
                and transaction.date == already_present.date
            ):
                exists = True
                break

        if exists:
            print(
                f"Transaction {transaction.reference_id} exists, skipping insertion..."
            )

        transactions_deduped.append(transaction)

    if not transactions_deduped:
        return "No new transactions to process"

    insert_stmt = """
        INSERT into bank_transaction
        VALUES (%(description_from_bank)s, %(reference_id)s, %(date)s, %(value_date)s, %(withdraw_amount)s, %(deposit_amount)s, %(closing_balance)s); 
    """
    cursor.execute(insert_stmt, transactions_deduped)
    connection.commit()

    print("closing connection")
    cursor.close()
    connection.close()

    return "Inserted transactions into DB"
