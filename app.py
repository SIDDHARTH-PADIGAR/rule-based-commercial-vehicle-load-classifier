import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from mf4_adapter import extract_signals_from_mf4
from rule_engine.rule_engine import evaluate_vehicle_load

# Streamlit Page Setup
st.set_page_config(page_title="Vehicle Load Evaluator", layout="centered")
st.title("Vehicle Load Status Evaluator")
st.markdown("Upload vehicle telemetry (raw or processed) or manually enter values to evaluate load status.")

# Sidebar Input Choice
method = st.sidebar.radio("Choose Input Method", ["Manual Entry", "Upload CSV", "Upload .MF4"])

# Util to handle raw .mf4-style data or clean format
def derive_missing_fields(row):
    try:
        required = ["torque", "rpm", "gear", "speed", "elevation", "voltage"]
        if all(field in row for field in required):
            return evaluate_vehicle_load(
                row["torque"], row["rpm"], row["gear"], row["speed"],
                row["elevation"], row["voltage"], row.get("weight", None), row.get("truck_id", "from_csv")
            )
        else:
            # Handle ECU-style raw converted data
            rpm = row.get("EngSpeed") or row.get("rpm")
            torque = row.get("ActualEngPercentTorque") or row.get("ActlEngPrcntTorqueHighResolution")
            if torque and rpm:
                torque = float(torque) * 10
                rpm = float(rpm)
                return evaluate_vehicle_load(
                    torque,
                    rpm,
                    int(row.get("gear", 4)),
                    float(row.get("speed", 30.0)),
                    float(row.get("elevation", 0.0)),
                    float(row.get("voltage", 26.0)),
                    row.get("weight", None),
                    row.get("truck_id", "raw_ecu_input")
                )
            else:
                return {"error": "Missing required fields to compute prediction."}
    except Exception as e:
        return {"error": f"Failed to evaluate row: {e}"}

# Manual Entry
if method == "Manual Entry":
    st.header("Manual Telemetry Input")

    torque = st.slider("Torque (Nm)", 100, 800, 390)
    rpm = st.slider("RPM", 1000, 3000, 1800)
    gear = st.slider("Gear", 1, 8, 4)
    speed = st.slider("Speed (km/h)", 0.0, 120.0, 28.0)
    elevation = st.slider("Elevation (%)", -5.0, 20.0, 10.5)
    voltage = st.slider("Voltage (V)", 22.0, 30.0, 27.2)
    weight = st.number_input("Actual Weight (tonnes)", min_value=0.0, max_value=50.0, value=13.2)

    if st.button("Evaluate Vehicle"):
        result = evaluate_vehicle_load(torque, rpm, gear, speed, elevation, voltage, weight, truck_id="manual_input")
        st.subheader("Evaluation Result")
        st.json(result)

# CSV Upload Mode
elif method == "Upload CSV":
    st.header("Upload Telemetry CSV")
    uploaded_file = st.file_uploader("Upload CSV (Processed or Raw from ECU)", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.markdown("### Raw Uploaded Data")
        st.dataframe(df.head())

        st.markdown("### Evaluation Results")
        results = [derive_missing_fields(row) for _, row in df.iterrows()]
        result_df = pd.DataFrame(results)
        st.dataframe(result_df)

        if "error" in result_df.columns:
            st.warning("Some rows could not be evaluated. Check 'error' column.")

        if "predicted_status" in result_df.columns:
            overloads = result_df[result_df["predicted_status"] == "Overload"].shape[0]
            st.success(f"Overloaded Vehicles Detected: {overloads}")

            # Dashboard Visuals
            st.markdown("##Dashboard Summary")

            # Bar Chart - Load Status
            st.markdown("### Load Status Distribution")
            st.bar_chart(result_df["predicted_status"].value_counts())

            # Scatter: Stress Index vs Elevation
            if "stress_index" in result_df.columns and "elevation" in result_df.columns:
                st.markdown("### Stress Index vs Elevation")
                fig1, ax1 = plt.subplots()
                colors = result_df["predicted_status"].map({'Normal': 'blue', 'Overload': 'orange'})
                ax1.scatter(result_df["elevation"], result_df["stress_index"], c=colors)
                ax1.axhline(y=150, color='red', linestyle='--', label="Threshold")
                ax1.set_xlabel("Elevation (%)")
                ax1.set_ylabel("Stress Index")
                ax1.legend()
                st.pyplot(fig1)

            # Histogram: RPM per Gear
            if "rpm_per_gear" in result_df.columns:
                st.markdown("### RPM per Gear Distribution")
                fig2, ax2 = plt.subplots()
                ax2.hist(result_df["rpm_per_gear"], bins=30, color='purple')
                ax2.set_xlabel("RPM per Gear")
                ax2.set_ylabel("Frequency")
                st.pyplot(fig2)

            # Histogram: Power Density
            if "power_density" in result_df.columns:
                st.markdown("### Power Density Distribution")
                fig3, ax3 = plt.subplots()
                ax3.hist(result_df["power_density"], bins=30, color='green')
                ax3.set_xlabel("Power Density")
                ax3.set_ylabel("Frequency")
                st.pyplot(fig3)

# MF4 Upload Mode
elif method == "Upload .MF4":
    st.header("Upload Raw ECU File (.mf4)")
    uploaded_mf4 = st.file_uploader("Upload MDF (.mf4) File", type=["mf4"])

    if uploaded_mf4:
        with st.spinner("Parsing MF4 file..."):
            df = extract_signals_from_mf4(uploaded_mf4)

        if df.empty:
            st.error("Could not extract usable signals from file.")
        else:
            st.success(f"{len(df)} rows extracted from MF4 file.")
            st.dataframe(df.head())

            st.markdown("### Evaluation Results")
            results = []
            for _, row in df.iterrows():
                try:
                    res = evaluate_vehicle_load(
                        row["torque"], row["rpm"], row["gear"], row["speed"],
                        row["elevation"], row["voltage"], row.get("weight", None), truck_id="from_mf4"
                    )
                except Exception as e:
                    res = {"error": str(e)}
                results.append(res)

            result_df = pd.DataFrame(results)
            st.dataframe(result_df)

            if "error" in result_df.columns:
                st.warning("Some rows could not be evaluated.")

            if "predicted_status" in result_df.columns:
                st.success(f"Overloaded Vehicles Detected: {result_df[result_df['predicted_status'] == 'Overload'].shape[0]}")

                st.markdown("##Dashboard Summary")

                st.markdown("### Load Status Breakdown")
                st.bar_chart(result_df["predicted_status"].value_counts())
