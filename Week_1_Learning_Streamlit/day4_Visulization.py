import sqlite3
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Streamlit Title
st.title("Shopping Trends Visualizations with SQLite")

# Step 1: File Upload
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

# Define required columns
required_columns = ["age", "gender", "category", "purchase_amount_(usd)"]

if uploaded_file:
    # Load the uploaded file into a DataFrame
    df = pd.read_csv(uploaded_file)

    # Normalize column names
    df.columns = df.columns.str.replace(" ", "_").str.lower()

    st.write("Columns in the dataset:", df.columns.tolist())

    # Check for missing columns
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        st.error(f"The following required columns are missing: {', '.join(missing_columns)}")
        st.stop()

    # Rename the column for consistency with the code logic
    df.rename(columns={"purchase_amount_(usd)": "purchase_amount_usd"}, inplace=True)

    # Step 2: SQLite Database Setup
    db_name = "shopping_trends.db"
    connection = sqlite3.connect(db_name)

    # Create table dynamically based on DataFrame columns
    columns_sql = ", ".join(
        f'"{col}" TEXT' if df[col].dtype == 'object' else
        f'"{col}" REAL' if df[col].dtype in ['float64', 'int64'] else
        f'"{col}" TEXT'
        for col in df.columns
    )
    create_table_query = f"CREATE TABLE IF NOT EXISTS shopping_data ({columns_sql})"
    connection.execute(create_table_query)

    # Insert data into the table
    df.to_sql("shopping_data", connection, if_exists="replace", index=False)

    # Fetch data back from the database
    query = "SELECT * FROM shopping_data"
    df = pd.read_sql_query(query, connection)

    # Step 3: Display Dataset
    st.subheader("Collected Shopping Data")
    st.dataframe(df)

    # Step 4: User Filters
    st.sidebar.subheader("Filter Options")

    # Gender Filter
    gender_filter = st.sidebar.multiselect(
        "Filter by Gender", options=df["gender"].dropna().unique(), default=df["gender"].dropna().unique()
    )

    # Age Range Filter
    age_filter = st.sidebar.slider(
        "Filter by Age",
        min_value=int(df["age"].min()),
        max_value=int(df["age"].max()),
        value=(int(df["age"].min()), int(df["age"].max())),
    )

    # Category Filter
    category_filter = st.sidebar.multiselect(
        "Filter by Category", options=df["category"].dropna().unique(), default=df["category"].dropna().unique()
    )

    # Location Filter
    location_filter = st.sidebar.multiselect(
        "Filter by Location", options=df["location"].dropna().unique(), default=df["location"].dropna().unique()
    )

    # Subscription Status Filter
    subscription_filter = st.sidebar.multiselect(
        "Filter by Subscription Status", options=df["subscription_status"].dropna().unique(), default=df["subscription_status"].dropna().unique()
    )

    # Apply Filters
    filtered_df = df[
        (df["gender"].isin(gender_filter)) &
        (df["age"].between(age_filter[0], age_filter[1])) &
        (df["category"].isin(category_filter)) &
        (df["location"].isin(location_filter)) &
        (df["subscription_status"].isin(subscription_filter))
    ]

    # Display Filtered Data
    st.subheader("Filtered Data")
    st.dataframe(filtered_df)

    # Step 5: Visualizations

    # Matplotlib Bar Chart: Age Distribution
    st.subheader("Matplotlib Bar Chart: Age Distribution")
    if not filtered_df.empty:
        fig, ax = plt.subplots()
        filtered_df["age"].value_counts().sort_index().plot(kind="bar", ax=ax, color="skyblue")
        ax.set_title("Age Distribution")
        ax.set_xlabel("Age")
        ax.set_ylabel("Count")
        st.pyplot(fig)

    # Seaborn Scatter Plot: Purchase Amount vs Age
    st.subheader("Seaborn Scatter Plot: Purchase Amount (USD) vs Age")
    if "purchase_amount_usd" in filtered_df.columns:
        fig, ax = plt.subplots()
        sns.scatterplot(data=filtered_df, x="age", y="purchase_amount_usd", hue="category", ax=ax)
        ax.set_title("Purchase Amount (USD) vs Age")
        st.pyplot(fig)
    else:
        st.warning("Column 'purchase_amount_usd' is missing in the dataset.")

    # Plotly Bar Chart: Category Breakdown
    st.subheader("Plotly Interactive Bar Chart: Category Breakdown")
    if "purchase_amount_usd" in filtered_df.columns:
        plotly_fig = px.bar(
            filtered_df,
            x="category",
            y="purchase_amount_usd",
            color="category",
            title="Category Breakdown by Purchase Amount (USD)",
            barmode="group",
        )
        st.plotly_chart(plotly_fig, use_container_width=True)
    else:
        st.warning("Column 'purchase_amount_usd' is missing in the dataset.")

    # Plotly Pie Chart: Gender Distribution
    st.subheader("Plotly Interactive Pie Chart: Gender Distribution")
    if "gender" in filtered_df.columns:
        pie_fig = px.pie(filtered_df, names="gender", title="Gender Distribution", hole=0.3)
        st.plotly_chart(pie_fig, use_container_width=True)
    else:
        st.warning("Column 'gender' is missing in the dataset.")

    # Close the SQLite Connection
    connection.close()
    st.success("Visualizations generated successfully!")
else:
    st.warning("Please upload a CSV file to proceed.")