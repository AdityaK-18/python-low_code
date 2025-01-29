import sqlite3
import streamlit as st
import pandas as pd

# # Apply custom CSS for background, title, and button styles
# st.markdown(
#     """
#     <style>
#     /* Background color for the app */
#     .main {
#         background-color: #f4f8fb; /* Light grey-blue */
#     }
#     /* Title styling */
#     h1 {
#         color: #ff6347; /* Tomato red */
#         text-align: center;
#         font-family: 'Arial', sans-serif;
#     }
#     /* Subtitle styling */
#     h2 {
#         color: #4caf50; /* Green */
#         text-align: center;
#     }
#     /* Button styling */
#     .stButton>button {
#         background-color: #4caf50; /* Green button */
#         color: white;
#         border-radius: 10px;
#         padding: 10px 20px;
#     }
#     .stButton>button:hover {
#         background-color: #45a049; /* Darker green on hover */
#     }
#     /* Input box styling */
#     .stTextInput>div>input {
#         border: 2px solid #4caf50; /* Green border */
#         border-radius: 8px;
#         padding: 5px;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )

# Page title
st.title("Registration Form")

# Subtitle
st.markdown("<h2>Register below to join : </h2>", unsafe_allow_html=True)

# Step 1: Set up SQLite database
connection = sqlite3.connect("registration.db")
cursor = connection.cursor()

# Create a table if it doesn't exist
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS attendees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        gender TEXT,
        admission_type TEXT
    )
    """
)
connection.commit()

# Collect user inputs
st.subheader("Enter your details:")

with st.form(key="registration_form"):
    # Name input
    name = st.text_input("Name")

    # Age input using slider
    age = st.slider("Age", min_value=18, max_value=60, value=25)

    # Gender selection using radio buttons
    gender = st.radio("Gender", options=["Male", "Female", "Other"])

    # Admission type using dropdown
    admission_type = st.selectbox("Admission Type", options=["General", "Student"])

    # Submit button
    submit_button = st.form_submit_button(label="Submit")

# Save Data to SQLite Database
if submit_button:
    if name:  # Ensure the name field is not empty
        # Insert data into the database
        cursor.execute(
            """
            INSERT INTO attendees (name, age, gender, admission_type)
            VALUES (?, ?, ?, ?)
            """,
            (name, age, gender, admission_type),
        )
        connection.commit()

        # Success message
        st.success(f"Thank you, {name}, for registering!")
    else:
        st.error("Please enter your name.")

# Display registered attendees
st.subheader("Registered Attendees")

# Fetch data from the database
attendees = pd.read_sql_query("SELECT * FROM attendees", connection)

# Display the data as a table
st.dataframe(attendees)

# Close the database connection when the app ends
connection.close()
