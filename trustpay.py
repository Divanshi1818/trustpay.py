import tkinter as tk
import tkinter as tkpython 
from tkinter import filedialog, messagebox
from tkinter import ttk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from PIL import Image, ImageTk
# -----------------------------
# Global Variables
# -----------------------------
df = None
# -----------------------------
# Check Dataset
# -----------------------------
def check_dataset():
    if df is None:
        messagebox.showwarning("Warning", "Please Load Dataset First.")
        return False
    return True
# -----------------------------
# Load Dataset
# -----------------------------
def load_dataset():
    global df
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path == "":
        return
    try:
        df = pd.read_csv(file_path)
        output.delete(1.0, tk.END)
        output.insert(tk.END, "=====================================\n")
        output.insert(tk.END, " TrustPay Banking System\n")
        output.insert(tk.END, "=====================================\n\n")
        output.insert(tk.END, "Dataset Loaded Successfully\n\n")
        output.insert(tk.END, f"Rows : {df.shape[0]}\n")
        output.insert(tk.END, f"Columns : {df.shape[1]}\n\n")
        output.insert(tk.END, "Columns Present\n")
        output.insert(tk.END, "-------------------------\n")
        for col in df.columns:
            output.insert(tk.END, col + "\n")
        # Update KPI Labels
        total_value.config(text=str(len(df)))
        if "fraud_flag" in df.columns:
            fraud = int(df["fraud_flag"].sum())
            fraud_value.config(text=str(fraud))
            safe_value.config(text=str(len(df) - fraud))
        if "transaction_amount" in df.columns:
            avg = df["transaction_amount"].mean()
            amount_value.config(text=f"{avg:.2f}")
            
        status.config(text="Dataset loaded successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))
# -----------------------------
# Dataset Information
# -----------------------------
def dataset_info():
    if not check_dataset():
        return
    output.delete(1.0, tk.END)
    output.insert(tk.END, "DATASET INFORMATION\n\n")
    output.insert(tk.END, f"Rows : {df.shape[0]}\n")
    output.insert(tk.END, f"Columns : {df.shape[1]}\n\n")
    output.insert(tk.END, "Column Data Types\n")
    output.insert(tk.END, "----------------------\n")
    output.insert(tk.END, str(df.dtypes))
# -----------------------------
# Show Dataset
# -----------------------------
def show_data():
    if not check_dataset():
        return
    table.delete(*table.get_children())
    for i, (_, row) in enumerate(df.head(100).iterrows()):
        tag = "even" if i % 2 == 0 else "odd"
        table.insert(
            "",
            tk.END,
            values=(
                row.get("transaction_id", ""),
                row.get("transaction_amount", ""),
                row.get("payment_channel", ""),
                row.get("authentication_type", ""),
                row.get("fraud_flag", "")
            ),
            tags=(tag,)
        )
# -----------------------------
# Statistics
# -----------------------------
def statistics():
    if not check_dataset():
        return
    if "transaction_amount" not in df.columns:
        messagebox.showerror("Error", "transaction_amount column not found.")
        return
    amount = df["transaction_amount"]
    output.delete(1.0, tk.END)
    output.insert(tk.END, "TRANSACTION STATISTICS\n\n")
    output.insert(tk.END, f"Mean : {np.mean(amount):.2f}\n")
    output.insert(tk.END, f"Median : {np.median(amount):.2f}\n")
    output.insert(tk.END, f"Maximum : {np.max(amount):.2f}\n")
    output.insert(tk.END, f"Minimum : {np.min(amount):.2f}\n")
    output.insert(tk.END, f"Standard Deviation : {np.std(amount):.2f}\n")
    output.insert(tk.END, f"Variance : {np.var(amount):.2f}\n")
# -----------------------------
# Fraud Transactions
# -----------------------------
def suspicious_transactions():
    if not check_dataset():
        return
    if "fraud_flag" not in df.columns:
        messagebox.showerror("Error", "fraud_flag column not found.")
        return
    fraud = df[df["fraud_flag"] == 1]
    output.delete(1.0, tk.END)
    output.insert(tk.END, "FRAUD TRANSACTIONS\n\n")
    output.insert(tk.END, f"Total Fraud Transactions : {len(fraud)}\n\n")
    output.insert(tk.END, str(fraud.head(20)))
# -----------------------------
# Payment Analysis
# -----------------------------
def payment_analysis():
    if not check_dataset():
        return
    if "payment_channel" not in df.columns:
        messagebox.showerror("Error", "payment_channel column not found.")
        return
    payment = df["payment_channel"].value_counts()
    output.delete(1.0, tk.END)
    output.insert(tk.END, "PAYMENT CHANNEL ANALYSIS\n\n")
    output.insert(tk.END, str(payment))
# -----------------------------
# Authentication Analysis
# -----------------------------
def authentication_analysis():
    if not check_dataset():
        return
    if "authentication_type" not in df.columns:
        messagebox.showerror("Error", "authentication_type column not found.")
        return
    auth = df["authentication_type"].value_counts()
    output.delete(1.0, tk.END)
    output.insert(tk.END, "AUTHENTICATION ANALYSIS\n\n")
    output.insert(tk.END, str(auth))
# -----------------------------
# Fraud Analysis
# -----------------------------
def fraud_analysis():
    if not check_dataset():
        return
    if "fraud_flag" not in df.columns:
        messagebox.showerror("Error", "fraud_flag column not found.")
        return
    fraud = df["fraud_flag"].value_counts()
    output.delete(1.0, tk.END)
    output.insert(tk.END, "FRAUD ANALYSIS\n\n")
    output.insert(tk.END, str(fraud))
# -----------------------------
# Correlation Analysis
# -----------------------------
def correlation_analysis():
    if not check_dataset():
        return
    numeric_df = df.select_dtypes(include=np.number)
    if numeric_df.empty:
        messagebox.showerror("Error", "No numeric columns available.")
        return
    corr = numeric_df.corr()
    output.delete(1.0, tk.END)
    output.insert(tk.END, "CORRELATION MATRIX\n\n")
    output.insert(tk.END, str(corr))
# -----------------------------
# Dataset Summary
# -----------------------------
def dataset_summary():
    if not check_dataset():
        return
    output.delete(1.0, tk.END)
    output.insert(tk.END, "DATASET SUMMARY DESCRIPTION\n\n")
    output.insert(tk.END, str(df.describe(include='all')))
# -----------------------------
# Payment Channel Bar Chart
# -----------------------------
from PIL import Image, ImageTk
def payment_chart():
    if not check_dataset():
        return
    if "payment_channel" not in df.columns:
        messagebox.showerror("Error", "payment_channel column not found.")
        return
    plt.figure(figsize=(8,5))
    df["payment_channel"].value_counts().plot(
        kind="bar",
        color="royalblue",
        edgecolor="black"
    )
    plt.title("Payment Channel Analysis")
    plt.xlabel("Payment Channel")
    plt.ylabel("Transactions")
    plt.grid(axis="y", linestyle="--", alpha=0.6)
    plt.tight_layout()
    # Save chart
    path = "payment_chart.png"
    plt.savefig(path)
    plt.close()
    # Create scrollable window
    top = tk.Toplevel(root)
    top.title("Payment Channel Analysis")
    top.geometry("900x600")
    canvas = tk.Canvas(top)
    scrollbar_y = tk.Scrollbar(top, orient="vertical", command=canvas.yview)
    scrollbar_x = tk.Scrollbar(top, orient="horizontal", command=canvas.xview)
    canvas.configure(
        yscrollcommand=scrollbar_y.set,
        xscrollcommand=scrollbar_x.set
    )
    scrollbar_y.pack(side="right", fill="y")
    scrollbar_x.pack(side="bottom", fill="x")
    canvas.pack(side="left", fill="both", expand=True)
    frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor="nw")
    img = ImageTk.PhotoImage(Image.open(path))
    panel = tk.Label(frame, image=img)
    panel.image = img
    panel.pack()
    frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))
