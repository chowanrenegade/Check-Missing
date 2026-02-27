import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import pyperclip  # You may need to run: pip install pyperclip

def load_file(file_path):
    """Load CSV or Excel file and return DataFrame."""
    if file_path.endswith('.csv'):
        return pd.read_csv(file_path)
    elif file_path.endswith(('.xlsx', '.xls')):
        return pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file type. Please select CSV or Excel files.")

def get_column_data(df, target_name):
    """Helper to find a column even if the capitalization is different."""
    actual_col = next((col for col in df.columns if col.strip().lower() == target_name.lower()), None)
    if actual_col:
        return set(df[actual_col].astype(str).str.strip().str.upper().unique())
    else:
        raise KeyError(f"Could not find a column named '{target_name}'")

def find_missing_parts(everest_file, website_file):
    """Finds parts in Everest (Code) that are missing from Website (Sku)."""
    try:
        everest_df = load_file(everest_file)
        everest_parts = get_column_data(everest_df, "Code")

        website_df = load_file(website_file)
        website_parts = get_column_data(website_df, "Sku")

        return sorted(list(everest_parts - website_parts))
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
        return None

def select_everest():
    path = filedialog.askopenfilename(title="Select Everest File", filetypes=[("Spreadsheets", "*.csv *.xlsx *.xls")])
    if path: everest_var.set(path)

def select_website():
    path = filedialog.askopenfilename(title="Select Website File", filetypes=[("Spreadsheets", "*.csv *.xlsx *.xls")])
    if path: website_var.set(path)

def run_check():
    everest_path = everest_var.get()
    website_path = website_var.get()

    if not everest_path or not website_path:
        messagebox.showwarning("Warning", "Please select both files.")
        return

    missing = find_missing_parts(everest_path, website_path)
    
    if missing is not None:
        result_text.delete(1.0, tk.END)
        if not missing:
            result_text.insert(tk.END, "SUCCESS: All Everest items are present on the Website.")
        else:
            result_text.insert(tk.END, "\n".join(missing))
        
        # Enable the save/copy buttons if there are results
        btn_save.config(state=tk.NORMAL)
        btn_copy.config(state=tk.NORMAL)

def save_to_txt():
    """Manually save the current results to a file chosen by the user."""
    content = result_text.get(1.0, tk.END).strip()
    if not content or "SUCCESS" in content:
        messagebox.showwarning("Empty", "Nothing to save.")
        return
        
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt")],
        initialfile="missing_parts_report.txt"
    )
    if file_path:
        with open(file_path, 'w') as f:
            f.write(content)
        messagebox.showinfo("Saved", "File saved successfully.")

def copy_to_clipboard():
    """Copy the results text to the system clipboard."""
    content = result_text.get(1.0, tk.END).strip()
    if content:
        pyperclip.copy(content)
        messagebox.showinfo("Copied", "List copied to clipboard!")

# --- GUI Setup ---
root = tk.Tk()
root.title("Inventory Auditor: Everest vs. Website")

everest_var = tk.StringVar()
website_var = tk.StringVar()

# Everest Selection
tk.Label(root, text="Everest File (Code):", font=('Arial', 10, 'bold')).grid(row=0, column=0, padx=10, pady=10, sticky="e")
tk.Entry(root, textvariable=everest_var, width=50).grid(row=0, column=1)
tk.Button(root, text="Browse", command=select_everest).grid(row=0, column=2, padx=10)

# Website Selection
tk.Label(root, text="Website File (Sku):", font=('Arial', 10, 'bold')).grid(row=1, column=0, padx=10, pady=10, sticky="e")
tk.Entry(root, textvariable=website_var, width=50).grid(row=1, column=1)
tk.Button(root, text="Browse", command=select_website).grid(row=1, column=2, padx=10)

# Run Button
tk.Button(root, text="Compare Files", command=run_check, bg="#27ae60", fg="white", font=('Arial', 11, 'bold'), height=1).grid(row=2, column=0, columnspan=3, pady=15)

# Results Display
result_text = scrolledtext.ScrolledText(root, width=80, height=15, font=('Consolas', 10))
result_text.grid(row=3, column=0, columnspan=3, padx=15, pady=5)

# Bottom Button Frame
btn_frame = tk.Frame(root)
btn_frame.grid(row=4, column=0, columnspan=3, pady=10)

btn_save = tk.Button(btn_frame, text="💾 Save to TXT", command=save_to_txt, state=tk.DISABLED, width=15)
btn_save.pack(side=tk.LEFT, padx=10)

btn_copy = tk.Button(btn_frame, text="📋 Copy to Clipboard", command=copy_to_clipboard, state=tk.DISABLED, width=20)
btn_copy.pack(side=tk.LEFT, padx=10)

root.mainloop()