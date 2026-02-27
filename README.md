# 🔍 Inventory Auditor: Everest vs. Website

A specialized GUI utility designed to reconcile product databases. It compares an **Everest** (Master) spreadsheet against a **Website** export to identify products that are missing from the online store.

## 🎯 Purpose
This tool automates the process of checking if all parts from your internal system have been successfully uploaded to your website. It eliminates the manual "VLOOKUP" or "Find" tasks in Excel.



## ✨ Key Features
* **Multi-Format Support:** Processes both `.csv` and Excel (`.xlsx`, `.xls`) files.
* **Smart Matching:** * **Case-Insensitive:** Matches `A123` to `a123` automatically.
    * **Auto-Trim:** Removes accidental leading/trailing spaces in filenames or cells.
* **Safety Features:** * Validates column names (`Code` and `Sku`) before running.
    * Handles "Not Found" errors without crashing.
* **One-Click Export:** Quickly copy the list of missing parts to your clipboard or save them to a `.txt` file.

## 🚀 How to Run
1.  **Install Dependencies:**
    Open your terminal or command prompt and run:
    ```bash
    pip install pandas openpyxl pyperclip
    ```
2.  **Launch the App:**
    Run the script via IDLE, VS Code, or your terminal:
    ```bash
    python inventory_auditor.py
    ```
3.  **Compare:**
    * Select your **Everest** file (must have a column named `Code`).
    * Select your **Website** file (must have a column named `Sku`).
    * Click **Compare Files** to see the results.

## 📊 Expected Data Format
| File Type | Required Column Name |
| :--- | :--- |
| **Everest Export** | `Code` |
| **Website Export** | `Sku` |

---
*Note: This tool requires the `pandas` library for high-speed data processing.*