# -----------------------------
# Fraud Pie Chart
# -----------------------------
def fraud_chart():
    if not check_dataset():
        return
    if "fraud_flag" not in df.columns:
        messagebox.showerror("Error", "fraud_flag column not found.")
        return
    plt.figure(figsize=(6,6))
    df["fraud_flag"].value_counts().plot(
        kind="pie",
        autopct="%1.1f%%",
        colors=["#4CAF50", "#E53935"],
        startangle=90
    )
    plt.ylabel("")
    plt.title("Fraud Distribution")
    plt.tight_layout()
    # Save chart
    path = "fraud_chart.png"
    plt.savefig(path)
    plt.close()
    # Create scrollable window
    top = tk.Toplevel(root)
    top.title("Fraud Distribution")
    top.geometry("700x600")
    canvas = tk.Canvas(top)
    scrollbar = tk.Scrollbar(top, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor="nw")
    img = ImageTk.PhotoImage(Image.open(path))
    panel = tk.Label(frame, image=img)
    panel.image = img
    panel.pack(padx=10, pady=10)
    frame.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))
# -----------------------------
# Transaction Amount Histogram
# -----------------------------
def amount_histogram():
    if not check_dataset():
        return
    if "transaction_amount" not in df.columns:
        messagebox.showerror("Error", "transaction_amount column not found.")
        return
    plt.figure(figsize=(8,5))
    plt.hist(
        df["transaction_amount"],
        bins=20,
        color="#1976D2",
        edgecolor="black"
    )
    plt.title("Transaction Amount Distribution")
    plt.xlabel("Transaction Amount")
    plt.ylabel("Frequency")
    plt.grid(alpha=0.4)
    plt.tight_layout()
    # Save chart
    path = "amount_histogram.png"
    plt.savefig(path)
    plt.close()
    # Create scrollable window
    top = tk.Toplevel(root)
    top.title("Transaction Amount Distribution")
    top.geometry("900x600")
    canvas = tk.Canvas(top)
    scrollbar_y = tk.Scrollbar(top, orient="vertical", command=canvas.yview)
    scrollbar_x = tk.Scrollbar(top, orient="horizontal", command=canvas.xview)
    canvas.configure(
        yscrollcommand=scrollbar_y.set,
        xscrollcommand=scrollbar_x.set
    )
    scrollbar_y.pack(side="right", fill="y")
    scrollbar_x.pack(side="bottom", fill="x")
    canvas.pack(side="left", fill="both", expand=True)
    frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor="nw")
    img = ImageTk.PhotoImage(Image.open(path))
    panel = tk.Label(frame, image=img)
    panel.image = img
    panel.pack()
    frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))
