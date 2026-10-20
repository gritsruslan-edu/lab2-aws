from datetime import date, timedelta
import csv
import boto3
import requests

AWS_ACCESS_KEY_ID = "_"
AWS_SECRET_ACCESS_KEY = "_"
AWS_REGION_NAME = "eu-north-1"
S3_BUCKET_NAME = "gritsruslan-sumdu-s3-bucket"
LOCAL_FILE_PATH = "nbu_rates_2022.csv"

data = []
current_date = date(2022, 1, 1)
end_date = date(2022, 12, 31)

while current_date <= end_date:
    date_str = current_date.strftime("%Y%m%d")
    url = f"https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?date={date_str}&json"
    response = requests.get(url).json()
    for item in response:
        if item.get("cc") in ["USD", "EUR"]:
            data.append(
                {
                    "date": item.get("exchangedate"),
                    "currency": item.get("cc"),
                    "rate": item.get("rate"),
                }
            )
    current_date += timedelta(days=1)

with open(LOCAL_FILE_PATH, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["date", "currency", "rate"])
    writer.writeheader()
    writer.writerows(data)

s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION_NAME,
)

s3_client.upload_file(LOCAL_FILE_PATH, S3_BUCKET_NAME, LOCAL_FILE_PATH)