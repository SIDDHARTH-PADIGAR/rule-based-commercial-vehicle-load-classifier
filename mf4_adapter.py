import pandas as pd

INPUT_FILE = "ecu_data.csv"
OUTPUT_FILE = "processed_test_cases.csv"

MAX_TOURQUE = 1000 # Nm - placeholder, adjust if known

def preprocess_mf4_csv(input_file):
    df = pd.read_csv(input_file)
    
    #Renaming and mapping import columns
    df = df.rename(columns={
        "ActlEngPrcntTorqueHighResolution": "percent_torque",
        "EngSpeed": "rpm",
        "DriversDemandEngPercentTorque": "driver_demand"
    })
    
    #Drop rows with un-useable data
    df = df.dropna(subset=["percent_torque", "rpm", "driver_demand"])
    
    #Compute real torque (approx)
    df["torque"] = (df["percent_torque"] / 100) * MAX_TOURQUE
    
    #Simulate or assign placeholders for required fields
    df["gear"] = 4  # Placeholder, or infer if available
    df["speed"] = 30.0  # km/h, placeholder
    df["elevation"] = 5.0  # m, placeholder
    df["voltage"] = 27.5  # V, placeholder
    df["weight"] = None # UNknown unless labeled
    
    # Derived features (optional but useful)
    df["power_kw"] = (df["torque"] * df["rpm"]) / 9550.0  # Convert Nm * RPM to kW
    df["power_density"] = df["power_kw"] / df["voltage"]
    df["stress_index"] = df["torque"] / df["elevation"] / df["speed"]
    df["rpm_per_gear"] = df["rpm"] / df["gear"]
    
    #Save the cleaned file
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Processed data saved to {OUTPUT_FILE}")
    
if __name__ == "__main__":
    preprocess_mf4_csv(INPUT_FILE)