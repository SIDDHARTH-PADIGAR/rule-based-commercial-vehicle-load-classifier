from asammdf import MDF
import pandas as pd

mf4_path = "data/sample3.mf4"
output_csv = "sample3.csv"

# Load the MDF file
mdf = MDF(mf4_path)

# Try dumping everything it can into a DataFrame
try:
    df = mdf.to_dataframe()
    df.to_csv(output_csv, index=False)
    print(f"Full data exported to {output_csv}")
except Exception as e:
    print(f"Failed to convert MF4 to CSV: {e}")
