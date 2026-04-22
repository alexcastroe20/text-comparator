import tkinter as tk
from tkinter import filedialog, messagebox
import difflib
import webbrowser
import os

def select_file1():
    filepath = filedialog.askopenfilename(title="Select the original file", filetypes=[("CSV Files", "*.csv"), ("Text Files", "*.txt")])
    if filepath:
        lbl_file1.config(text=filepath)
        window.filepath_1 = filepath

def select_file2():
    filepath = filedialog.askopenfilename(title="Select the modified file", filetypes=[("CSV Files", "*.csv"), ("Text Files", "*.txt")])
    if filepath:
        lbl_file2.config(text=filepath)
        window.filepath_2 = filepath

def compare_files():
    if not hasattr(window, 'filepath_1') or not hasattr(window, 'filepath_2'):
        messagebox.showwarning("Attention", "Please select both files first.")
        return

    try:
        # Read the files
        with open(window.filepath_1, 'r', encoding='utf-8') as f1, \
             open(window.filepath_2, 'r', encoding='utf-8') as f2:
            lines1 = f1.readlines()
            lines2 = f2.readlines()

        # Generate an interactive HTML file with differences (side-by-side)
        html_generator = difflib.HtmlDiff()
        html_output = html_generator.make_file(lines1, lines2, context=True, numlines=5)

        # Save the temporary HTML and open it in the browser
        output_path = os.path.abspath("comparison_result.html")
        with open(output_path, 'w', encoding='utf-8') as f_out:
            f_out.write(html_output)

        webbrowser.open('file://' + output_path)
        messagebox.showinfo("Success", "Comparison finished. Opened in your web browser.")

    except Exception as e:
        messagebox.showerror("Error", f"There was a problem comparing the files: {e}")

# --- GUI CONFIGURATION ---
window = tk.Tk()
window.title("CSV File Comparator")
window.geometry("400x250")
window.eval('tk::PlaceWindow . center') # Center the window

# UI Elements
tk.Label(window, text="1. Select the ORIGINAL file:").pack(pady=(15, 0))
btn_file1 = tk.Button(window, text="Browse File...", command=select_file1)
btn_file1.pack()
lbl_file1 = tk.Label(window, text="(No file selected)", fg="gray", font=("Arial", 8))
lbl_file1.pack()

tk.Label(window, text="2. Select the MODIFIED file:").pack(pady=(15, 0))
btn_file2 = tk.Button(window, text="Browse File...", command=select_file2)
btn_file2.pack()
lbl_file2 = tk.Label(window, text="(No file selected)", fg="gray", font=("Arial", 8))
lbl_file2.pack()

btn_compare = tk.Button(window, text="⚡ COMPARE FILES ⚡", command=compare_files, bg="lightblue", font=("Arial", 10, "bold"))
btn_compare.pack(pady=20)

window.mainloop()