# -----------------------------
# Scatter Plot
# -----------------------------
def scatter_plot():
    if not check_dataset():
        return
    if "transaction_amount" not in df.columns or "fraud_flag" not in df.columns:
        messagebox.showerror("Error", "Required columns missing.")
        return
    plt.figure(figsize=(8,5))
    plt.scatter(
        df["transaction_amount"],
        df["fraud_flag"],
        color="crimson",
        alpha=0.5
    )
    plt.title("Transaction Amount vs Fraud")
    plt.xlabel("Transaction Amount")
    plt.ylabel("Fraud Flag")
    plt.grid(alpha=0.5)
    plt.tight_layout()
    # Save chart
    path = "scatter_plot.png"
    plt.savefig(path)
    plt.close()
    # Create scrollable window
    top = tk.Toplevel(root)
    top.title("Transaction Amount vs Fraud")
    top.geometry("900x600")
    canvas = tk.Canvas(top)
    scrollbar_y = tk.Scrollbar(top, orient="vertical", command=canvas.yview)
    scrollbar_x = tk.Scrollbar(top, orient="horizontal", command=canvas.xview)
    canvas.configure(
        yscrollcommand=scrollbar_y.set,
        xscrollcommand=scrollbar_x.set
    )
    scrollbar_y.pack(side="right", fill="y")
    scrollbar_x.pack(side="bottom", fill="x")
    canvas.pack(side="left", fill="both", expand=True)
    frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor="nw")
    img = ImageTk.PhotoImage(Image.open(path))
    panel = tk.Label(frame, image=img)
    panel.image = img
    panel.pack()
    frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))
# -----------------------------
# Correlation Heatmap
# -----------------------------
def correlation_heatmap():
    if not check_dataset():
        return
    numeric = df.select_dtypes(include=np.number)
    corr = numeric.corr()
    plt.figure(figsize=(8,6))
    plt.imshow(corr, cmap="coolwarm")
    plt.colorbar()
    plt.xticks(range(len(corr.columns)), corr.columns, rotation=90)
    plt.yticks(range(len(corr.columns)), corr.columns)
    plt.title("Correlation Heatmap")
    plt.tight_layout()
    # Save chart
    path = "correlation_heatmap.png"
    plt.savefig(path)
    plt.close()
    # Create scrollable window
    top = tk.Toplevel(root)
    top.title("Correlation Heatmap")
    top.geometry("900x600")
    canvas = tk.Canvas(top)
    scrollbar_y = tk.Scrollbar(top, orient="vertical", command=canvas.yview)
    scrollbar_x = tk.Scrollbar(top, orient="horizontal", command=canvas.xview)
    canvas.configure(
        yscrollcommand=scrollbar_y.set,
        xscrollcommand=scrollbar_x.set
    )
    scrollbar_y.pack(side="right", fill="y")
    scrollbar_x.pack(side="bottom", fill="x")
    canvas.pack(side="left", fill="both", expand=True)
    frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor="nw")
    img = ImageTk.PhotoImage(Image.open(path))
    panel = tk.Label(frame, image=img)
    panel.image = img
    panel.pack()
    frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))
