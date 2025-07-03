from typing import Dict

# Baseline torque/tonne for each truck
baseline_torque_per_tonne = {
    "truck_001": 19.39,
    "truck_002": 20.48,
    "truck_003": 24.43
}

def evaluate_vehicle_load(torque, rpm, gear, speed, elevation, voltage, weight=None, truck_id=None):
    """
    Evaluates vehicle load status using rule-based thresholds on telemetry.

    Parameters:
        torque (float): Torque in Nm
        rpm (float): Engine RPM
        gear (int): Gear number
        speed (float): Vehicle speed in km/h
        elevation (float): Road gradient in percent
        voltage (float): Battery or engine voltage
        weight (float): (Optional) Actual weight in tonnes
        truck_id (str): (Optional) Identifier for the vehicle

    Returns:
        dict: Dictionary with computed metrics and classification
    """

    # Derived metrics
    stress_index = (torque * elevation) / speed
    power_kw = (torque * rpm) / 9550
    power_density = power_kw / voltage
    rpm_per_gear = rpm / gear
    torque_per_tonne = torque / weight if weight else None

    # Expected TPT from baseline if truck_id provided, fallback to default
    expected_tpt = baseline_torque_per_tonne.get(truck_id, 20.0)

    # Model's prediction
    overload = (
        stress_index > 150 or
        power_density > 2.5 or
        (torque_per_tonne and torque_per_tonne > 30) or
        rpm_per_gear > 600
    )
    predicted_status = "Overload" if overload else "Normal"

    # Ground truth from actual weight
    expected_status = None
    if weight is not None:
        expected_status = "Overload" if weight > 13.0 else "Normal"  # adjustable threshold
    match = (expected_status == predicted_status) if expected_status else None

    return {
        "truck_id": truck_id,
        "torque": torque,
        "rpm": rpm,
        "gear": gear,
        "speed": speed,
        "elevation": elevation,
        "voltage": voltage,
        "stress_index": round(stress_index, 2),
        "power_kw": round(power_kw, 2),
        "power_density": round(power_density, 2),
        "rpm_per_gear": round(rpm_per_gear, 2),
        "actual_weight": weight,
        "actual_tpt": round(torque_per_tonne, 2) if torque_per_tonne else None,
        "expected_tpt": expected_tpt,  # <--- Added for torque comparison visuals
        "predicted_status": predicted_status,
        "expected_status": expected_status,
        "match": match
    }
