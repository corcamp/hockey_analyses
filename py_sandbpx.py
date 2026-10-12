# Load hockey data from local .csv
import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv('temp/events.csv')

# View the first 5 rows of data
print(df.head())