# -----------------------------
# Search Transaction
# -----------------------------
def search_transaction():
    if not check_dataset():
        return
    value = search_box.get().strip()
    if value == "":
        messagebox.showwarning("Warning", "Enter Transaction ID")
        return
    if "transaction_id" not in df.columns:
        messagebox.showerror("Error", "transaction_id column not found.")
        return
    result = df[df["transaction_id"].astype(str) == value]
    output.delete(1.0, tk.END)
    if len(result) == 0:
        output.insert(tk.END, "Transaction Not Found")
    else:
        output.insert(tk.END, str(result))
# -----------------------------
# Export Fraud Transactions
# -----------------------------
def export_fraud():
    if not check_dataset():
        return
    if "fraud_flag" not in df.columns:
        messagebox.showerror("Error", "fraud_flag column not found.")
        return
    fraud = df[df["fraud_flag"] == 1]
    fraud.to_csv("Fraud_Transactions.csv", index=False)
    messagebox.showinfo("Success", "Fraud Transactions Exported Successfully (Fraud_Transactions.csv)")
# -----------------------------
# Reset Dashboard
# -----------------------------
def reset_dashboard():
    global df
    df = None
    output.delete(1.0, tk.END)
    search_box.delete(0, tk.END)
    table.delete(*table.get_children())
    total_value.config(text="0")
    fraud_value.config(text="0")
    safe_value.config(text="0")
    amount_value.config(text="0")
    status.config(text="Dashboard Reset Successful.")
# -----------------------------
# About Project
# -----------------------------
def about():
    messagebox.showinfo(
        "About",
        "TrustPay Banking Transaction Monitoring System\n\nDeveloped Using:\nPythonTkinter, Pandas, NumPy, Matplotlib"
    )
# -----------------------------
# Live Time
# -----------------------------
def update_time():
    current = datetime.now().strftime("%d-%m-%Y   %H:%M:%S")
    time_label.config(text=current)
    root.after(1000, update_time)
# -----------------------------
# Refresh Dashboard
# -----------------------------
def refresh_dashboard():
    if df is None:
        return
    total_value.config(text=str(len(df)))
    if "fraud_flag" in df.columns:
        fraud = int(df["fraud_flag"].sum())
        fraud_value.config(text=str(fraud))
        safe_value.config(text=str(len(df)-fraud))
    if "transaction_amount" in df.columns:
        amount_value.config(text=f"{df['transaction_amount'].mean():.2f}")
    status.config(text="Dashboard Refreshed Successfully")
# =========================================================================
# MAIN WINDOW INITIALIZATION
# ==========================================================================
root = tk.Tk()
root.title("TrustPay Banking Transaction Monitoring System")
root.geometry("1450x850")
root.configure(bg="#F4F6F9")
# ===========================
# HEADER
# ===========================
header = tk.Frame(root, bg="#97144D", height=80)
header.pack(fill="x")
title = tk.Label(header, text="TrustPay Banking Transaction Monitoring System", font=
("Segoe UI", 22, "bold"), bg="#97144D", fg="white")
title.pack(side="left", padx=20, pady=20)
time_label = tk.Label(header, text="", bg="#97144D", fg="white", font=("Segoe UI", 
11, "bold"))
time_label.pack(side="right", padx=20)
update_time()
status_label = tk.Label(header, text="Secure Banking Analytics", font=("Segoe UI", 
11), bg="#97144D", fg="white")
status_label.pack(side="right", padx=20)
# Dashboard Label
dashboard = tk.Label(root, text="Banking Fraud Analytics Dashboard", font=("Segoe UI", 17, "bold"), bg="#F4F6F9", fg="#97144D")
dashboard.pack(pady=5)
# ===========================
# KPI CARDS
# ===========================
card_frame = tk.Frame(root, bg="#F4F6F9")
card_frame.pack(pady=5)
def create_card(parent, title_text):
    card = tk.Frame(parent, bg="white", width=220, height=100, bd=1, relief="solid")
    card.pack(side="left", padx=10)
    card.pack_propagate(False)
    tk.Label(card, text=title_text, bg="white", fg="#555555", font=("Segoe UI", 11, 
"bold")).pack(pady=5)
    value = tk.Label(card, text="0", bg="white", fg="#97144D", font=("Segoe UI", 22, 
"bold"))
    value.pack()
    return value
