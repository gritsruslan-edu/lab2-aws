import io
import boto3
import matplotlib.pyplot as plt
import pandas as pd

AWS_ACCESS_KEY_ID = "_"
AWS_SECRET_ACCESS_KEY = "_"
AWS_REGION_NAME = "eu-north-1"
S3_BUCKET_NAME = "gritsruslan-sumdu-s3-bucket"
S3_FILE_KEY = "nbu_rates_2022.csv"

s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION_NAME,
)

response = s3.get_object(Bucket=S3_BUCKET_NAME, Key=S3_FILE_KEY)
df = pd.read_csv(io.BytesIO(response["Body"].read()))

df["date"] = pd.to_datetime(df["date"], format="%d.%m.%Y")
df_pivot = df.pivot(index="date", columns="currency", values="rate")
df_pivot.head()

plt.figure(figsize=(12, 6))
plt.plot(df_pivot.index, df_pivot["USD"], label="USD", color="blue")
plt.plot(df_pivot.index, df_pivot["EUR"], label="EUR", color="green")
plt.title("Курс гривні до USD та EUR за 2022 рік")
plt.xlabel("Дата")
plt.ylabel("Курс (грн)")
plt.legend()
plt.grid(True)
plt.savefig("chart_2022.png", bbox_inches="tight")
plt.show()

s3.upload_file("chart_2022.png", S3_BUCKET_NAME, "chart_2022.png")
