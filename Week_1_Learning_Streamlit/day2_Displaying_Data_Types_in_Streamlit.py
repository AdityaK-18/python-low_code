import pandas as pd
import sqlite3

# Manually create a small dataset
data = {
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [25, 30, 35],
    "City": ["New York", "Los Angeles", "Chicago"]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Save to a CSV file (optional)
df.to_csv("sample_data.csv", index=False)

# Connect to SQLite database (or create it)
conn = sqlite3.connect("data_types.db")

# Save DataFrame to SQLite
df.to_sql("people", conn, if_exists="replace", index=False)

# Confirm data saved
print("Data saved to SQLite database")
