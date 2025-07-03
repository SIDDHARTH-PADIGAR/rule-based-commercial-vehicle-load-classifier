#  Rule-Based Vehicle Load Detector

This project evaluates whether a commercial vehicle is overloaded using **rule-based logic** derived from engine telemetry data. Designed to run efficiently and cost-effectively (e.g., on ECUs or lightweight edge devices), it avoids the need for heavy ML models.

---

##  Problem Statement

Fleet operators struggle with detecting vehicle overloading in real time, which leads to increased maintenance, fuel inefficiency, and safety risks.

This system uses:
- Torque
- RPM
- Gear
- Speed
- Elevation
- Voltage  
to determine overload status — all using deterministic rules.

---

##  Sample Evaluation

**Input:**  
`torque=390 Nm`, `rpm=1800`, `gear=4`, `speed=28 km/h`, `elevation=10.5%`, `voltage=27.2 V`, `weight=13.2 tonnes`

**Output:**
```python
{
  'truck_id': 'test_truck',
  'stress_index': 146.25,
  'power_kw': 73.51,
  'power_density': 2.7,
  'rpm_per_gear': 450.0,
  'actual_tpt': 29.55,
  'expected_tpt': 20.0,
  'predicted_status': 'Overload',
  'expected_status': 'Overload',
  'match': True
}
````

---

##  Visual Outputs

Radar and Bar charts help visualize abnormalities like:

* Power-to-Voltage ratio (power density)
* Stress index
* Torque per tonne
* RPM per gear



![Screenshot 2025-07-03 205554](https://github.com/user-attachments/assets/19e75972-692d-48f6-922f-d61a55459a91)

![Screenshot 2025-07-03 205608](https://github.com/user-attachments/assets/e266e0f2-54c5-441e-a011-612f269fb8da)


---

##  Usage

Install dependencies:

```bash
pip install -r requirements.txt
```

Run a test case from the CLI:

```bash
python cli_test.py --torque 390 --rpm 1800 --gear 4 --speed 28 --elevation 10.5 --voltage 27.2 --weight 13.2
```
