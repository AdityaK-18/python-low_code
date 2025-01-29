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
   streamlit run day4_Visulization.py
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


# Streamlit Deployment on AWS EC2 - Comprehensive Guide

This guide provides a step-by-step explanation for deploying a Streamlit application on AWS EC2, including resolutions to common challenges to ensure a smooth experience for new users.

---

## Prerequisites
1. AWS Account.
2. Basic understanding of Python and Streamlit.
3. SSH Key Pair downloaded during EC2 setup.

---

## Step 1: Setting Up AWS EC2 Instance

### 1.1 Launch an EC2 Instance
- Go to the AWS EC2 dashboard and launch an instance.
- Select **Amazon Linux 2 AMI**.
- Choose an instance type (e.g., `t2.micro` for free tier).
- Configure security groups:
  - Add **SSH** (port `22`) for your IP.
  - Add a **Custom TCP Rule** for port `8501` (for Streamlit).

### 1.2 Connect to the Instance
- Use SSH to connect to your instance:
  ```bash
  ssh -i /path/to/your-key.pem ec2-user@<Public-IP>
  ```

---

## Step 2: Preparing the EC2 Instance

### 2.1 Update and Install Required Packages
- Update the system:
  ```bash
  sudo yum update -y
  ```
- Install development tools:
  ```bash
  sudo yum groupinstall "Development Tools" -y
  ```
- Install Python dependencies:
  ```bash
  sudo yum install gcc libffi-devel bzip2 bzip2-devel zlib-devel xz-devel readline-devel sqlite sqlite-devel openssl11 openssl11-devel -y
  ```

### 2.2 Install Python 3.9+
- Download and build Python:
  ```bash
  wget https://www.python.org/ftp/python/3.9.16/Python-3.9.16.tgz
  tar xvf Python-3.9.16.tgz
  cd Python-3.9.16
  ./configure --with-openssl=/usr/bin/openssl11 --enable-optimizations
  make
  sudo make install
  ```
- Verify installation:
  ```bash
  python3.9 --version
  ```

### 2.3 Install and Verify SQLite Support
- Verify SQLite installation:
  ```bash
  python3.9 -c "import sqlite3; print(sqlite3.sqlite_version)"
  ```
  If any issues arise, ensure `sqlite-devel` is installed and Python is built with the correct paths.

### 2.4 Install Pip and Streamlit
- Install pip:
  ```bash
  sudo python3.9 -m ensurepip --upgrade
  ```
- Install Streamlit:
  ```bash
  pip3 install streamlit
  ```

---

## Step 3: Deploy the Streamlit Application

### 3.1 Upload Files to EC2
- Use `scp` to transfer your application files:
  ```bash
  scp -i /path/to/your-key.pem your_script.py ec2-user@<Public-IP>:/home/ec2-user
  ```
  If your app has dependencies (e.g., SQLite database or CSV files), upload them as well.

### 3.2 Run the Application
- Start the Streamlit app:
  ```bash
  nohup python3.9 -m streamlit run your_script.py --server.port 8501 &
  ```
- Confirm the app is running by visiting:
  ```
  http://<Public-IP>:8501
  ```

---

## Step 4: Troubleshooting Common Challenges

### Challenge 1: "No module named '_sqlite3'"
- Ensure `sqlite-devel` is installed:
  ```bash
  sudo yum install sqlite sqlite-devel -y
  ```
- Rebuild Python:
  ```bash
  ./configure --with-openssl=/usr/bin/openssl11 --enable-optimizations
  make
  sudo make install
  ```

### Challenge 2: "SSL not supported"
- Ensure `openssl11` is installed and linked correctly:
  ```bash
  sudo ln -sf /usr/bin/openssl11 /usr/bin/openssl
  ./configure --with-openssl=/usr/bin/openssl11 --enable-optimizations
  make
  sudo make install
  ```

### Challenge 3: "Permission Denied" Errors
- Use `sudo` for commands requiring elevated privileges.
- Ensure correct file permissions for Python and related files:
  ```bash
  sudo chown -R ec2-user:ec2-user /home/ec2-user/Python-3.9.16
  ```

