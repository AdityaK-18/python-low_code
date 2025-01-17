import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Database setup
def init_db():
    conn = sqlite3.connect('conference.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS events (
                    event_id INTEGER CHECK(event_id >= 0),
                    event_name TEXT,
                    location TEXT,
                    date_time TEXT,
                    attendee_name TEXT,
                    attendee_email TEXT,
                    attendee_phone_number TEXT
                )''')
    conn.commit()
    conn.close()

# Insert data into the database
def insert_data(event_id, event_name, location, date_time, attendee_name, attendee_email, attendee_phone_number):
    if event_id < 0:
        raise ValueError("Event ID cannot be negative.")
    conn = sqlite3.connect('conference.db')
    c = conn.cursor()
    c.execute('''INSERT INTO events (event_id, event_name, location, date_time, attendee_name, attendee_email, attendee_phone_number)
                 VALUES (?, ?, ?, ?, ?, ?, ?)''',
              (event_id, event_name, location, date_time, attendee_name, attendee_email, attendee_phone_number))
    conn.commit()
    conn.close()

# Fetch data from the database
def fetch_data():
    conn = sqlite3.connect('conference.db')
    c = conn.cursor()
    c.execute('SELECT * FROM events')
    rows = c.fetchall()
    conn.close()
    return rows

# Load Kaggle dataset into the database with error handling and chunk loading
def load_kaggle_dataset(file):
    try:
        st.write("Uploading and processing the file in chunks...")
        conn = sqlite3.connect('conference.db')
        for chunk in pd.read_csv(file, chunksize=10000):
            chunk.to_sql('events', conn, if_exists='append', index=False)
        conn.close()
        st.success("Kaggle dataset uploaded and saved to the database successfully!")
    except Exception as e:
        st.error(f"An error occurred while uploading the dataset: {e}")

# Fetch data for display
def fetch_data_from_db():
    conn = sqlite3.connect('conference.db')
    df = pd.read_sql_query('SELECT * FROM events', conn)
    conn.close()
    return df

# Streamlit app
init_db()
st.title("College Conference Event Management App")

menu = ["Add Event", "View Events", "Upload Kaggle Dataset", "Visualize Data"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Add Event":
    st.subheader("Add Event Details")
    event_id = st.number_input("Event ID", step=1, min_value=0)
    event_name = st.text_input("Event Name")
    location = st.text_input("Location")
    date_time = st.text_input("Date and Time (YYYY-MM-DD HH:MM:SS)")
    attendee_name = st.text_input("Attendee Name")
    attendee_email = st.text_input("Attendee Email")
    attendee_phone_number = st.text_input("Attendee Phone Number")

    if st.button("Add Event"):
        if event_name and location and date_time and attendee_name and attendee_email and attendee_phone_number:
            try:
                insert_data(event_id, event_name, location, date_time, attendee_name, attendee_email, attendee_phone_number)
                st.success(f"Event '{event_name}' with attendee '{attendee_name}' added successfully!")
            except ValueError as ve:
                st.error(str(ve))
        else:
            st.error("Please fill all fields.")

elif choice == "View Events":
    st.subheader("View and Filter Events")
    data = fetch_data()
    df = pd.DataFrame(data, columns=["Event ID", "Event Name", "Location", "Date and Time", "Attendee Name", "Attendee Email", "Attendee Phone Number"])

    if not df.empty:
        st.dataframe(df)

        # Filtering options
        filter_event_name = st.text_input("Filter by Event Name")
        filter_location = st.text_input("Filter by Location")

        filtered_data = df.copy()
        if filter_event_name:
            filtered_data = filtered_data[filtered_data['Event Name'].str.contains(filter_event_name, case=False, na=False)]
        if filter_location:
            filtered_data = filtered_data[filtered_data['Location'].str.contains(filter_location, case=False, na=False)]

        st.dataframe(filtered_data)
    else:
        st.warning("No events found.")

elif choice == "Upload Kaggle Dataset":
    st.subheader("Upload Kaggle Dataset")
    st.write("**Expected Columns:** `event_id`, `event_name`, `location`, `date_time`, `attendee_name`, `attendee_email`, `attendee_phone_number`.")
    uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

    if uploaded_file:
        load_kaggle_dataset(uploaded_file)
        df = fetch_data_from_db()
        st.write("Dataset Preview:")
        st.dataframe(df.head())

elif choice == "Visualize Data":
    st.subheader("Visualize Event Data")
    data = fetch_data()
    df = pd.DataFrame(data, columns=["Event ID", "Event Name", "Location", "Date and Time", "Attendee Name", "Attendee Email", "Attendee Phone Number"])

    if not df.empty:
        st.write("Event Count by Location")
        location_counts = df['Location'].value_counts()

        st.write("Event Count by Event Name")
        event_name_counts = df['Event Name'].value_counts()

        # Side-by-side charts
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        location_counts.plot(kind='bar', ax=axes[0], title='Event Count by Location')
        event_name_counts.plot(kind='bar', ax=axes[1], title='Event Count by Event Name')
        st.pyplot(fig)
    else:
        st.warning("No events found to visualize.")
