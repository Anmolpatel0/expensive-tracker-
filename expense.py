from collections import defaultdict
import csv
from datetime import datetime
import os
import streamlit as st

FILENAME = "expenses.csv"

st.set_page_config(
    page_title="Personal Expense Tracker", page_icon="💰", layout="centered"
)

st.title("💰 Personal Expense Tracker")
st.write(
    "Record daily expenses, view history, filter by category, and check"
    " summary stats persistently via CSV!"
)
st.markdown("---")


def initialize_csv():
  if not os.path.exists(FILENAME):
    with open(FILENAME, mode="w", newline="", encoding="utf-8") as file:
      writer = csv.writer(file)
      writer.writerow(["Date", "Category", "Amount", "Description"])


initialize_csv()

# Navigation Tabs
tab1, tab2, tab3 = st.tabs(
    ["➕ Add Expense", "📋 View & Filter", "📊 Summary Stats"]
)

with tab1:
  st.subheader("Record a New Expense")
  with st.form("expense_form"):
    date = st.date_input("Date", datetime.today())
    category = st.text_input(
        "Category (e.g. Food, Transport)"
    ).strip().capitalize()
    amount = st.number_input("Amount (₹)", min_value=0.0, step=1.0)
    description = st.text_input("Description (Optional)").strip()

    submit = st.form_submit_button("Save Expense")
    if submit:
      if not category or amount <= 0:
        st.error(
            "⚠️ Please fill in a valid category and an amount greater than 0!"
        )
      else:
        with open(FILENAME, mode="a", newline="", encoding="utf-8") as file:
          writer = csv.writer(file)
          writer.writerow([str(date), category, amount, description])
        st.success(
            f"✅ Expense of ₹{amount} added successfully under '{category}'!"
        )

with tab2:
  st.subheader("View and Filter Expenses")
  if os.path.exists(FILENAME):
    with open(FILENAME, mode="r", encoding="utf-8") as file:
      reader = csv.reader(file)
      data = list(reader)
      if len(data) > 1:
        filter_cat = st.text_input(
            "Filter by category (leave empty for all):"
        ).strip()

        filtered_data = [data[0]]
        for row in data[1:]:
          if not filter_cat or filter_cat.lower() in row[1].lower():
            filtered_data.append(row)

        st.table(filtered_data)
      else:
        st.info("No expense records found yet.")
  else:
    st.info("No expense file found.")

with tab3:
  st.subheader("Category Summary Statistics")
  if os.path.exists(FILENAME):
    summary = defaultdict(float)
    total_spent = 0.0
    with open(FILENAME, mode="r", encoding="utf-8") as file:
      reader = csv.reader(file)
      data = list(reader)
      for row in data[1:]:
        try:
          cat = row[1]
          amt = float(row[2])
          summary[cat] += amt
          total_spent += amt
        except (ValueError, IndexError):
          continue

    if summary:
      st.metric("Grand Total Spent", f"₹{total_spent:.2f}")
      st.markdown("---")
      for cat, amt in summary.items():
        st.write(f"- **{cat}**: ₹{amt:.2f}")
    else:
      st.info("No summary data available.")
  else:
    st.info("No expense records found.")
