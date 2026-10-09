from collections import defaultdict
import csv
import os
from datetime import datetime
import customtkinter as ctk

FILENAME = "expenses.csv"

# App Appearance Setup
ctk.set_appearance_mode("Dark")  # Default mode
ctk.set_default_color_theme("blue")


class ExpenseTrackerApp(ctk.CTk):

  def __init__(self):
    super().__init__()

    self.title("💰 Personal Expense Tracker Hub")
    self.geometry("700x550")
    self.resizable(False, False)

    self.initialize_csv()

    # Top Header & Theme Switcher Frame
    self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
    self.header_frame.pack(fill="x", padx=20, pady=(15, 5))

    self.title_label = ctk.CTkLabel(
        self.header_frame,
        text="💰 Expense Tracker",
        font=ctk.CTkFont(family="Poppins", size=20, weight="bold"),
    )
    self.title_label.pack(side="left")

    # Theme Toggle Switch/Button
    self.theme_btn = ctk.CTkButton(
        self.header_frame,
        text="🌙 Toggle Theme",
        width=130,
        command=self.toggle_theme,
        fg_color="#334155",
        hover_color="#1e293b",
    )
    self.theme_btn.pack(side="right")

    # Tabs for different features
    self.tab_view = ctk.CTkTabview(self, width=660, height=450)
    self.tab_view.pack(padx=20, pady=10)

    self.tab_add = self.tab_view.add("➕ Add Expense")
    self.tab_view.add("📋 View & Filter")
    self.tab_summary = self.tab_view.add("📊 Summary Stats")

    # Setup individual tabs
    self.setup_add_tab()
    self.setup_view_tab()
    self.setup_summary_tab()

  def initialize_csv(self):
    if not os.path.exists(FILENAME):
      with open(FILENAME, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Category", "Amount", "Description"])

  def toggle_theme(self):
    if ctk.get_appearance_mode() == "Dark":
      ctk.set_appearance_mode("Light")
      self.theme_btn.configure(text="☀️ Dark Mode")
    else:
      ctk.set_appearance_mode("Dark")
      self.theme_btn.configure(text="🌙 Light Mode")

  # ==================== TAB 1: ADD EXPENSE ====================
  def setup_add_tab(self):
    ctk.CTkLabel(
        self.tab_add,
        text="Record a New Expense",
        font=ctk.CTkFont(size=16, weight="bold"),
    ).pack(pady=10)

    # Form Fields
    self.date_input = ctk.CTkEntry(
        self.tab_add,
        placeholder_text="Date (YYYY-MM-DD)",
        width=300,
        height=38,
    )
    self.date_input.insert(0, datetime.today().strftime("%Y-%m-%d"))
    self.date_input.pack(pady=8)

    self.category_input = ctk.CTkEntry(
        self.tab_add,
        placeholder_text="Category (e.g. Food, Transport)",
        width=300,
        height=38,
    )
    self.category_input.pack(pady=8)

    self.amount_input = ctk.CTkEntry(
        self.tab_add, placeholder_text="Amount (e.g. 500)", width=300, height=38
    )
    self.amount_input.pack(pady=8)

    self.desc_input = ctk.CTkEntry(
        self.tab_add,
        placeholder_text="Description (Optional)",
        width=300,
        height=38,
    )
    self.desc_input.pack(pady=8)

    submit_btn = ctk.CTkButton(
        self.tab_add,
        text="Save Expense",
        command=self.save_expense,
        fg_color="#6366f1",
        hover_color="#4f46e5",
        height=40,
        width=300,
    )
    submit_btn.pack(pady=15)

    self.msg_label = ctk.CTkLabel(
        self.tab_add, text="", font=ctk.CTkFont(size=13, weight="bold")
    )
    self.msg_label.pack(pady=5)

  def save_expense(self):
    date = self.date_input.get().strip()
    category = self.category_input.get().strip().capitalize()
    amount_str = self.amount_input.get().strip()
    desc = self.desc_input.get().strip()

    if not date or not category or not amount_str:
      self.msg_label.configure(
          text="⚠️ Please fill in all required fields!", text_color="#f59e0b"
      )
      return

    try:
      amount = float(amount_str)
    except ValueError:
      self.msg_label.configure(
          text="❌ Amount must be a valid number!", text_color="#ef4444"
      )
      return

    with open(FILENAME, mode="a", newline="", encoding="utf-8") as file:
      writer = csv.writer(file)
      writer.writerow([date, category, amount, desc])

    self.msg_label.configure(
        text=f"✅ Saved successfully: ₹{amount} under '{category}'!",
        text_color="#10b981",
    )
    self.amount_input.delete(0, "end")
    self.desc_input.delete(0, "end")
    # Refresh other tabs if needed
    self.load_expenses_data()
    self.load_summary_data()

  # ==================== TAB 2: VIEW & FILTER ====================
  def setup_view_tab(self):
    top_frame = ctk.CTkFrame(self.tab_view.tab("📋 View & Filter"), fg_color="transparent")
    top_frame.pack(fill="x", pady=5)

    self.filter_input = ctk.CTkEntry(
        top_frame,
        placeholder_text="Filter by category (leave empty for all)...",
        width=350,
        height=35,
    )
    self.filter_input.pack(side="left", padx=5)

    filter_btn = ctk.CTkButton(
        top_frame,
        text="Apply Filter",
        command=self.load_expenses_data,
        width=120,
        height=35,
        fg_color="#3b82f6",
        hover_color="#2563eb",
    )
    filter_btn.pack(side="left", padx=5)

    # Textbox to display expenses table layout
    self.expense_textbox = ctk.CTkTextbox(
        self.tab_view.tab("📋 View & Filter"), width=620, height=310, font=("Courier", 12)
    )
    self.expense_textbox.pack(pady=10)
    self.load_expenses_data()

  def load_expenses_data(self):
    self.expense_textbox.delete("1.0", "end")
    filter_cat = self.filter_input.get().strip().lower() if hasattr(self, "filter_input") else ""

    if not os.path.exists(FILENAME):
      self.expense_textbox.insert("end", "No expense records found.")
      return

    with open(FILENAME, mode="r", encoding="utf-8") as file:
      reader = csv.reader(file)
      data = list(reader)

      if len(data) <= 1:
        self.expense_textbox.insert("end", "No expenses recorded yet.")
        return

      header = data[0]
      header_str = f"{header[0]:<12} | {header[1]:<15} | {header[2]:<10} | {header[3]}\n"
      self.expense_textbox.insert("end", header_str)
      self.expense_textbox.insert("end", "-" * 65 + "\n")

      count = 0
      for row in data[1:]:
        if filter_cat and filter_cat not in row[1].lower():
          continue
        row_str = f"{row[0]:<12} | {row[1]:<15} | ₹{row[2]:<9} | {row[3]}\n"
        self.expense_textbox.insert("end", row_str)
        count += 1

      if count == 0 and filter_cat:
        self.expense_textbox.insert(
            "end", f"No records found for category '{filter_cat}'."
        )

  # ==================== TAB 3: SUMMARY STATS ====================
  def setup_summary_tab(self):
    ctk.CTkLabel(
        self.tab_view.tab("📊 Summary Stats"),
        text="Category Spending Breakdown",
        font=ctk.CTkFont(size=16, weight="bold"),
    ).pack(pady=10)

    self.summary_textbox = ctk.CTkTextbox(
        self.tab_view.tab("📊 Summary Stats"), width=620, height=310, font=("Courier", 13)
    )
    self.summary_textbox.pack(pady=10)
    self.load_summary_data()

  def load_summary_data(self):
    if not hasattr(self, "summary_textbox"):
      return
    self.summary_textbox.delete("1.0", "end")

    if not os.path.exists(FILENAME):
      self.summary_textbox.insert("end", "No expense records found.")
      return

    summary = defaultdict(float)
    total_spent = 0.0

    with open(FILENAME, mode="r", encoding="utf-8") as file:
      reader = csv.reader(file)
      data = list(reader)

      for row in data[1:]:
        try:
          category = row[1]
          amount = float(row[2])
          summary[category] += amount
          total_spent += amount
        except (ValueError, IndexError):
          continue

    if not summary:
      self.summary_textbox.insert("end", "No data available for summary.")
      return

    self.summary_textbox.insert(
        "end", f"{'Category':<20} | {'Total Spent':<15}\n"
    )
    self.summary_textbox.insert("end", "-" * 40 + "\n")
    for cat, amt in summary.items():
      self.summary_textbox.insert("end", f"{cat:<20} | ₹{amt:<15.2f}\n")
    self.summary_textbox.insert("end", "-" * 40 + "\n")
    self.summary_textbox.insert(
        "end", f"{'GRAND TOTAL':<20} | ₹{total_spent:<15.2f}\n"
    )


if __name__ == "__main__":
  app = ExpenseTrackerApp()
  app.mainloop()
