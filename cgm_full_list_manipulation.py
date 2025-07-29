import pandas as pd

# Load the Excel file and sheet
file_path = r"C:\Users\kyleh\Desktop\CGM_Project\CGM Analytics.xlsx"  # Adjust if needed
sheet_name = 'Full List'

# Read the main data
df = pd.read_excel(file_path, sheet_name=sheet_name)

# Print original dimensions
print(f"Original 'Full List' dimensions: {df.shape[0]} rows, {df.shape[1]} columns")

# Filter for procedure codes
target_codes = ['A4239', 'E2103']
filtered_df = df[df['Invoice Detail Proc Code'].isin(target_codes)].copy()

# Clean numeric fields
for col in ['Invoice Detail Allow', 'Invoice Detail Payments', 'Invoice Detail Charge', 'Invoice Detail Balance']:
    filtered_df[col] = pd.to_numeric(filtered_df[col], errors='coerce')

# Compute patient responsibility
filtered_df['Patient Responsibility'] = (
    filtered_df['Invoice Detail Allow'] - filtered_df['Invoice Detail Payments']
)

# Reorder columns
ordered_columns = [
    'Patient Last Name',
    'Patient First Name',
    'Policy Payor Name',
    'Invoice Detail ID',
    'Invoice Detail Proc Code',
    'Patient Responsibility',
    'Invoice Detail Charge',
    'Invoice Detail Allow',
    'Invoice Detail Payments',
    'Invoice Detail Balance',
    'Payment ID',
    'Payment Post Date',
    'Policy Pay %',
    'Sales Order SO Number',
    'Sales Order Confirm Date'
]
result_df = filtered_df[ordered_columns].sort_values(by='Patient Last Name')

# Add summary row
summary_data = {
    col: result_df[col].sum() if col in [
        'Patient Responsibility', 'Invoice Detail Charge',
        'Invoice Detail Allow', 'Invoice Detail Payments', 'Invoice Detail Balance'
    ] else '' for col in result_df.columns
}
summary_row = pd.DataFrame([summary_data])
result_df_with_summary = pd.concat([result_df, summary_row], ignore_index=True)

# Print new dimensions
print(f"Filtered output dimensions: {result_df_with_summary.shape[0]} rows, {result_df_with_summary.shape[1]} columns")

# ---------------------------
# Create patient responsibility by month sheet
# ---------------------------

# Extract required columns
monthly_data = filtered_df[['Patient Last Name', 'Patient First Name', 'Patient Responsibility', 'Invoice Detail Original DOS']].copy()

# Convert to datetime
monthly_data['Invoice Detail Original DOS'] = pd.to_datetime(monthly_data['Invoice Detail Original DOS'], errors='coerce')

# Extract Month-Year
monthly_data['Month'] = monthly_data['Invoice Detail Original DOS'].dt.to_period('M')

# Group by patient and month
grouped = monthly_data.groupby(
    ['Patient Last Name', 'Patient First Name', 'Month']
)['Patient Responsibility'].sum().reset_index()

# Pivot to wide format
pivot_df = grouped.pivot_table(
    index=['Patient Last Name', 'Patient First Name'],
    columns='Month',
    values='Patient Responsibility',
    fill_value=0
).reset_index()

# ---------------------------
# Save both sheets to Excel
# ---------------------------
output_path = r"C:\Users\kyleh\Desktop\CGM_Project\CGM_Patient_Analytics_Output.xlsx"
with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
    result_df_with_summary.to_excel(writer, sheet_name='Detailed Report', index=False)
    pivot_df.to_excel(writer, sheet_name='Monthly Responsibility', index=False)

print(f"File saved successfully with both sheets to: {output_path}")
