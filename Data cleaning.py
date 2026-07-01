# ============================================================
# DATA CLEANING SCRIPT
# ============================================================

import pandas as pd
import numpy as np

# ------------------------------------------------------------
# STEP 1: Load Dataset
# ------------------------------------------------------------

df = pd.read_csv("Boof_Agency_Restaurant_Ad_Film_Client_Requests.csv")

print("="*60)
print("Original Dataset")
print("="*60)

print(df.head())
print("\nShape:", df.shape)

# ------------------------------------------------------------
# STEP 2: Check Dataset Information
# ------------------------------------------------------------

print("\nData Types")
print(df.dtypes)

print("\nMissing Values")
print(df.isnull().sum())

print("\nDuplicate Rows:", df.duplicated().sum())

# ------------------------------------------------------------
# STEP 3: Remove Duplicate Rows
# ------------------------------------------------------------

df.drop_duplicates(inplace=True)

print("\nDuplicates Removed!")

# ------------------------------------------------------------
# STEP 4: Remove Extra Spaces
# ------------------------------------------------------------

for col in df.select_dtypes(include="object"):
    df[col] = df[col].str.strip()

print("Extra spaces removed.")

# ------------------------------------------------------------
# STEP 5: Standardize Text
# ------------------------------------------------------------

# City

df["City"] = df["City"].str.title()

# Restaurant Type

df["Restaurant Type"] = df["Restaurant Type"].str.title()

# Campaign Type

df["Campaign Type"] = df["Campaign Type"].str.title()

# Status

df["Status"] = df["Status"].str.title()

# Target Audience

df["Target Audience"] = df["Target Audience"].str.title()

# ------------------------------------------------------------
# STEP 6: Fix Common Spelling Variations
# ------------------------------------------------------------

df["Location Type"] = df["Location Type"].replace({
    "Cafe":"Café",
    "cafe":"Café",
    "restaurant":"Restaurant",
    "studio":"Studio"
})

# ------------------------------------------------------------
# STEP 7: Convert Date
# ------------------------------------------------------------

df["Preferred Date"] = pd.to_datetime(
    df["Preferred Date"],
    errors="coerce"
)

# ------------------------------------------------------------
# STEP 8: Convert Numeric Columns
# ------------------------------------------------------------

df["Budget (USD)"] = pd.to_numeric(
    df["Budget (USD)"],
    errors="coerce"
)

df["Shoot Days"] = pd.to_numeric(
    df["Shoot Days"],
    errors="coerce"
)

# ------------------------------------------------------------
# STEP 9: Handle Missing Values
# ------------------------------------------------------------

# Numeric columns

df["Budget (USD)"].fillna(df["Budget (USD)"].median(), inplace=True)

df["Shoot Days"].fillna(df["Shoot Days"].median(), inplace=True)

# Categorical columns

for col in df.select_dtypes(include="object"):
    df[col].fillna("Unknown", inplace=True)

print("Missing values handled.")

# ------------------------------------------------------------
# STEP 10: Check Outliers (IQR Method)
# ------------------------------------------------------------

Q1 = df["Budget (USD)"].quantile(0.25)

Q3 = df["Budget (USD)"].quantile(0.75)

IQR = Q3 - Q1

lower = Q1 - 1.5 * IQR

upper = Q3 + 1.5 * IQR

outliers = df[
    (df["Budget (USD)"] < lower) |
    (df["Budget (USD)"] > upper)
]

print("\nBudget Outliers:", len(outliers))

# ------------------------------------------------------------
# STEP 11: Create Month Column
# ------------------------------------------------------------

df["Month"] = df["Preferred Date"].dt.month_name()

# ------------------------------------------------------------
# STEP 12: Create Quarter
# ------------------------------------------------------------

df["Quarter"] = df["Preferred Date"].dt.quarter

# ------------------------------------------------------------
# STEP 13: Create Budget Category
# ------------------------------------------------------------

def budget_category(x):
    if x < 7000:
        return "Low"
    elif x < 15000:
        return "Medium"
    else:
        return "High"

df["Budget Category"] = df["Budget (USD)"].apply(budget_category)

# ------------------------------------------------------------
# STEP 14: Create Premium Project Flag
# ------------------------------------------------------------

df["Premium Project"] = np.where(
    (df["Drone"] == "Yes") &
    (df["Food Styling"].isin(["Luxury","Premium"])) &
    (df["Editing Level"].isin(["Advanced","Cinema"])),
    "Yes",
    "No"
)

# ------------------------------------------------------------
# STEP 15: Create Estimated Production Complexity
# ------------------------------------------------------------

def complexity(row):

    score = 0

    if row["Drone"] == "Yes":
        score += 2

    if row["Actors Required"] == "Yes":
        score += 2

    if row["Shoot Days"] >= 3:
        score += 2

    if row["Editing Level"] == "Cinema":
        score += 2

    if row["Food Styling"] == "Luxury":
        score += 2

    if score <= 3:
        return "Low"

    elif score <= 6:
        return "Medium"

    else:
        return "High"

df["Project Complexity"] = df.apply(complexity, axis=1)

# ------------------------------------------------------------
# STEP 16: Check Final Dataset
# ------------------------------------------------------------

print("\nCleaned Dataset")

print(df.head())

print("\nShape:", df.shape)

print("\nMissing Values")

print(df.isnull().sum())

# ------------------------------------------------------------
# STEP 17: Save Clean Dataset
# ------------------------------------------------------------

df.to_csv(
    "Boof_Agency_Restaurant_Ad_Film_Client_Requests_Cleaned.csv",
    index=False
)

print("\nCleaned dataset saved successfully!")

# ------------------------------------------------------------
# STEP 18: Summary Statistics
# ------------------------------------------------------------

print("\nSummary Statistics")

print(df.describe(include="all"))

# ------------------------------------------------------------
# STEP 19: Revenue Summary
# ------------------------------------------------------------

print("\nTotal Revenue: $", df["Budget (USD)"].sum())

print("Average Budget: $", round(df["Budget (USD)"].mean(),2))

print("Highest Budget: $", df["Budget (USD)"].max())

print("Lowest Budget: $", df["Budget (USD)"].min())

print("Total Projects:", len(df))

# ------------------------------------------------------------
# STEP 20: Confirmation
# ------------------------------------------------------------

print("\nData Cleaning Completed Successfully!")

df.to_csv("Boof_Agency_Restaurant_Ad_Film_Client_Requests_Cleaned.csv", index=False)

print("Cleaned dataset exported successfully!")