import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import matplotlib.pyplot as plt
import csv
from fpdf import FPDF
from tkcalendar import DateEntry

class ExpansesTracker:
    def __init__(self, root):
        self.expenses = []
        self.total_amount = 0
        root.title("Expanses Tracker")
        root.geometry("600x700")
        root.config(bg='#f0f0f0')

        # Title
        self.title_label = tk.Label(root, text="Expanses Tracker", font=("Arial", 18, "bold"), bg='#f0f0f0')
        self.title_label.pack(pady=10)

        # Entry fields section
        input_container = tk.Frame(root, bg='#f0f0f0')
        input_container.pack(pady=10)

        # Description input
        tk.Label(input_container, text="Description", font=("Arial", 12), bg='#f0f0f0').grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.description_entry = self.create_entry(input_container)
        self.description_entry.grid(row=0, column=1, padx=10, pady=5)

        # Amount input
        tk.Label(input_container, text="Amount", font=("Arial", 12), bg='#f0f0f0').grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.amount_entry = self.create_entry(input_container)
        self.amount_entry.grid(row=1, column=1, padx=10, pady=5)

        # Date input with DateEntry
        tk.Label(input_container, text="Date", font=("Arial", 12), bg='#f0f0f0').grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.date_entry = DateEntry(input_container, width=27, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.date_entry.grid(row=2, column=1, padx=10, pady=5)
        
        # Category selection
        tk.Label(input_container, text="Category", font=("Arial", 12), bg='#f0f0f0').grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.category_var = tk.StringVar()
        self.category_combobox = ttk.Combobox(input_container, textvariable=self.category_var)
        self.category_combobox['values'] = ('Food', 'Transportation', 'Entertainment', 'Utilities', 'Other')
        self.category_combobox.grid(row=3, column=1, padx=10, pady=5)

        # Button container for adding and exporting expenses
        button_container = tk.Frame(root, bg='#f0f0f0')
        button_container.pack(pady=10)

        self.add_button = tk.Button(button_container, text="Add Expanses", command=self.add_expense, font=("Arial", 10), bg='#4caf50', fg='white', width=15)
        self.add_button.pack(side=tk.LEFT, padx=10)

        self.export_button = tk.Button(button_container, text="Export to CSV", command=self.export_csv, font=("Arial", 10), bg='#2196f3', fg='white', width=15)
        self.export_button.pack(side=tk.LEFT)

        self.export_pdf_button = tk.Button(button_container, text="Export to PDF", command=self.export_pdf, font=("Arial", 10), bg='#ff9800', fg='white', width=15)
        self.export_pdf_button.pack(side=tk.LEFT)

        # Search bar
        search_container = tk.Frame(root, bg='#f0f0f0')
        search_container.pack(pady=10)
        
        self.search_label = tk.Label(search_container, text="Search", font=("Arial", 12), bg='#f0f0f0')
        self.search_label.grid(row=0, column=0, padx=10, pady=5)
        
        self.search_entry = self.create_entry(search_container)
        self.search_entry.grid(row=0, column=1, padx=10, pady=5)
        self.search_entry.bind("<KeyRelease>", self.search_expenses)

        # Expense List
        self.expense_list = ttk.Treeview(root, columns=('Description', 'Amount', 'Date', 'Category'), show='headings', height=8)
        self.expense_list.column('Description', width=200)
        self.expense_list.column('Amount', width=100)
        self.expense_list.column('Date', width=100)
        self.expense_list.column('Category', width=150)
        self.expense_list.heading('Description', text="Description")
        self.expense_list.heading('Amount', text="Amount (₹)")
        self.expense_list.heading('Date', text="Date")
        self.expense_list.heading('Category', text="Category")
        self.expense_list.pack(pady=10)

        # Total amount label at the bottom
        self.total_label = tk.Label(root, text="Total Amount: ₹0", font=("Arial", 12), bg='#f0f0f0')
        self.total_label.pack(pady=5)

        # View Graph Button
        self.view_button = tk.Button(root, text="View Graph", command=self.view_graph, font=("Arial", 10), bg='#ff5722', fg='white', width=15)
        self.view_button.pack(pady=10)

        # Delete and Reset buttons side by side
        action_container = tk.Frame(root, bg='#f0f0f0')
        action_container.pack(pady=10)

        self.delete_button = tk.Button(action_container, text="Delete Selected", command=self.delete_expense, font=("Arial", 10), bg='#f44336', fg='white', width=15, height=2)
        self.delete_button.pack(side=tk.LEFT, padx=10)

        self.reset_button = tk.Button(action_container, text="Reset All", command=self.reset_expenses, font=("Arial", 10), bg='#ff9800', fg='white', width=15, height=2)
        self.reset_button.pack(side=tk.LEFT, padx=10)

    def create_entry(self, container):
        entry = tk.Entry(container, width=30, font=("Arial", 12))
        return entry

    def add_expense(self):
        description = self.description_entry.get()
        amount = self.amount_entry.get()
        date = self.date_entry.get_date()
        category = self.category_var.get()

        if description and amount.isdigit() and date and category:
            self.expenses.append((description, int(amount), date, category))
            self.total_amount += int(amount)
            self.expense_list.insert('', 'end', values=(description, amount, date, category))
            self.update_total_label()
            messagebox.showinfo("Success", "Expense Added")
            
            # Clear entries after adding
            self.description_entry.delete(0, tk.END)
            self.amount_entry.delete(0, tk.END)
            self.date_entry.set_date(datetime.today())
            self.category_var.set('')
        else:
            messagebox.showerror("Error", "Please enter valid data.")

    def delete_expense(self):
        selected_item = self.expense_list.selection()
        if selected_item:
            values = self.expense_list.item(selected_item)['values']
            amount = int(values[1])
            self.expenses.remove((values[0], amount, values[2], values[3]))
            self.total_amount -= amount
            self.expense_list.delete(selected_item)
            self.update_total_label()
            messagebox.showinfo("Success", "Expense Deleted")
        else:
            messagebox.showerror("Error", "Please select an expense to delete.")

    def reset_expenses(self):
        if messagebox.askyesno("Reset", "Are you sure you want to reset all expenses?"):
            self.expenses.clear()
            self.total_amount = 0
            self.expense_list.delete(*self.expense_list.get_children())
            self.update_total_label()
            messagebox.showinfo("Reset", "All expenses have been reset.")

    def update_total_label(self):
        self.total_label.config(text=f"Total Amount: ₹{self.total_amount}")

    def search_expenses(self, event):
        search_term = self.search_entry.get().lower()
        for item in self.expense_list.get_children():
            self.expense_list.delete(item)
        for desc, amt, date, cat in self.expenses:
            if search_term in desc.lower():
                self.expense_list.insert('', 'end', values=(desc, amt, date, cat))

    def view_graph(self):
        if not self.expenses:
            messagebox.showerror("Error", "No expenses to display.")
            return

        categories = {}
        for _, _, _, category in self.expenses:
            categories[category] = categories.get(category, 0) + 1
        
        plt.figure(figsize=(8, 6))
        plt.pie(categories.values(), labels=categories.keys(), autopct='%1.1f%%')
        plt.title("Expense Distribution")
        plt.show()

    def export_csv(self):
        try:
            with open("expenses.csv", mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Description', 'Amount', 'Date', 'Category'])
                for expense in self.expenses:
                    writer.writerow(expense)
            messagebox.showinfo("Success", "Data exported to expenses.csv")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export CSV: {e}")

    def export_pdf(self):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt="Expanses Tracker Report", ln=True, align='C')
        pdf.cell(200, 10, txt="", ln=True)  # Empty line
        
        pdf.cell(50, 10, txt="Description", border=1)
        pdf.cell(30, 10, txt="Amount (in INR)", border=1)  # Changed header to avoid the currency symbol
        pdf.cell(50, 10, txt="Date", border=1)
        pdf.cell(50, 10, txt="Category", border=1)
        pdf.ln()

        for expense in self.expenses:
            pdf.cell(50, 10, txt=expense[0].encode('latin-1', 'replace').decode('latin-1'), border=1)  # Encode to handle special characters
            pdf.cell(30, 10, txt=str(expense[1]), border=1)
            pdf.cell(50, 10, txt=str(expense[2]), border=1)
            pdf.cell(50, 10, txt=expense[3].encode('latin-1', 'replace').decode('latin-1'), border=1)  # Encode to handle special characters
            pdf.ln()

        pdf.cell(200, 10, txt="", ln=True)  # Empty line
        pdf.cell(50, 10, txt="Total Amount:", border=1)
        pdf.cell(30, 10, txt=str(self.total_amount), border=1)
        pdf.cell(50, 10, txt="", border=1)
        pdf.cell(50, 10, txt="", border=1)
        
        pdf.output("expenses.pdf")
        messagebox.showinfo("Success", "Data exported to expenses.pdf")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpansesTracker(root)
    root.mainloop()
