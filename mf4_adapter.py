from asammdf import MDF
import pandas as pd

def extract_signals_from_mf4(mf4_path, signal_map=None):
    """
    Extract key vehicle telemetry signals from an .mf4 file.

    Args:
        mf4_path (str): Path to the .mf4 file.
        signal_map (dict): Optional mapping of readable names to actual signal names in the file.

    Returns:
        pd.DataFrame: Cleaned and structured telemetry data ready for evaluation.
    """
    mdf = MDF(mf4_path)

    # Set defaults based on common ECU fields (adapt to your real data schema)
    default_map = {
        "torque_percent": "ActualEngPercentTorque",  # Required
        "rpm": "EngSpeed",                           # Required
        "gear": "SelectedGear",                      # May be missing
        "voltage": "BatteryVoltage",                 # Optional
        "speed": "VehicleSpeed",                     # Optional
    }

    if signal_map:
        default_map.update(signal_map)

    extracted = {}
    for key, signal_name in default_map.items():
        try:
            sig = mdf.get(signal_name)
            extracted[key] = sig.samples
        except Exception:
            print(f"Warning: Signal '{signal_name}' not found in file.")
            extracted[key] = None

    # Begin dataframe construction
    df = pd.DataFrame()

    if extracted["torque_percent"] is not None:
        df["torque"] = pd.Series(extracted["torque_percent"]) * 10  # scale % torque
    if extracted["rpm"] is not None:
        df["rpm"] = pd.Series(extracted["rpm"])

    # Gear fallback
    if extracted.get("gear") is not None:
        df["gear"] = pd.Series(extracted["gear"]).fillna(4).astype(int)
    else:
        df["gear"] = 4

    # Speed fallback
    if extracted.get("speed") is not None:
        df["speed"] = pd.Series(extracted["speed"]).fillna(30.0)
    else:
        df["speed"] = 30.0

    # Voltage fallback
    if extracted.get("voltage") is not None:
        df["voltage"] = pd.Series(extracted["voltage"]).fillna(26.0)
    else:
        df["voltage"] = 26.0

    # Elevation and weight (static/fallback)
    df["elevation"] = 0.0
    df["weight"] = None

    # Drop incomplete rows (can’t evaluate without torque and rpm)
    df = df.dropna(subset=["torque", "rpm"])
    df = df.reset_index(drop=True)

    return df
