import matplotlib.pyplot as plt
import streamlit as st

def visualize_torque_bar(res):
    actual = res["actual_tpt"]
    expected = res.get("expected_tpt", 20)

    fig, ax = plt.subplots()
    ax.bar(["Expected"], [expected], color="seagreen")
    ax.bar(["Actual"], [actual], color="crimson" if actual > expected else "dodgerblue")
    ax.set_ylabel("Torque/Tonne")
    ax.set_title("Torque Comparison")
    st.pyplot(fig)
