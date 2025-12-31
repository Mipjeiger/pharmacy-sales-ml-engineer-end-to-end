import os
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine

# Load .env file terlebih dahulu sebelum membaca environment variables
env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path=env_path)

# Baca environment variables setelah .env dimuat
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Gunakan path absolut untuk membaca file CSV
csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "pharma-data.csv")
df = pd.read_csv(csv_path)
df.columns = [
    "distributor",
    "customer_name",
    "city",
    "country",
    "latitude",
    "longitude",
    "channel",
    "sub_channel",
    "product_name",
    "product_class",
    "quantity",
    "price",
    "sales",
    "month",
    "year",
    "sales_rep_name",
    "manager",
    "sales_team",
]

df.to_sql(
    "pharmacy_sales",
    engine,
    schema="raw",
    if_exists="append",
    index=False,
)
