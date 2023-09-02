# DataSciBuddy


DataSciBuddy Python Package

The goal of this package is to provide helper functions and datasets for data science exploration.

DATASETS:

1. Fraud Data:
   - transaction_amount: Amount of the transaction.
   - is_foreign_transaction: Whether the transaction was made outside the home country (1 for yes, 0 for no).
   - account_age_in_days: Age of the account in days.
   - is_fraud: Whether the transaction was fraudulent (1 for yes, 0 for no).

2. House Prices Data:
   - num_rooms: Number of rooms in the house.
   - area_in_sqft: Total area of the house in square feet.
   - distance_to_city_center: Distance to the city center in miles.
   - price: Price of the house.

To use the helper functions, simply import them:
from DataSciBuddy import helper_functions

For datasets, read them using pandas:
import pandas as pd
fraud_data = pd.read_csv('path_to_package/DataSciBuddy/datasets/fraud_data.csv')
