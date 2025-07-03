import argparse
from rule_engine.rule_engine import evaluate_vehicle_load
from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np

# ------------- CLI Argument Parser -------------
parser = argparse.ArgumentParser(description="Evaluate custom vehicle telemetry")
parser.add_argument("--torque", type=float, required=True)
parser.add_argument("--rpm", type=float, required=True)
parser.add_argument("--gear", type=int, required=True)
parser.add_argument("--speed", type=float, required=True)
parser.add_argument("--elevation", type=float, required=True)
parser.add_argument("--voltage", type=float, required=True)
parser.add_argument("--weight", type=float, help="(Optional) actual known weight")
parser.add_argument("--truck_id", type=str, default="test_truck")
args = parser.parse_args()

# ------------- Evaluation Logic -------------
result = evaluate_vehicle_load(
    torque=args.torque,
    rpm=args.rpm,
    gear=args.gear,
    speed=args.speed,
    elevation=args.elevation,
    voltage=args.voltage,
    weight=args.weight,
    truck_id=args.truck_id
)

# ------------- Output to Terminal -------------
print("\n Evaluation Result:")
pprint(result)

# ------------- Visualization 1: Radar Chart -------------
def visualize_radar(res):
    metrics = {
        "Stress Index": (res["stress_index"], 150),
        "Power Density": (res["power_density"], 2.5),
        "Torque/Tonne": (res["actual_tpt"] or 0, 30),
        "RPM/Gear": (res["rpm_per_gear"], 600),
    }

    labels = list(metrics.keys())
    values = [v[0]/v[1] for v in metrics.values()]
    values += values[:1]

    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.plot(angles, values, color='crimson' if res["predicted_status"] == "Overload" else 'seagreen', linewidth=2)
    ax.fill(angles, values, alpha=0.25)
    ax.plot(angles, [1]*len(values), 'k--', linewidth=1)

    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.set_title(f"Radar View: {res['truck_id']} | {res['predicted_status']}", size=14, y=1.1)
    plt.tight_layout()
    plt.show()

# ------------- Visualization 2: Torque Comparison -------------
def visualize_torque_bar(res):
    expected = res["expected_tpt"]
    actual = res["actual_tpt"]

    fig, ax = plt.subplots()
    ax.bar(["Expected Torque/Tonne", "Actual Torque/Tonne"], [expected, actual], color=["gray", "crimson" if actual > expected else "seagreen"])
    ax.set_ylabel("Nm per Tonne")
    ax.set_title(f"Torque Analysis: {res['truck_id']}")
    plt.tight_layout()
    plt.show()

# ------------- Visualization 3: Weight Gauge -------------
def visualize_weight_gauge(res):
    from matplotlib.patches import Wedge

    weight = res["predicted_weight"]
    limit = 16.0  # assume max truck limit
    percentage = min(weight / limit, 1.0)

    fig, ax = plt.subplots(figsize=(6,3))
    ax.axis('equal')
    wedge = Wedge((0.5,0.5), 0.4, 180, 180 + 180*percentage, width=0.3, color='crimson' if weight > limit else 'seagreen')
    bg = Wedge((0.5,0.5), 0.4, 180, 360, width=0.3, color='lightgray')
    ax.add_patch(bg)
    ax.add_patch(wedge)
    ax.text(0.5, 0.65, f"{weight:.2f}t", ha='center', va='center', fontsize=14, weight='bold')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_title(f"Weight Gauge (Max Allowed: {limit}t)", y=1.05)
    plt.axis('off')
    plt.tight_layout()
    plt.show()

# ------------- Show All Visuals -------------
visualize_radar(result)
visualize_torque_bar(result)
##visualize_weight_gauge(result) commented out since we are running a rule-based classifier and not a regressor model
