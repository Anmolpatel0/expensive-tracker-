# 💰 Personal Expense Tracker

A simple and interactive Personal Expense Tracker built using Python and Streamlit. This application helps users record daily expenses, view transaction history, filter expenses by category, and monitor their total spending.

## 🌐 Live Demo

[Open Personal Expense Tracker](https://expensetrackerforyou.streamlit.app/)

## 📌 About the Project

Managing daily expenses is important for maintaining a healthy budget. This project provides a simple web-based application where users can record their expenses and view spending summaries.

The application uses CSV file storage to save expense records.

## ✨ Features

- **Add Expenses:** Record expenses with date, category, amount, and optional description.
- **View Expense History:** Display previously recorded transactions.
- **Category Filtering:** Filter expenses using category names.
- **Total Spending:** Calculate the overall amount spent.
- **Category-wise Summary:** View spending for each expense category.
- **CSV Storage:** Store expense records in a CSV file.
- **Input Validation:** Prevent saving expenses with an empty category or invalid amount.
- **Interactive Dashboard:** Simple interface with three navigation tabs.

## 🛠️ Technologies Used

- Python
- Streamlit
- CSV Module
- Collections (defaultdict)
- Datetime Module

## 📂 Project Structure

```text
expensive-tracker-/
│
├── expense.py
├── requirements.txt
└── README.md
```

The `expenses.csv` file is created automatically when the application runs and initializes its storage.

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Anmolpatel0/expensive-tracker-.git
```

### 2. Open the project folder

```bash
cd expensive-tracker-
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
streamlit run expense.py
```

The application will open in your web browser.

## 📊 How to Use

1. Open the application.
2. Go to the **Add Expense** tab.
3. Enter the date, category, amount, and optional description.
4. Click **Save Expense**.
5. Open **View & Filter** to see your transactions.
6. Open **Summary Stats** to check your total and category-wise spending.

## 🎯 Learning Outcomes

Through this project, I practiced:

- Python programming fundamentals.
- Working with CSV files.
- Reading and writing data.
- Using functions and Python modules.
- Handling user input and validation.
- Calculating totals using dictionaries.
- Building interactive applications with Streamlit.

## 👨‍💻 Author

**Anmol Patel**

GitHub: [Anmolpatel0](https://github.com/Anmolpatel0)

LinkedIn: [Anmol Patel](https://www.linkedin.com/in/anmol-patel-7a5b78378/)

---

⭐ If you find this project useful, consider giving it a star!
