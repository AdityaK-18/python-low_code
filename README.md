# python-low_code

## Pre-Commit Set up for Developers

These steps ensure that code is properly linted, formatted, etc., before committing to a remote branch.

### 1. Open Command Prompt
- Start by opening the Command Prompt (CMD) on your VDI machine.

### 2. Install Python
- Install Python on your machine.

### 3. Navigate to Your Repository
- Use the `dir` command to navigate to the directory where your repository is cloned.

### 4. Set Up a Virtual Environment
- Install the virtual environment package by running:
  ```
  pip install virtualenv
  ```
- Create a new virtual environment in a directory named `.venv`:
  ```
  python -m virtualenv .venv
  ```

### 5. Activate the Virtual Environment
- Activate the virtual environment with the following command:
  ```
  .venv/Scripts/activate
  ```
  OR
  ```
  ..venv\Scripts\activate
  ```

### 6. Install Pre-Commit
- Install pre-commit in your virtual environment:
  ```
  pip install pre-commit
  ```

### 7. Verify the Virtual Environment
- From your current directory, run `dir` to confirm that the `.venv` folder exists. This directory contains the virtual environment.
- Change to the `.venv` directory:
  ```
  cd .venv
  ```
- From this location, run `dir` to check for the `Scripts` folder. This folder contains executables for the virtual environment.
- Change to the `Scripts` directory:
  ```
  cd Scripts
  ```
- Inside the `Scripts` folder, you should find the `pre-commit.exe` binary file.

### 8. Install Pre-Commit Hooks
- While inside the `Scripts` directory, install the pre-commit hooks by running:
  ```
  pre-commit.exe install
  ```

### 9. Run Pre-Commit Checks
- To run pre-commit on all files in the repository, use:
  ```
  pre-commit run --all-files
  ```
- The initial run might take longer, but subsequent runs will be faster. After setup, pre-commit will automatically run every time you execute a `git commit`.

### 10. Add Pre-Commit Configuration
- Use the below `pre-commit-config.yaml` in your project root directory before installing pre-commit hooks.

### 11. Run Streamlit
- Start the Streamlit application by running:
  ```
  streamlit run Week_1_Learning_Streamlit/day_1_intro_to_streamlit.py
  ```


# Day 4 Visualization
# Shopping Trends Visualizations with SQLite

This project allows you to upload a shopping dataset in CSV format and visualize trends using Streamlit, SQLite, and various visualization libraries such as Matplotlib, Seaborn, and Plotly.

## Features
1. **File Upload**:
   - Upload your shopping data in CSV format (**shopping_trends.csv**).
   - Automatically normalize column names (spaces replaced with underscores and converted to lowercase).
   - Ensures proper data validation before processing.

2. **Data Validation**:
   - Checks if required columns (`age`, `gender`, `category`, `purchase_amount_(usd)`) are present in the uploaded dataset.
   - Provides clear error messages if any required column is missing.

3. **SQLite Database Integration**:
   - Automatically creates an SQLite database (`shopping_trends.db`) and a table (`shopping_data`).
   - Inserts the uploaded dataset into the database for querying and analysis.

4. **Filters**:
   - Filter the data using various parameters:
     - Gender
     - Age range
     - Category
     - Location
     - Subscription status

5. **Visualizations**:
   - **Matplotlib Bar Chart**: Age distribution.
   - **Seaborn Scatter Plot**: Purchase amount vs. age, colored by category.
   - **Plotly Bar Chart**: Category breakdown by purchase amount.
   - **Plotly Pie Chart**: Gender distribution.

## Requirements
- Python 3.7+
- Libraries:
  - `streamlit`
  - `pandas`
  - `sqlite3`
  - `matplotlib`
  - `seaborn`
  - `plotly`

Install the required libraries using:
```bash
pip install streamlit pandas matplotlib seaborn plotly
```

## How to Run
1. Clone the repository or copy the script.
2. Ensure the required libraries are installed.
3. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```
4. Upload your CSV file and interact with the visualizations.

## Uploading Your File
- Ensure your CSV file is properly formatted before uploading.
- The file upload section in the app allows you to browse and select your CSV file.
- After uploading, the application will:
  1. Normalize column names to lowercase and replace spaces with underscores.
  2. Validate if the file contains the required columns (`age`, `gender`, `category`, `purchase_amount_(usd)`).
  3. Stop processing if validation fails, with a clear error message indicating missing columns.
  4. Proceed to data visualization if validation succeeds.

### Expected CSV Format
Your dataset should contain the following columns:
- `age`: Integer values representing customer age.
- `gender`: Gender of the customer (e.g., Male, Female).
- `category`: Category of the purchased item (e.g., Clothing, Footwear).
- `purchase_amount_(usd)`: Numeric values for purchase amounts in USD.

### Example Dataset
| age | gender | category  | purchase_amount_(usd) | location       | subscription_status |
|-----|--------|-----------|------------------------|----------------|----------------------|
| 25  | Female | Clothing  | 45.5                  | New York       | Yes                  |
| 32  | Male   | Footwear  | 89.0                  | Los Angeles    | No                   |

## Filtering Options
- **Gender**: Multiselect filter to include/exclude specific genders.
- **Age Range**: Slider to filter customers within a specific age range.
- **Category**: Multiselect filter to focus on particular product categories.
- **Location**: Multiselect filter to include/exclude specific locations.
- **Subscription Status**: Multiselect filter for subscription status (e.g., Yes, No).

## Visualizations
1. **Age Distribution**:
   - A bar chart showing the number of customers across different age groups.
2. **Purchase Amount vs. Age**:
   - Scatter plot illustrating purchase amounts against customer age, categorized by product type.
3. **Category Breakdown**:
   - Interactive bar chart showing total purchase amounts for each category.
4. **Gender Distribution**:
   - Pie chart displaying the percentage of customers by gender.

## Notes on Data Upload and Validation
- The file upload process ensures that only valid CSV files with the required data structure are accepted.
- If any required columns are missing, the application stops execution and displays an error.
- After a successful upload, the application displays a dataset preview and applies all filters for further analysis.

## Contributing
Feel free to contribute by creating a pull request or opening an issue for any bugs or feature requests.

## License
This project is open-source and available under the [MIT License](LICENSE).


