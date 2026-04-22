import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import csv
from itertools import zip_longest

def select_file1():
    filepath = filedialog.askopenfilename(title="Select the original file", filetypes=[("CSV Files", "*.csv")])
    if filepath:
        lbl_file1.config(text=filepath)
        window.filepath_1 = filepath

def select_file2():
    filepath = filedialog.askopenfilename(title="Select the modified file", filetypes=[("CSV Files", "*.csv")])
    if filepath:
        lbl_file2.config(text=filepath)
        window.filepath_2 = filepath

def compare_files():
    if not hasattr(window, 'filepath_1') or not hasattr(window, 'filepath_2'):
        messagebox.showwarning("Attention", "Please select both files first.")
        return

    # Clear previous results from the table
    for item in results_table.get_children():
        results_table.delete(item)

    try:
        with open(window.filepath_1, 'r', encoding='utf-8') as f1, \
             open(window.filepath_2, 'r', encoding='utf-8') as f2:

            reader1 = list(csv.reader(f1))
            reader2 = list(csv.reader(f2))

        # Assume the first row contains the column headers
        headers = reader1[0] if reader1 else []
        differences_found = False

        # Compare row by row and column by column
        for row_num, (row1, row2) in enumerate(zip_longest(reader1, reader2, fillvalue=[]), start=1):
            for col_num, (val1, val2) in enumerate(zip_longest(row1, row2, fillvalue="[Empty]")):
                if val1 != val2:
                    differences_found = True
                    col_name = headers[col_num] if col_num < len(headers) else f"Col {col_num + 1}"

                    # Insert the detected difference into the table
                    results_table.insert("", "end", values=(f"Row {row_num}", col_name, val1, val2))

        if not differences_found:
            messagebox.showinfo("Result", "The files are exactly the same!")

    except Exception as e:
        messagebox.showerror("Error", f"There was a problem reading the CSVs: {e}")

# --- GUI CONFIGURATION ---
window = tk.Tk()
window.title("Integrated CSV Comparator")
window.geometry("700x500") # Larger window to fit the table
window.eval('tk::PlaceWindow . center') # Center the window on the screen

# Top elements (File selection)
frame_top = tk.Frame(window)
frame_top.pack(pady=10)

tk.Label(frame_top, text="1. ORIGINAL File:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
lbl_file1 = tk.Label(frame_top, text="(None)", fg="gray", width=40, anchor="w")
lbl_file1.grid(row=0, column=1, padx=10, pady=5)
tk.Button(frame_top, text="Browse...", command=select_file1).grid(row=0, column=2, padx=10, pady=5)

tk.Label(frame_top, text="2. MODIFIED File:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
lbl_file2 = tk.Label(frame_top, text="(None)", fg="gray", width=40, anchor="w")
lbl_file2.grid(row=1, column=1, padx=10, pady=5)
tk.Button(frame_top, text="Browse...", command=select_file2).grid(row=1, column=2, padx=10, pady=5)

btn_compare = tk.Button(window, text="⚡ FIND DIFFERENCES ⚡", command=compare_files, bg="lightblue", font=("Arial", 10, "bold"))
btn_compare.pack(pady=10)

# --- RESULTS TABLE (Treeview) ---
frame_table = tk.Frame(window)
frame_table.pack(fill="both", expand=True, padx=20, pady=10)

# Define columns
columns = ("row", "column", "original", "modified")
results_table = ttk.Treeview(frame_table, columns=columns, show="headings")

# Configure table headers
results_table.heading("row", text="Row")
results_table.heading("column", text="Affected Column")
results_table.heading("original", text="Original Value (1)")
results_table.heading("modified", text="New Value (2)")

# Configure column widths and alignment
results_table.column("row", width=80, anchor="center")
results_table.column("column", width=120, anchor="center")
results_table.column("original", width=200)
results_table.column("modified", width=200)

# Add scrollbar (vital for large CSVs)
scrollbar = ttk.Scrollbar(frame_table, orient=tk.VERTICAL, command=results_table.yview)
results_table.configure(yscroll=scrollbar.set)

scrollbar.pack(side="right", fill="y")
results_table.pack(side="left", fill="both", expand=True)

window.mainloop()