### Challenge 4: Keeping App Running After Logout
- Use `nohup` to run the app in the background:
  ```bash
  nohup python3.9 -m streamlit run your_script.py --server.port 8501 &
  ```
- Monitor logs:
  ```bash
  tail -f nohup.out
  ```

---

## Additional Tips
1. **Security Groups:**
   - Limit access to your instance by specifying your IP instead of `0.0.0.0/0`.

2. **Monitoring:**
   - Use `ps aux | grep streamlit` to check running processes.
   - Use `kill <PID>` to stop the app if necessary.

3. **Backup:**
   - Regularly back up your application and data to avoid data loss.

---

## Conclusion
By following this guide, you should be able to deploy a Streamlit application on AWS EC2 seamlessly. Common challenges have been addressed to prevent future issues. Enjoy deploying your application!

# Streamlit Deployment Guide

This guide provides a step-by-step walkthrough for deploying a Streamlit application, addressing common challenges faced during the process to ensure a smooth experience for beginners.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Setting Up the Development Environment](#setting-up-the-development-environment)
3. [Running the Streamlit Application Locally](#running-the-streamlit-application-locally)
4. [Deployment Challenges and Solutions](#deployment-challenges-and-solutions)
   - [External URL Not Accessible](#external-url-not-accessible)
   - [Port Visibility in GitHub Codespaces](#port-visibility-in-github-codespaces)
   - [`ngrok` Not Found](#ngrok-not-found)
5. [Final Deployment Checklist](#final-deployment-checklist)
6. [Useful Resources](#useful-resources)

---

## Prerequisites

Before getting started, ensure you have the following:

- Python 3.7 or higher installed.
- Streamlit library installed:
  ```bash
  pip install streamlit
  ```
- A working code editor (e.g., VS Code) and Git setup.
- An internet connection to test external URLs.

---

## Setting Up the Development Environment

1. Clone your project repository:
   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit app locally:
   ```bash
   streamlit run <your_app.py>
   ```
   - Use the `Local URL` provided in the terminal to test your application.

---

## Running the Streamlit Application Locally

Use the following command to start your app:
```bash
streamlit run <your_app.py> --server.enableCORS false --server.enableXsrfProtection false
```

The terminal will display the **Local URL**, **Network URL**, and **External URL**. Use these to test your app's accessibility.

---

## Deployment Challenges and Solutions

### 1. External URL Not Accessible

**Problem:** The external URL provided by Streamlit does not work.

**Solution:**
- Check if the port your app is running on is accessible from outside the local environment.
- If using GitHub Codespaces, ensure the port is set to **Public** (see the next section).

---

### 2. Port Visibility in GitHub Codespaces

**Problem:** The port in GitHub Codespaces is set to **Private** by default, making it inaccessible externally.

**Solution:**
1. Open the **Ports** tab in VS Code (you can find this in the bottom panel).
2. Locate your app's port (e.g., 8501).
3. Click the lock icon (🔒) under the "Visibility" column and change it to **Public**.

---

### 3. `ngrok` Not Found

**Problem:** You want to expose your app to the public internet using `ngrok`, but it is not installed.

**Solution:**
1. Install `ngrok`:
   ```bash
   wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-stable-linux-amd64.zip
   unzip ngrok-stable-linux-amd64.zip
   sudo mv ngrok /usr/local/bin
   ```
2. Authenticate with your token:
   ```bash
   ngrok config add-authtoken <your-auth-token>
   ```
3. Start a tunnel to expose your app:
   ```bash
   ngrok http 8504
   ```
   Copy the public URL provided by `ngrok` and use it to access your app.

---

## Final Deployment Checklist

Before considering the deployment complete, ensure the following:
1. **Port Visibility:** All required ports are set to **Public** if using GitHub Codespaces.
2. **External URL Testing:** Verify that the app's external URL is accessible on other devices or networks.
3. **Firewall Configuration:** Ensure no firewalls block the app's external access.
4. **Error-Free Code:** Test all features and fix any errors before sharing the app.

---

## Useful Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [GitHub Codespaces Documentation](https://docs.github.com/en/codespaces)
- [ngrok Documentation](https://ngrok.com/docs)

---

With this guide, new developers should be able to avoid common pitfalls and successfully deploy their Streamlit applications.
