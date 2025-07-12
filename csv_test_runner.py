import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from rule_engine.rule_engine import evaluate_vehicle_load
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import os

# Load processed dataset
df = pd.read_csv("data/verified_test_cases.csv")

# Run rule engine on all rows
results = []
for _, row in df.iterrows():
    res = evaluate_vehicle_load(
        torque=row["torque"],
        rpm=row["rpm"],
        gear=row["gear"],
        speed=row["speed"],
        elevation=row["elevation"],
        voltage=row["voltage"],
        weight=row["weight"],
        truck_id=row.get("truck_id", "test_truck")
    )
    results.append(res)

# Convert results to DataFrame
results_df = pd.DataFrame(results)

# Save results
os.makedirs("outputs", exist_ok=True)
results_df.to_csv("outputs/rule_engine_results.csv", index=False)

# Evaluation summary
y_true = results_df["expected_status"]
y_pred = results_df["predicted_status"]

print("\nEvaluation Summary")
print("-" * 50)
print(f"Total Vehicles Evaluated    : {len(results_df)}")
print(f"Overload Predictions        : {sum(y_pred == 'Overload')} ({(y_pred == 'Overload').mean() * 100:.2f}%)")
print(f"Actual Overloads           : {sum(y_true == 'Overload')}")
print(f"Model Accuracy              : {accuracy_score(y_true, y_pred) * 100:.2f}%")
print("\n" + classification_report(y_true, y_pred))

# Confusion matrix
cm = confusion_matrix(y_true, y_pred, labels=["Normal", "Overload"])
cm_df = pd.DataFrame(cm, index=["Actual Normal", "Actual Overload"], columns=["Predicted Normal", "Predicted Overload"])

plt.figure(figsize=(6, 5))
sns.heatmap(cm_df, annot=True, fmt="d", cmap="Blues")
plt.title("Confusion Matrix")
plt.savefig("outputs/confusion_matrix.png")
plt.close()

# Pie chart of predicted status
plt.figure(figsize=(5, 5))
results_df["predicted_status"].value_counts().plot.pie(autopct="%1.1f%%", startangle=90, colors=["seagreen", "tomato"])
plt.title("Predicted Load Status Distribution")
plt.ylabel("")
plt.savefig("outputs/prediction_distribution.png")
plt.close()

# Accuracy bar
plt.figure(figsize=(4, 5))
sns.barplot(x=["Accuracy"], y=[accuracy_score(y_true, y_pred)], palette="viridis")
plt.ylim(0, 1)
plt.title("Model Accuracy")
plt.savefig("outputs/accuracy_bar.png")
plt.close()

print("Evaluation complete. Visuals saved to 'outputs/' folder.")
