🛒 RetailPulse AI: Enterprise Analytics Suite
RetailPulse AI is a 3-Tier Full Stack Data Science Application designed to simulate an enterprise-grade analytics environment. It integrates Bayesian Probability and IQR Outlier Detection to identify high-risk retail transactions and predict return probabilities in real-time.

Unlike simple scripts, this project demonstrates a Microservices Architecture by decoupling the Database, the Backend Intelligence API, and the Frontend Dashboard.

🏗 Architecture
This project follows a professional 3-Tier Design Pattern:

Tier 1 (Data Layer): MySQL Server stores raw transaction logs.

Tier 2 (Logic Layer): FastAPI serves as the backend "Brain," handling statistical computations (IQR, Bayes) and serving JSON endpoints.

Tier 3 (Presentation Layer): Streamlit consumes the API to visualize insights for end-usesdd .rs.

🚀 How to Run Locally
1. Prerequisites
Ensure you have the following installed:

Python 3.8+

MySQL Server (Running via MySQL Workbench, XAMPP, or Docker)

Git

2. Installation
Clone the repository and install the required Python packages:

Bash

git clone [https://github.com/YOUR_USERNAME/enterprise-retail-analytics.git](https://github.com/YOUR_USERNAME/enterprise-retail-analytics.git)
cd enterprise-retail-analytics
pip install -r requirements.txt
3. Database Setup (Crucial Step)
Create a file named .env in the root directory (you can copy .env.example).

Open .env and enter your local MySQL credentials:

Ini, TOML

DB_HOST=localhost
DB_USER=root
DB_PASSWORD=YOUR_ACTUAL_PASSWORD
Run the Database Seeder script. This connects to MySQL, creates the retail_db database, and populates it with 200+ synthetic transactions, including hidden outliers for the AI to find.

Bash

python setup_db.py
(Look for the "✅ Success!" message in your terminal)

4. Running the Application
Because this is a full-stack application, you need to run the Backend and Frontend simultaneously. Open two separate terminal windows:

Terminal 1: Start the Backend API This launches the FastAPI server on port 8000.

Bash

uvicorn api_server:app --reload
Terminal 2: Start the Frontend Dashboard This launches the Streamlit UI on port 8501.

Bash

streamlit run dashboard_app.py
📊 Features & Usage
1. Financial Anomaly Detection
Method: Interquartile Range (IQR) Analysis.

Usage: Navigate to the "Outlier Detection" tab and click "Scan Transactions." The system will query the API to identify transactions that deviate significantly from the norm (e.g., massive "Whale" purchases or pricing glitches).

2. Bayesian Risk Engine
Method: Naive Bayes Theorem (P(Return∣Category)).

Usage: Navigate to the "AI Predictions" tab. Select a product category (e.g., "Electronics") to calculate the real-time probability of that item being returned based on historical data.

🛠 Tech Stack
Language: Python 3.10

Database: MySQL, mysql-connector-python

Backend API: FastAPI, Uvicorn

Frontend UI: Streamlit, Plotly Express

Data Science: Pandas, NumPy, Scipy (Stats), Scikit-Learn

Security: Python-Dotenv (Environment Variable Management)

📂 Project Structure
Plaintext

/enterprise-retail-analytics
├── analytics_pkg/       # Shared Logic Package
│   ├── database.py      # MySQL Connection Handler
│   └── science.py       # Data Science & Math Engine
├── api_server.py        # FastAPI Backend
├── dashboard_app.py     # Streamlit Frontend
├── setup_db.py          # Database Seeder Script
├── requirements.txt     # Python Dependencies
└── README.md            # Documentation