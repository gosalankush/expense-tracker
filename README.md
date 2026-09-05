# 💰 Personal Expense & Budget Tracker CLI

A lightweight, secure, command-line interface (CLI) application built with Python for tracking personal daily expenses, managing monthly/yearly budgets, calculating projected savings, exporting reports, and generating data visualizations using Matplotlib and Pandas.

---

## 🌟 Key Features

### 🔒 User Authentication & Security
* **Encrypted Passwords:** Passwords are hashed using SHA-256 encryption (`hashlib`) before being stored locally in `users.json`.
* **Masked Password Input:** Password fields are hidden during entry using Python's native `getpass` module.

### 💸 Expense Management
* **Add & Categorize:** Log expenses with precise timestamps (`YYYY-MM-DD HH:MM`), amounts, categories, and descriptions.
* **View & Search:** Display structured expense logs or query transactions by category.
* **Category Summaries:** View total spend along with dynamic percentage breakdowns by category.
* **Remove Entries:** Easily remove expenses under specific categories.

### 📊 Savings & Budget Tracking
* **Monthly & Yearly Budgets:** Set and update specific budget limits without duplicate overwrites.
* **Savings Calculator:** Dynamic analysis comparing total spend versus budgets across overall, monthly, and yearly timeframes.
* **Goal Projections:** Calculate estimated timeframes (in months) required to achieve custom savings goals.

### 📁 Data Exporting (CSV)
* **Expense CSV Export:** Export all recorded expenses into timestamped `.csv` spreadsheet files for record-keeping or Excel analysis.
* **Budget CSV Export:** Export monthly and yearly budget records into separate timestamped `.csv` spreadsheets.

### 📈 Visual Data Analytics
* **Category Breakdown:** Render pie charts for overall and current month expense distributions.
* **Yearly Trends:** Bar charts detailing monthly spend totals.
* **Monthly Savings Breakdown:** Interactive Matplotlib bar chart comparing Total Budget, Total Expenses, and Net Savings for the current month.
* **Month-by-Month Savings:** Interactive yearly bar chart tracking net savings per month from January to December.

---

## 📂 File Structure
```text
.
├── main.py              # Core application entry point logic
├── expenses.json        # Persistent local storage for expenses
├── budgets.json         # Persistent local storage for monthly/yearly budgets
├── users.json           # User database with hashed credentials
├── *.csv                # Timestamped CSV export files (generated on export)
├── README.md            # Project documentation
└── requirements.txt     # Python dependencies

---

## 🚀 Getting Started

### Prerequisites
* **Python 3.8+** installed on your system.

### Installation

1. **Clone the repository:**
   `git clone [https://github.com/gosalankush/expense-tracker.git](https://github.com/gosalankush/expense-tracker.git)`
   `cd expense-tracker`

2. **Install required dependencies:**
   `pip install pandas matplotlib`

3. **Run the application:**
   `python main.py`

---

## 💡 Usage Example

1. Launch the program and log in (or register an account if launching for the first time).
2. Select **Option 1 (Expense Account)** to log daily expenses, view pie charts, or export expenses to CSV.
3. Select **Option 2 (Savings Account)** to set monthly budgets, run savings goal projections, view bar graph reports, or export budgets to CSV.

---

## 📄 License

This project is licensed under the MIT License - feel free to use, modify, and distribute!