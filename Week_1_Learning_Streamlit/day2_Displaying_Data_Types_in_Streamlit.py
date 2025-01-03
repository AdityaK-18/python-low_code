import sqlite3 as st  # Using alias `st` for sqlite3
import pandas as pd
import streamlit as stl  # Using alias `stl` for Streamlit
import matplotlib.pyplot as plt

# Step 1: Create a sample dataset
data = {
    "Name": ["Alice", "Bob", "Charlie", "Diana", "Eve"],
    "Age": [25, 30, 35, 28, 40],
    "City": ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"]
}

# Convert the data to a DataFrame
df = pd.DataFrame(data)
stl.write("### Sample Dataset")
stl.dataframe(df)

# Step 2: Connect to SQLite database (or create one if it doesn't exist)
connection = st.connect("data_types.db")

# Step 3: Save the DataFrame to the SQLite database
df.to_sql("data_types", connection, if_exists="replace", index=False)
stl.write("### Data saved to SQLite database!")

# Step 4: Read the data back from the SQLite database
query = "SELECT * FROM data_types"
df_from_db = pd.read_sql_query(query, connection)
stl.write("### Data retrieved from the database")
stl.dataframe(df_from_db)

# Step 5: Visualizations using Streamlit
stl.write("### Visualizations")

# Bar Graph: Age Distribution
stl.write("#### Bar Graph: Age Distribution")
fig1, ax1 = plt.subplots()
df_from_db.plot(x="Name", y="Age", kind="bar", ax=ax1, color="skyblue", legend=False)
ax1.set_title("Age Distribution")
ax1.set_xlabel("Name")
ax1.set_ylabel("Age")
stl.pyplot(fig1)

# Pie Chart: City Distribution
stl.write("#### Pie Chart: City Distribution")
fig2, ax2 = plt.subplots()
df_from_db["City"].value_counts().plot.pie(autopct="%1.1f%%", ax=ax2, title="City Distribution")
ax2.set_ylabel("")
stl.pyplot(fig2)

# Close the database connection
connection.close()
stl.write("### Database connection closed.")
