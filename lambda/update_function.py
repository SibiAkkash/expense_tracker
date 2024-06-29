import os
import time
import boto3

from dotenv import load_dotenv
load_dotenv()


def wait_for_update(lambda_arn):
    function = client.get_function(FunctionName=lambda_arn)
    update_successful = function["Configuration"]["LastUpdateStatus"]

    while update_successful != "Successful":
        print("Function updating...")
        time.sleep(1)
        function = client.get_function(FunctionName=lambda_arn)
        update_successful = function["Configuration"]["LastUpdateStatus"]


LAMBDA_ARN = "arn:aws:lambda:ap-south-1:982695942133:function:lambda-rds-conn"

# SSO credentials from IAM Identity center
# Make sure an sso session with profile name "admin" is present and not expired
session = boto3.Session(profile_name="admin")

client = session.client(service_name="lambda")

# upload lambda package zip file
with open("./package.zip", "rb") as package_zip:
    print("Uploading lambda function...")
    function_update_resp = client.update_function_code(
        FunctionName=LAMBDA_ARN, ZipFile=package_zip.read()
    )

wait_for_update(LAMBDA_ARN)
print("Function code updated ✅")


print("Updating function config...")

function_config_update_resp = client.update_function_configuration(
    FunctionName=LAMBDA_ARN,
    Handler="handler.save_transactions",
    Timeout=8,
    Description="Lambda to receive scraped transactions, dedup and save them in the DB",
    Environment={
        "Variables": {
            "DB_HOST": os.getenv("PROD_DB_HOST"),
            "DB_PORT": os.getenv("PROD_DB_PORT"),
            "DB_USERNAME": os.getenv("PROD_DB_USERNAME"),
            "DB_PASSWORD": os.getenv("PROD_DB_PASSWORD"),
            "DB_NAME": os.getenv("PROD_DB_NAME"),
        }
    },
    Runtime="python3.10",
)

wait_for_update(LAMBDA_ARN)
print("Function config updated ✅")
