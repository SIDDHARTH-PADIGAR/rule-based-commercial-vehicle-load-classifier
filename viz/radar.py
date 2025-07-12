import matplotlib.pyplot as plt
import numpy as np

def visualize_radar(res):
    metrics = {
        "Stress Index": (res["stress_index"], 150),
        "Power Density": (res["power_density"], 2.5),
        "Torque/Tonne": (res["actual_tpt"] or 0, 30),
        "RPM/Gear": (res["rpm_per_gear"], 600),
    }

    labels = list(metrics.keys())
    values = [v[0] / v[1] for v in metrics.values()]
    values += values[:1]

    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.plot(angles, values, color='crimson' if res["predicted_status"] == "Overload" else 'seagreen', linewidth=2)
    ax.fill(angles, values, alpha=0.25)
    ax.plot(angles, [1] * len(values), 'k--', linewidth=1)

    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.set_title(f"{res['truck_id']} | Predicted: {res['predicted_status']}", size=14, y=1.1)

    st.pyplot(fig)
