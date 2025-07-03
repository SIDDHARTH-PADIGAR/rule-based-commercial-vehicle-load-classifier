import pandas as pd
from rule_engine.rule_engine import evaluate_vehicle_load

df = pd.read_csv("data/synthetic_vehicle_telemetry.csv")

results = []
for _, row in df.iterrows():
    result = evaluate_vehicle_load(
        torque=row['torque'],
        rpm=row['rpm'],
        gear=row['gear'],
        speed=row['speed'],
        elevation=row['elevation'],
        voltage=row['voltage'],
        weight=row.get('weight', None),
        truck_id=row.get('truck_id', None)
    )
    results.append(result)

results_df = pd.DataFrame(results)
results_df.to_csv("data/rule_engine_results.csv", index=False)
print(" Rule engine results saved to 'data/rule_engine_results.csv'")
