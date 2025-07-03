#!/bin/bash

echo "Running rule engine..."
python3 main.py

echo "Generating visualizations..."
python3 -i viz.py
