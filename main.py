
import csv

file_path = "suppliers.csv"

with open(file_path, mode="r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    suppliers = list(reader)

print("Total supplier records:", len(suppliers))
print("\nStarting data quality validation...\n")

seen_records = set()

for row_number, supplier in enumerate(suppliers, start=2):
    supplier_id = supplier["supplier_id"].strip()
    supplier_name = supplier["supplier_name"].strip()
    spend = float(supplier["spend"])

    # Rule 1: Check for a missing supplier ID
    if not supplier_id:
        print(f"Missing supplier ID: {supplier_name}")

    # Rule 2: Check for an exact duplicate record
    record_key = tuple(
        supplier[column].strip()
        for column in [
            "supplier_id",
            "supplier_name",
            "category",
            "spend",
        ]
    )

    if record_key in seen_records:
        print(f"Duplicate record found at CSV row {row_number}")
    else:
        seen_records.add(record_key)

    # Rule 3: Check for negative spend
    if spend < 0:
        print(f"Negative spend: {supplier_name}, {spend}")

print("\nData quality validation completed.")
# Next improvement: export validation issues to a CSV report