total_value = create_card(card_frame, "Total Transactions")
fraud_value = create_card(card_frame, "Fraud Detected")
safe_value = create_card(card_frame, "Safe Transactions")
amount_value = create_card(card_frame, "Average Amount")
# ===========================
# UTILITY ACTIONS (Search, Export, Reset, About)
# ===========================
utility_frame = tk.Frame(root, bg="#F4F6F9")
utility_frame.pack(pady=5)
tk.Label(utility_frame, text="Search Transaction ID:", font=("Segoe UI", 10, "bold"), 
bg="#F4F6F9").pack(side="left", padx=5)
search_box = tk.Entry(utility_frame, font=("Segoe UI", 10), width=20)
search_box.pack(side="left", padx=5)
tk.Button(utility_frame, text="Search", command=search_transaction, bg="#97144D", 
fg="white", font=("Segoe UI", 9, "bold")).pack(side="left", padx=5)
tk.Button(utility_frame, text="Export Fraud", command=export_fraud, bg="#2E7D32", 
fg="white", font=("Segoe UI", 9, "bold")).pack(side="left", padx=5)
tk.Button(utility_frame, text="Reset Dashboard", command=reset_dashboard, 
bg="#D32F2F", fg="white", font=("Segoe UI", 9, "bold")).pack(side="left", padx=5)
tk.Button(utility_frame, text="Refresh", command=refresh_dashboard, bg="#1976D2", 
fg="white", font=("Segoe UI", 9, "bold")).pack(side="left", padx=5)
tk.Button(utility_frame, text="About", command=about, bg="#757575", fg="white", 
font=("Segoe UI", 9, "bold")).pack(side="left", padx=5)
# ===========================
# WORKSPACE SPLIT (Left Buttons, Right Output & Table)
# ===========================
workspace = tk.Frame(root, bg="#F4F6F9")
workspace.pack(fill="both", expand=True, padx=10, pady=5)
# Left Side Button Frame
frame = tk.Frame(workspace, bg="#F4F6F9")
frame.pack(side="left", fill="y", padx=10)
button_style = {
    "font": ("Segoe UI", 10, "bold"),
    "bg": "#97144D",
    "fg": "white",
    "activebackground": "#7D0F3D",
    "activeforeground": "white",
    "width": 20,
    "height": 1,
    "cursor": "hand2",
    "bd": 0
}
buttons = [
    ("Load Dataset", load_dataset),
    ("Dataset Info", dataset_info),
    ("Show Data", show_data),
    ("Statistics", statistics),
    ("Fraud Transactions", suspicious_transactions),
    ("Payment Analysis", payment_analysis),
    ("Authentication", authentication_analysis),
    ("Fraud Analysis", fraud_analysis),
    ("Correlation", correlation_analysis),
    ("Payment Chart", payment_chart),
    ("Fraud Chart", fraud_chart),
    ("Histogram", amount_histogram),
    ("Scatter Plot", scatter_plot),
    ("Heatmap", correlation_heatmap),
    ("Dataset Summary", dataset_summary)
]
row, col = 0, 0
for text, cmd in buttons:
    tk.Button(frame, text=text, command=cmd, **button_style).grid(row=row, 
column=col, padx=5, pady=5)
    col += 1
    if col == 2:  # Adjusted to a clean 2-column button layout on the side
        col = 0
        row += 1
# Right Side Visualizer Frame
right_frame = tk.Frame(workspace, bg="#F4F6F9")
right_frame.pack(side="right", fill="both", expand=True)
# Console Output Box
output = tk.Text(right_frame, height=12, font=("Consolas", 10), bg="white", bd=1, 
relief="solid")
output.pack(fill="x", pady=5)
# Transaction Table Frame
table_frame = tk.Frame(right_frame)
table_frame.pack(fill="both", expand=True, pady=5)
scroll_y = tk.Scrollbar(table_frame)
scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
columns = ("Transaction ID", "Amount", "Payment", "Authentication", "Fraud")
table = ttk.Treeview(table_frame, columns=columns, show="headings", 
yscrollcommand=scroll_y.set)
scroll_y.config(command=table.yview)
for col_name in columns:
    table.heading(col_name, text=col_name)
    table.column(col_name, width=120, anchor="center")
table.pack(fill="both", expand=True)
table.tag_configure("odd", background="#F8F8F8")
table.tag_configure("even", background="white")
# Progress Bar & Status Footer
progress = ttk.Progressbar(root, orient="horizontal", length=400, 
mode="determinate")
progress.pack(pady=2)
progress["value"] = 100
status = tk.Label(root, text="System Ready", bd=1, relief="sunken", anchor="w", 
bg="#E0E0E0", font=("Segoe UI", 9))
status.pack(fill="x", side="bottom")
# ===========================
# EXECUTE APPLICATION
# ===========================
root.mainloop()