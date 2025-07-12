# Vehicle Load Evaluator

A production-grade telemetry analysis tool to detect overloaded heavy vehicles using real ECU data.

**Note: This is a rule-based classifier, designed as a practical solution because ECUs (Electronic Control Units) often lack the computational resources to support ML model deployment. However, a machine learning alternative using XGBoost and Random Forest Classifier is also being developed in parallel.**

## Why it matters

Commercial vehicle OEMs lose millions annually due to improper loading, stress failures, and warranty abuse. This tool lets OEMs or fleet managers evaluate vehicle load status using direct `.mf4` logs from ECUs or preprocessed CSV telemetry.

## What it does

- Ingests raw `.mf4` files (industry standard format)
- Auto-extracts engine signals (torque %, RPM, etc.)
- Derives additional metrics: stress index, power density
- Applies a scalable rule-based classifier
- Outputs Overload or Normal status per vehicle
- Visualizes data on a real-time dashboard (Streamlit)

## Supported Inputs

- Raw ECU logs (`.mf4`)
- Raw or cleaned CSVs
- Manual parameter entry for testing

## Outputs

- Load classification (Normal / Overload)
- Key diagnostics: stress index, torque RPM plots, RPM/gear histograms
- Summary dashboard for fleet-level overview

**Ouptut with real-world MDF data:**
 <img width="881" height="464" alt="Screenshot 2025-07-12 180311" src="https://github.com/user-attachments/assets/9b4aba3f-6885-49ea-a3b8-7ac56a0df327" />

**Output with a verified test-case where 3 of the 6 vehicles are overloaded:**
<img width="750" height="836" alt="Screenshot 2025-07-12 180523" src="https://github.com/user-attachments/assets/cd48b556-7681-41d7-8cef-30ae6f16731d" />

## Built for scale

- Handles raw signal noise and missing fields
- Designed to integrate with live vehicle telemetry
- Cloud-ready, modular codebase, built with extensibility in mind

