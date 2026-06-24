import pandas as pd
import os

# -------- FILE PATHS --------
base_dir = os.path.dirname(os.path.dirname(__file__))

file1 = os.path.join(base_dir, "data", "final_legal_risk_dataset_150plus.csv")
file2 = os.path.join(base_dir, "data", "legal_dataset_500.csv")

output_file = os.path.join(base_dir, "data", "final_legal_dataset.csv")

# -------- LOAD DATA --------
df1 = pd.read_csv(file1)
df2 = pd.read_csv(file2)

print("Dataset 1 shape:", df1.shape)
print("Dataset 2 shape:", df2.shape)

# -------- STANDARDIZE COLUMN NAMES --------
df1.columns = df1.columns.str.strip()
df2.columns = df2.columns.str.strip()

# Rename if needed
if "Risk" in df1.columns:
    df1.rename(columns={"Risk": "Risk_Level"}, inplace=True)

# -------- KEEP REQUIRED COLUMNS --------
df1 = df1[["Clause", "Category", "Risk_Level"]]
df2 = df2[["Clause", "Category", "Risk_Level"]]

# -------- MERGE --------
df = pd.concat([df1, df2], ignore_index=True)

print("Merged shape before cleaning:", df.shape)

# -------- CLEAN DATA --------
df.dropna(inplace=True)
df.drop_duplicates(subset=["Clause", "Category"], inplace=True)

# Strip spaces
df["Clause"] = df["Clause"].str.strip()
df["Category"] = df["Category"].str.strip()
df["Risk_Level"] = df["Risk_Level"].str.strip()

# -------- FIX LABELS --------
df["Category"] = df["Category"].str.replace(" ", "_")
df["Risk_Level"] = df["Risk_Level"].str.capitalize()

# -------- SAVE --------
df.to_csv(output_file, index=False)

print("\n✅ FINAL DATASET CREATED!")
print("Final shape:", df.shape)
print("Saved at:", output_file)