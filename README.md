# 🌌 D‑ning – Data Cleaning Website

## 📌 Overview
**D‑ning** is a web application for cleaning impure Excel or CSV files.  
You can upload files containing null values or duplicates, and the app will process them by:
- Replacing missing values with **mean** or **median**.
- Assigning proper numbering for primary keys if missing.
- Removing duplicate rows.

After processing, you can **download the cleaned files** instantly.

---

## ✨ Features
✅ Upload **multiple files** (CSV/Excel) at once.  
✅ Choose how to handle missing values: **Mean** or **Median**.  
✅ Automatic removal of duplicates.  
✅ Automatic primary key assignment if needed.  
✅ **Dark-themed dashboard** with a clean layout.  
✅ **Download** the processed files in the same format (CSV/Excel).  
✅ Static header and footer with contact information.

---

## 🛠️ Tools and Technologies
- **Frontend:** HTML, CSS, JavaScript  
- **Backend:** Python (Flask)  
- **Libraries:** pandas, openpyxl

---

## 📦 Requirements
Make sure you have Python installed.  
Install dependencies with:
```bash
pip install flask pandas openpyxl
