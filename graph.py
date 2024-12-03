import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Sample data creation
np.random.seed(0)
regions = ['Orissa', 'Karnataka', 'Tamil Nadu','Maharashtra', 'Gujrat', 'Bihar', 'UP', 'MP']
allocated_resources = np.random.randint(100, 800, size=8)
completion_rates = np.random.uniform(20, 100, size=8)
target_completion_rates = [90, 80, 85, 75, 70, 65, 60, 55]  # Target rates for demonstration

# 1. Resource vs. Completion Rate Bar Chart
fig, ax = plt.subplots(figsize=(10, 9))
ax.bar(regions, allocated_resources, color='skyblue', label='Allocated Resources')
ax.plot(regions, completion_rates, color='orange', marker='o', label='Completion Rate (%)')
ax.set_title("Resource Allocation vs. Completion Rate per Region")
ax.set_ylabel("Resources & Completion Rate (%)")
ax.legend()

# Display the chart for Resource vs. Completion Rate Bar Chart
plt.show()

# 2. Resource Utilization Efficiency Heatmap
# Calculate efficiency as completion per unit resource for simplicity
efficiency = [c / r for c, r in zip(completion_rates, allocated_resources)]
efficiency_df = pd.DataFrame({'Region': regions, 'Efficiency': efficiency})
efficiency_df.set_index('Region', inplace=True)

fig, ax = plt.subplots(figsize=(8, 4))
sns.heatmap(efficiency_df.T, annot=True, fmt=".2f", cmap="YlGnBu", ax=ax)
ax.set_title("Resource Utilization Efficiency Heatmap (Completion per Unit Resource)")
plt.show()

# 3. Time-Series Analysis for Allocation and Completion Rates (Simulated over 5 periods)
time_periods = ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8']
resource_allocation_trend = [allocated_resources + np.random.randint(-40, 40, size=8) for _ in time_periods]
completion_trend = [completion_rates + np.random.uniform(-8, 8, size=8) for _ in time_periods]

resource_df = pd.DataFrame(resource_allocation_trend, columns=regions, index=time_periods)
completion_df = pd.DataFrame(completion_trend, columns=regions, index=time_periods)

fig, ax = plt.subplots(figsize=(10, 6))
resource_df.plot(ax=ax, linestyle='--', marker='o')
ax.set_title("Time-Series Analysis of Resource Allocation per Region")
ax.set_ylabel("Resources Allocated")
ax.set_xlabel("Time Period")
plt.legend(loc='upper right')
plt.show()

fig, ax = plt.subplots(figsize=(10, 6))
completion_df.plot(ax=ax, linestyle='-', marker='o')
ax.set_title("Time-Series Analysis of Completion Rate per Region")
ax.set_ylabel("Completion Rate (%)")
ax.set_xlabel("Time Period")
plt.legend(loc='upper right')
plt.show()

# 4. Gap Analysis Visualization
gap_to_target = np.array(target_completion_rates) - np.array(completion_rates)
gap_df = pd.DataFrame({'Region': regions, 'Gap to Target (%)': gap_to_target, 'Allocated Resources': allocated_resources})
gap_df.set_index('Region', inplace=True)

fig, ax1 = plt.subplots(figsize=(10, 6))
gap_df['Gap to Target (%)'].plot(kind='bar', color='salmon', ax=ax1, position=0.5, width=0.4, label='Gap to Target (%)')
gap_df['Allocated Resources'].plot(kind='bar', color='lightblue', ax=ax1, position=-0.5, width=0.4, label='Allocated Resources')
ax1.set_title("Gap to Target Completion Rate and Resource Allocation per Region")
ax1.set_ylabel("Gap to Target (%) & Allocated Resources")
ax1.legend()

plt.show()
