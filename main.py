
import csv

# Input and output files
input_file = "suppliers_test.csv"
output_file = "exceptions.csv"

# Read supplier records
with open(input_file, mode="r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    suppliers = list(reader)

print("Total supplier records:", len(suppliers))
print("\nStarting data quality validation...\n")

# Store detected issues
issues = []

# Track previously seen records and supplier IDs
seen_records = set()
seen_supplier_ids = set()

# Validate each supplier record
for row_number, supplier in enumerate(suppliers, start=2):
    supplier_id = supplier["supplier_id"].strip()
    supplier_name = supplier["supplier_name"].strip()
    category = supplier["category"].strip()
    spend_value = supplier["spend"].strip()

    # Rule 1: Check for a missing supplier ID
    if not supplier_id:
        issue_type = "Missing supplier ID"
        print(f"{issue_type}: {supplier_name}")

        issues.append({
            "supplier_id": supplier_id,
            "supplier_name": supplier_name,
            "issue_type": issue_type,
            "row_number": row_number
        })

    # Rule 2: Check for a repeated supplier ID
    if supplier_id:
        if supplier_id in seen_supplier_ids:
            issue_type = "Repeated supplier ID"
            print(f"{issue_type}: {supplier_id} at CSV row {row_number}")

            issues.append({
                "supplier_id": supplier_id,
                "supplier_name": supplier_name,
                "issue_type": issue_type,
                "row_number": row_number
            })
        else:
            seen_supplier_ids.add(supplier_id)

    # Rule 3: Check for an exact duplicate record
    record_key = (
        supplier_id,
        supplier_name,
        category,
        spend_value
    )

    if record_key in seen_records:
        issue_type = "Duplicate record"
        print(f"{issue_type} found at CSV row {row_number}")

        issues.append({
            "supplier_id": supplier_id,
            "supplier_name": supplier_name,
            "issue_type": issue_type,
            "row_number": row_number
        })
    else:
        seen_records.add(record_key)

    # Rule 4: Validate the spend value
    try:
        spend = float(spend_value)
    except ValueError:
        spend = None

        issue_type = "Invalid spend value"
        print(f"{issue_type}: {supplier_name}, '{spend_value}'")

        issues.append({
            "supplier_id": supplier_id,
            "supplier_name": supplier_name,
            "issue_type": issue_type,
            "invalid_value":spend_value,
            "row_number": row_number
        })

    # Rule 5: Check for negative spend
    if spend is not None and spend < 0:
        issue_type = "Negative spend"
        print(f"{issue_type}: {supplier_name}, {spend}")

        issues.append({
            "supplier_id": supplier_id,
            "supplier_name": supplier_name,
            "issue_type": issue_type,
            "row_number": row_number
        })

# Display validation summary
print("\nData quality validation completed.")
print("Total issues found:", len(issues))

# Export detected issues to a CSV report
fieldnames = [
    "supplier_id",
    "supplier_name",
    "issue_type",
    "invalid_value",
    "row_number"
]

with open(output_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(issues)

print(f"Exception report generated: {output_file}")
