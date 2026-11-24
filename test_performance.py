
from performance import PerformanceRecord

# Create a sample performance record
record = PerformanceRecord(
    branch_name="Eldoret",
    report_date="2026-11-23",
    performance_type="Revenue",
    target=100000,
    actual=85000,
    notes="Monthly revenue performance"
)

# Test the record
print("Branch:", record.branch_name)
print("Valid record:", record.is_valid())
print("Variance:", record.variance())
print("Achievement rate:", record.achievement_rate(), "%")
print("Status:", record.status())
