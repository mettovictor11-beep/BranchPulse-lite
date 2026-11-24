
from performance import PerformanceRecord
from database import update_record, get_all_records
from database import delete_record

# Create updated performance details
updated_record = PerformanceRecord(
    branch_name="Eldoret",
    report_date="2026-11-24",
    performance_type="Revenue",
    target=100000,
    actual=95000,
    notes="Updated monthly revenue performance"
)

# Update record with ID 1
update_record(1, updated_record)

# Display all records
print("\nUpdated performance records:")

for record in get_all_records():
    print(record)


# Delete record with ID 3
delete_record(3)

print("\nRecords after deletion:")

for record in get_all_records():
    print(record)    
