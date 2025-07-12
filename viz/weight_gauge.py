import matplotlib.pyplot as plt
import streamlit as st

def visualize_weight_gauge(res):
    weight = res.get("actual_weight", 0)
    threshold = 13.0

    fig, ax = plt.subplots(figsize=(6, 1))
    ax.barh(["Truck"], [weight], color="crimson" if weight > threshold else "seagreen")
    ax.axvline(threshold, color='black', linestyle='--', label="Overload Threshold")
    ax.set_xlim(0, 20)
    ax.set_title("Vehicle Weight Status")
    ax.set_xlabel("Weight (tonnes)")
    st.pyplot(fig)
