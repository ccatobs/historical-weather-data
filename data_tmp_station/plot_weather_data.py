"""
Script to visualize weather data from dump_tmpwx.csv
Plots temperature, wind speed, and pressure over time
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the CSV file
print("Loading CSV file...")
df = pd.read_csv('dump_tmpwx.csv')

# Convert Datetime column to datetime type
df['Datetime'] = pd.to_datetime(df['Datetime'])

# Sort by datetime
df = df.sort_values('Datetime').reset_index(drop=True)

print(f"Data loaded successfully!")
print(f"Date range: {df['Datetime'].min()} to {df['Datetime'].max()}")
print(f"Total records: {len(df)}")
print(f"\nAvailable columns: {df.columns.tolist()}")

# Create a figure with 3 subplots
fig, axes = plt.subplots(3, 1, figsize=(16, 10))
fig.suptitle('Historical Weather Data Timeline', fontsize=16, fontweight='bold')

# ===== PLOT 1: Temperature =====
ax1 = axes[0]
if 'Temp_C_Avg' in df.columns:
    ax1.plot(df['Datetime'], df['Temp_C_Avg'], linewidth=0.8, color='orangered', alpha=0.7)
    ax1.set_ylabel('Temperature (°C)', fontsize=11, fontweight='bold')
    ax1.set_title('Temperature Over Time', fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.3)

# ===== PLOT 2: Wind Speed =====
ax2 = axes[1]
if 'WS_ms_Avg' in df.columns:
    ax2.plot(df['Datetime'], df['WS_ms_Avg'], linewidth=0.8, color='steelblue', alpha=0.7)
    ax2.set_ylabel('Wind Speed (m/s)', fontsize=11, fontweight='bold')
    ax2.set_title('Wind Speed Over Time', fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.3)

# ===== PLOT 3: Pressure =====
ax3 = axes[2]
if 'BP_mbar_Avg' in df.columns:
    ax3.plot(df['Datetime'], df['BP_mbar_Avg'], linewidth=0.8, color='forestgreen', alpha=0.7)
    ax3.set_ylabel('Pressure (mbar)', fontsize=11, fontweight='bold')
    ax3.set_xlabel('Date and Time', fontsize=11, fontweight='bold')
    ax3.set_title('Barometric Pressure Over Time', fontsize=12, fontweight='bold')
    ax3.grid(True, alpha=0.3)

# Format x-axis for all plots
for ax in axes:
    ax.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('weather_timeline.png', dpi=150, bbox_inches='tight')
print("\nPlot saved as 'weather_timeline.png'")

plt.show()

# Print some basic statistics
print("\n" + "="*60)
print("DATA STATISTICS")
print("="*60)
if 'Temp_C_Avg' in df.columns:
    print(f"\nTemperature (°C):")
    print(f"  Mean: {df['Temp_C_Avg'].mean():.2f}")
    print(f"  Min:  {df['Temp_C_Avg'].min():.2f}")
    print(f"  Max:  {df['Temp_C_Avg'].max():.2f}")
    print(f"  Std:  {df['Temp_C_Avg'].std():.2f}")

if 'WS_ms_Avg' in df.columns:
    print(f"\nWind Speed (m/s):")
    print(f"  Mean: {df['WS_ms_Avg'].mean():.2f}")
    print(f"  Min:  {df['WS_ms_Avg'].min():.2f}")
    print(f"  Max:  {df['WS_ms_Avg'].max():.2f}")
    print(f"  Std:  {df['WS_ms_Avg'].std():.2f}")

if 'BP_mbar_Avg' in df.columns:
    print(f"\nBarometric Pressure (mbar):")
    print(f"  Mean: {df['BP_mbar_Avg'].mean():.2f}")
    print(f"  Min:  {df['BP_mbar_Avg'].min():.2f}")
    print(f"  Max:  {df['BP_mbar_Avg'].max():.2f}")
    print(f"  Std:  {df['BP_mbar_Avg'].std():.2f}")
